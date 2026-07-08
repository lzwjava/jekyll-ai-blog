---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计算受限批量大小恒定吞吐量
translated: true
type: note
---

**问题：** 我正以一个批次大小 (batch) 为 48 的配置，在一张 H200 (显存 135GB/144GB, GPU 利用率 100%, MFU 66%) 上训练一个模型。我该如何考虑选择批次大小？因为即使增大批次，墙钟时间 (wall-clock time) 也并未显著缩短。

**回答：**

你的直觉是合理的——GPU 利用率（100%）已经揭示了原因。你目前处于**计算受限 (compute-bound) 状态，而非启动开销受限 (launch-overhead-bound) 状态**。这改变了批大小能做什么，以及不能做什么。

## 核心公式

对于密集 (dense) Transformer 模型，每步的 FLOPs 随批大小线性增长：

```
FLOPs_per_step ≈ 6 * N * B * T
```

其中 `N` = 参数数量，`B` = 批大小，`T` = 序列长度（来自 Kaplan 等人的标准 6ND 近似）。你的单步时间 (step_time) 是：

```
step_time ≈ FLOPs_per_step / (peak_FLOPs * MFU)
```

所以 `tokens/sec = B*T / step_time = peak_FLOPs * MFU / (6*N)` — **批大小在此处被抵消了**。一旦你处于计算受限状态且利用率达到 100%，tokens/秒 就取决于你的**硬件效率 (MFU)**，而不是你的批大小。这正是为什么加倍批大小只会导致单步时间加倍，而 tokens/秒 基本保持不变——你已经在实践中验证了这一点（批大小=48 时达到 136,700 tok/s）。

批大小仅在**开销受限 (overhead-bound) 状态**下才能提升墙钟速度：当批大小很小时，GPU 在内核启动之间处于空闲状态，等待数据加载器，或是在分布式训练中为固定的 allreduce/同步延迟付出代价。在这种状态下，增大 B 可以将固定开销分摊到更多的有用计算上，并且 tokens/秒 会随着 B 增加而上升，直到你触及计算受限的平稳期——而你现在已经处在这个平稳期上了。

## 在计算受限状态下，批大小实际控制什么

1.  **梯度噪声 (Gradient noise)，而非吞吐量 (throughput)。** McCandlish 等人的梯度噪声尺度框架衡量了跨训练样本的梯度的信噪比，并预测了某个任务的最大有效批大小。同时，该框架表明，噪声尺度会随着训练损失降低而增大，并且主要通过与模型性能相关的模型大小来影响。低于临界批大小 (CBS) 时，更大的 B 会降低梯度方差，使你可以迈出更大、更可靠的一步——收敛所需的步数相同，但每步的噪声更少。高于 CBS 时，你只是在浪费算力，几乎无法进一步减少信号波动（每个额外的样本与批中已有的样本几乎冗余）。

2.  **一篇值得了解的后续论文**发现，噪声尺度方法在实践中并不稳健：虽然大批大小对于快速训练是必要的，但过大的批大小会损害 token 效率。并且，虽然 McCandlish 等人的基于梯度噪声的 CBS 估计已在实践中使用（例如 GPT-3），但其背后的假设很强，可靠性也不明确。实验证明，梯度噪声尺度可能会将真实的临界批大小低估几个数量级，尤其是在更大的模型规模下。不要盲目相信噪声尺度公式——如果你关心它，请通过实验测量 CBS。

3.  **达到特定 token 预算的总墙钟时间**大致为：

```
total_time ≈ total_tokens_needed / tokens_per_sec
```

由于一旦进入计算受限状态，`tokens_per_sec` 是稳定的，那么对于固定的 token 预算，你的总训练墙钟时间**基本上与批大小无关**——剩下的唯一杠杆是提升 MFU（更好的内核、更少的重计算、更好的重叠）或使用更少的总计算量（更高效的扩展/更好的数据）。

## 针对你当前训练的实际建议

你的 MFU 是 66%——不错但未达到上限（H200 搭配优秀内核 + FlashAttention 通常可以达到 50-60%+ 用于密集模型；对于路由开销较大的 MoE 模型，66% 已经相当不错了）。这才是你剩余墙钟性能增益的来源，而非批大小：

```python
# 快速基准测试工具，找出你实际的开销受限 -> 计算受限的转折点
import time, torch

def bench(model, optimizer, batch_sizes, seq_len, steps=5):
    results = {}
    for B in batch_sizes:
        x = torch.randint(0, 32000, (B, seq_len), device="cuda")
        y = torch.randint(0, 32000, (B, seq_len), device="cuda")
        torch.cuda.synchronize()
        t0 = time.time()
        for _ in range(steps):
            optimizer.zero_grad(set_to_none=True)
            loss = model(x, labels=y).loss
            loss.backward()
            optimizer.step()
        torch.cuda.synchronize()
        dt = (time.time() - t0) / steps
        toks_per_sec = B * seq_len / dt
        results[B] = toks_per_sec
        print(f"B={B:4d}  step_time={dt*1000:7.1f}ms  tok/s={toks_per_sec:,.0f}")
    return results

# 进行扫描，找到 tok/s 停止增长的点——那就是你的计算受限下限
bench(model, optimizer, batch_sizes=[8, 16, 24, 32, 48, 64], seq_len=2048)
```

如果在这个测试中，tok/s 在 B=24-32 时已经持平，那就证实了 B=48 纯粹是一个梯度质量的选择，而不是吞吐量的选择——实际上你可以降低到更小的 B（从而释放显存用于更长的上下文或更大的 MoE Expert 容量），而不会带来墙钟时间上的损失，只要保持在你的经验 CBS 之上即可。

## MoE 特有的复杂因素（与你 DeepSeek v4 的工作相关）

对于 MoE，批大小也决定了**每步每个 Expert 的 token 数**。假设有 `E` 个 Expert 和 top-`k` 路由，每步路由到某个特定 Expert 的预期 token 数约为 `B*T*k/E`。批大小过小 → Expert 负载方差高 → 某些 Expert 饥饿，容量因子 (capacity-factor) 被触发，丢弃的 token 会损害质量，这与上述的噪声尺度论点无关。这是第二个、MoE 特有的保持批大小高于某个下限的原因，与梯度噪声论点不同——值得在不同 B 值下检查你的路由器的丢弃 token 率，而不仅仅是 tok/s。

## 总结

-   批大小不再帮助提升墙钟速度，因为你已处于计算受限状态（利用率 100%）——这是预期且正确的，不是 bug。
-   根据**梯度噪声 / MoE 负载均衡**来调整批大小，而不是根据吞吐量。
-   通过提升 **MFU**（核融合、FA3/FA2 调优、激活检查点权衡、序列打包等）来追求墙钟性能的提升——一旦利用率被钉死，这是你剩下的唯一杠杆。

参考：

-   [大规模批量训练的经验模型 (McCandlish 等人, 2018)](https://arxiv.org/abs/1812.06162)
-   [临界批量大小再探讨 (2025)](https://arxiv.org/abs/2505.23971)