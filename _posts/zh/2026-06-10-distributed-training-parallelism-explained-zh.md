---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式训练并行性详解
translated: true
type: note
---

**问题：** 分布式训练在底层是如何工作的？它真的能帮助 nanochat 760M 在 MI300X 上运行吗？

**回答：**

## 先理解一个训练步骤实际是什么

无论你有多少 GPU，每个训练步骤都是相同的三个阶段：

```python
loss = model(x, y)        # 前向：激活值
loss.backward()           # 反向：梯度
optimizer.step()          # 更新：权重 -= f(梯度)
```

分布式训练只是回答一个问题的答案：**这三个阶段中的哪个阶段你要拆分，沿着哪个维度拆分？** 正好有三个维度可以沿其拆分——批次、权重和层——从而产生三种并行范式。

---

## 1. 数据并行 (DP/DDP) — 拆分批次

每个 GPU 都持有模型的**完整副本**。你拆分批次。

关键洞察是数学上的：一个批次上的平均损失的梯度就是每个样本梯度的平均值：

```
∇L(batch) = (1/B) Σᵢ ∇L(xᵢ)
          = (1/N) Σₖ [ (1/(B/N)) Σᵢ∈GPUₖ ∇L(xᵢ) ]
            ─────   ──────────────────────────────
            平均           GPU k 上的本地梯度
```

因此每个 GPU 在其分片上计算梯度，然后你在 **GPU 间平均梯度**——每个副本都执行相同的优化器步骤。副本始终保持逐位一致（第 0 步通过广播进行相同的初始化，每一步都有相同的平均梯度）。

最简实现，无需框架魔法：

```python
import torch, torch.distributed as dist

dist.init_process_group("nccl")  # ROCm 上使用 RCCL，API 相同
rank, world = dist.get_rank(), dist.get_world_size()
torch.cuda.set_device(rank)

model = GPT(config).cuda()
# 第 0 步：让所有副本相同
for p in model.parameters():
    dist.broadcast(p.data, src=0)

for step in range(num_steps):
    x, y = get_batch(rank)            # 每个 rank 获得不同的数据
    loss = model(x, y)
    loss.backward()
    for p in model.parameters():      # 在所有 rank 间平均梯度
        dist.all_reduce(p.grad, op=dist.ReduceOp.AVG)
    optimizer.step()
    optimizer.zero_grad()
```

这就是 DDP 的全部本质。`torch.nn.parallel.DistributedDataParallel` 在此之上添加了两个优化：

**a) 分桶 + 重叠。** 与在最后对每个张量执行一次 AllReduce 不同，DDP 注册了 autograd 钩子。一旦在 `backward()` 期间某个梯度就绪，它就会被放入一个约 25MB 的桶中；满桶的 AllReduce **异步执行，而此时 backward 仍在计算更早的层**。由于反向传播是从最后一层到第一层，第 24 层梯度的通信与第 1 层的计算重叠。在 transformer 上，这隐藏了大部分通信开销。

**b) `no_sync()` 用于梯度累积。** 你只在最后一个微批次上执行 AllReduce：

```python
for i in range(grad_accum_steps):
    ctx = model.no_sync() if i < grad_accum_steps - 1 else nullcontext()
    with ctx:
        loss = model(x_i, y_i) / grad_accum_steps
        loss.backward()
optimizer.step()
```

nanochat 已经这样做了——查看 `base_train.py`，它从 torchrun 读取 `RANK`/`WORLD_SIZE`，并将 `total_batch_size` 除以 world size。

### AllReduce 的实际成本

Ring AllReduce 每个 GPU 移动 `2 × (N-1)/N × bytes`，与 GPU 数量无关——对于你的 760M 可训练矩阵（bf16），大约是 **~1.5 GB 每步** 通过互连传输。在具有 Infinity Fabric（~几百 GB/s）的 MI300X 节点上，这需要几十毫秒——而且它与反向传播重叠。对于这种规模的模型，DP 几乎线性扩展。

---

## 2. 张量并行 — 拆分权重

每个矩阵乘法都被分片。对于 `Y = XW`，其中 `W [1536, 6144]` 按列拆分为 4 个 GPU，每个 GPU 计算 `X @ W[:, shard]`，然后你进行拼接。Megatron 风格的 TP 在升投影上进行列拆分，在降投影上进行行拆分，因此每个 MLP 只需要**一次 AllReduce**，每个注意力块也只需要一次——但这是每**层**、每**前向和反向**、在关键路径上的操作。它不能像 DDP 的通信那样被隐藏。

当你**一层的权重/激活放不下**时，或者当你需要扩展 batch=1 的延迟时，你才使用 TP。760M 模型在 192 GB GPU 上距离需要这一点还有大约两个数量级。

## 3. 流水线并行 — 拆分层

