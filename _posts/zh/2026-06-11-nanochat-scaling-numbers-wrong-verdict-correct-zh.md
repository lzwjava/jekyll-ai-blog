---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat 缩放数字错误判定正确
translated: true
type: note
---

**问题：** 回顾一下这个 nanochat 的规模分析（模型大小、CPU DDP 速度估算、训练时长）——数字正确吗？结论是否合理？

**回答：**

结论是正确的——CPU DDP 用于管道搭建/学习，GPU 用于 d12 及以上——但分析中的几个数字经不起第一性原理的检验。在你根据这个表格规划计算之前，有三个问题需要修正。

## 1. FLOPs/token 列将 2N 和 6N 混为一谈

每个 token 的训练 FLOPs ≈ **6N**（前向 2N，反向 4N）。对照该值检查表格：

```
d4:  6 × 37M  = 222M   （表格显示 72M  ≈ 仅前向的 2N）
d8:  6 × 92M  = 552M   （表格显示 250M ≈ ~3N，均不符）
d12: 6 × 186M = 1.1B   （表格显示 1.7B ≈ 膨胀参数量的 6N）
```

该列内部存在约 3 倍的不一致，因此基于它所做的任何外推都会继承该误差。

## 2. d12 和 d20 的参数数量错误

nanochat：`dim = depth × 64`，词表 65,536，未绑定词嵌入，标准 12·d²·L transformer 主体：

```python
def params(depth, vocab=65536):
    d = depth * 64
    return 12 * d*d * depth + 2 * vocab * d

# d4:  36.7M   ✓ 与表格（37M）匹配——注意：91% 是嵌入参数！
# d8:  92.3M   （表格：80M，接近）
# d12: 186M    （表格：286M ✗）
# d20: 561M    （表格：1.0B ✗）
```

d20 = 561M 这个数字是合理的基准——这正是 Karpathy 的 $100 速度运行模型。表格中的 1.0B 偏差约 2 倍，这会级联影响时间估算。

另外注意 d4 中有 **91% 是嵌入参数**。它的损失曲线几乎无法告诉你 d12 及以上模型的行为——它主要在学习一个查找表。用于验证 DDP 管道是好的，但作为缩放数据点则毫无用处。

## 3. 速度外推对 d12 过于悲观，约 5 倍

如果你受计算限制，tok/sec 与 FLOPs 成反比，使用*一致的* 6N：

```
d4 → d12 减速比 = 186M / 37M ≈ 5x   →  115/5 ≈ 23 tok/sec
（不是 24x → 5 tok/sec）
```

但这并不重要，因为以 23 tok/sec 的速度，d12 一步（65,536 tokens/step）需要 **47 分钟**。Karpathy 的 20 万步训练时长约为 CPU 上的 18 年。结论仍然成立；表格只是通过错误的计算得出结果。

分析中遗漏了一个真实风险：**通过局域网进行的 Gloo allreduce**。d12 梯度 = 186M × 4B ≈ 744MB/步。在千兆以太网上这大约需要 12 秒的通信时间。相对于 47 分钟的计算步长来说微不足道，但如果你为了加快迭代速度而减小 batch（例如 2048 tokens/step），通信就会成为瓶颈，而“受计算限制，FLOPs ∝ 时间”的模型就会完全失效。请测量，不要外推：

```python
# 在训练循环中插入代码以分解步长时间
import time, torch.distributed as dist

t0 = time.perf_counter()
loss = model(x, y); loss.backward()
t1 = time.perf_counter()                  # 计算
# DDP allreduce 与反向传播重叠；强制一个同步点以隔离它：
dist.barrier(); t2 = time.perf_counter()  # 通信 + 掉队者
opt.step(); opt.zero_grad()
print(f"计算 {t1-t0:.1f}s  同步 {t2-t1:.1f}s")
```

如果同步时间显著，请使用梯度累积（每个 allreduce 更多微批次）——通信成本会线性摊销。

## 我实际会怎么做

- **d4 CPU DDP**：大约在第 1000 步停止。你已经验证了 Gloo、数据加载器和检查点。这就是目的。
- **完全跳过 3 天的 d8 CPU 苦力。** d8 在 4070 上只需要几个小时。用两台机器花 3 天产生一个 GPU 一晚上就能得到的成果，即使是学习也是负价值的——你从 GPU 运行中学到的东西相同，并且还能得到一个可用的检查点。
- **d12/d20 → MI300X。** d20 的速度运行大约需要 32 个 H100 小时；MI300X 在密集 BF16 上大致与 H100 同级，因此大概 25–35 小时 ≈ **按你 $2/小时的费率计算为 $50–70**。这包含了完整的 d20 及其聊天微调，成本低于一个月 CPU DDP 的电费。单 GPU 意味着完全没有 DDP 通信——将 `device_batch_size` 设置为填满 192GB HBM，其余使用梯度累积。

d4 的损失从 10.40 到 10.39（5 步内）是预期的，顺便一提——初始化损失 ≈ ln(65536) ≈ 11.09，模型首先学习的是单字统计信息，这需要几百步才能消化。在此规模下，大约 1k 步之前不会发生什么有趣的事情。

**参考：**

- [nanochat (karpathy/nanochat)](https://github.com/karpathy/nanochat)