GPU 0 持有层 0-11，GPU 1 持有层 12-23。激活值向前流动，梯度向后流动。朴素 PP 会让 GPU 空闲（"气泡"）；GPipe/1F1B 调度将气泡缩小到 `(stages-1)/(microbatches+stages-1)`。只有当模型即使使用 ZeRO 也放不下时才相关。不是你的问题。

## 4. ZeRO/FSDP — 没有内存冗余的数据并行

普通 DDP 浪费内存：权重 + 梯度 + 优化器状态的 N 份副本。对于 760M，使用你的 Muon/Adam 混合，每个 GPU 大约有 ~10 GB 的状态被复制。ZeRO-1/2/3 对优化器状态 → 梯度 → 参数进行分片，通过即时 AllGather 重建。权衡：更多的通信换取更少的内存。你在单个 GPU 上已经使用了 105/192 GB——**内存不是你的限制**，所以 ZeRO 对你没有任何好处。

---

## 现在应用到你的运行

根据总结中的数据：1× MI300X，7.7 秒/步，每步 8 个梯度累积微批次，27.5% MFU，29K 步 ≈ 62 小时。存在两个独立的低效问题，并且顺序很重要，先处理哪个问题：

**低效 1：每 FLOP 效率 (MFU=27%)。** 这是一个*内核*问题——SDPA 数学回退而不是融合的 flash attention，加上完整的 `L` 注意力而不是 `SSSL` 滑动窗口。**DP 不能解决这个问题。** 四个 GPU 在 27% MFU 下，每个 GPU 都浪费了 73% 的计算能力。你将支付 4 倍的 $/hr，得到 4 倍的低效基线。

**低效 2：墙钟串行化。** 你的 8 个梯度累积微批次是串行执行的。这正是 DP 可以并行化的地方——使用 8 个 GPU，梯度累积降为 1，8 个微批次在的不同设备上同时运行：

```
1 GPU:  step = 8 × (fwd+bwd) + opt           ≈ 7.7 s
8 GPUs: step = 1 × (fwd+bwd) + allreduce + opt ≈ 1.1–1.3 s
```

相同的 `total_batch_size=524288`，相同的损失曲线，~6-7 倍墙钟加速（通信 + 每个微批次的固定开销会消耗一点）。命令很简单，因为 nanochat 已经为 DDP 做好了准备：

```bash
torchrun --standalone --nproc_per_node=8 -m scripts.base_train \
  --depth=24 --window-pattern=L --total-batch-size=524288
```

其他什么都不用改变——超参数、学习率、token 预算都保持不变，因为*有效批次*没有改变。这就是正确实现 DP 的美妙之处：它在数学上对优化过程是不可见的。

### 决策表

| 配置 | MFU | 墙钟时间 | 成本 @ ~$2/h/GPU |
| --- | --- | --- | --- |
| 1× MI300X, SDPA (当前) | 27% | ~62 h | ~$124 |
| 1× + ROCm flash-attn, SSSL | ~45–50% | ~33 h | ~$66 |
| 8× MI300X, SDPA | 27% | ~10 h | ~$160 |
| 8× + flash-attn | ~45% | ~5–6 h | ~$90 |

所以：**分布式训练绝对有助于你的墙钟时间，接近线性，只需一行命令更改**——nanochat 的 DDP 路径已经就绪。但它没有触及你的成本效率问题，即 SDPA 内核。操作顺序：

1. **首先尝试 ROCm flash-attn**（在 droplet 上运行 `pip install flash-attn --no-build-isolation`；AMD 维护了一个 ROCm 分支 `ROCm/flash-attention`，如果上游无法为 gfx942 构建，可以使用它）。这将同时将时间和成本减半。
2. **然后**，如果你想在几小时内而不是几天内完成，再添加 GPU——并且只有在那时，因为每个额外的 GPU 都会乘以你已经固定的每个 GPU 效率。

一个值得注意的警告，以便你在进一步扩展时了解：在非常大的 world size 下，DP 要么迫使用巨大的全局批次（最终会损害收敛——参见 McCandlish 等人的"An Empirical Model of Large-Batch Training"中的关键批次大小概念），要么使用极小的每 GPU 批次（这会降低 MFU）。这时 TP/PP/ZeRO 就不再是学术问题了。对于 760M 和 ≤8 个 GPU，你远未达到这一点——纯 DP 是正确且完整的答案。

**参考文献：**

- [PyTorch DDP 设计文档（分桶，重叠）](https://pytorch.org/docs/stable/notes/ddp.html)
- [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054)
- [Megatron-LM: 张量并行](https://arxiv.org/abs/1909.08053)
- [ROCm flash-attention 分支](https://github.com/ROCm/flash-attention)
- [An Empirical Model of Large-Batch Training](https://arxiv.org/abs/1812.06162)
