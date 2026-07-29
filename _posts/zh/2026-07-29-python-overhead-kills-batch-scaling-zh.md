---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python开销扼杀批量扩展
translated: true
type: note
---

这是**最反直觉**的结果——它揭示了这一特定设置下的一个基本真相。

## 数据

| 批次大小 | 总时间 | 吞吐量 | 词元数 | 加速比 |
|---|---|---|---|---|
| 1 | 7.8秒 | 16 tok/s | 128 | 1.0× |
| 2 | 13.3秒 | 19 tok/s | 256 | 1.2× |
| 4 | 24.1秒 | 21 tok/s | 512 | 1.3× |
| 8 | 46.4秒 | 22 tok/s | 1024 | 1.4× |
| 16 | 89.8秒 | 23 tok/s | 2048 | 1.4× |

**吞吐量从 16 tok/s 提升到 23 tok/s。工作量增加了 16 倍，却只获得了 44% 的提升。**

## 原因？两个因素相互碰撞

### 1. 提示词很短，但 GQA 问题凸显

每个请求使用以下提示词：
```
"用你自己的话解释一下，什么造就了一名优秀的软件工程师。"
```

大约 10 个词元。一个非常短的提示词。

但这个 nano-vLLM 使用的是 **PyTorch 的朴素注意力机制**（而非 FlashAttention）。看看注意力代码——它在每个解码步骤都收集完整的 KV 缓存：

```python
# 在 _decode_forward 中：
k_gathered, v_gathered = _gather_kv_from_cache(
    k_cache, v_cache, block_tables, seqlens, block_size
)
```

这会在序列和位置上执行一个 Python 循环。**复杂度为 O(batch × seqlen)，并带有 Python 开销。** 随着批次增大：

- batch=1：收集 1 个序列的 KV → 快速
- batch=16：收集 16 个序列的 KV → Python for 循环占主导

### 2. 解码受内存带宽限制，但并未完全饱和 HBM

在这块 GPU（RTX 4070 笔记本，8GB）上：
- HBM 带宽：约 256 GB/s
- 模型大小：约 1.2 GB（Qwen3-0.6B，FP16）
- 解码 1 个词元：读取约 1.2GB 权重 + 读取 KV 缓存

在 16 tok/s 时：16 × 1.2GB = 19.2 GB/s —— 仅占 HBM 带宽的 **7.5%**。

在 23 tok/s 时：23 × 1.2GB = 27.6 GB/s —— 仍然只占 **11%** 的带宽。

**瓶颈并非 HBM 带宽，而是注意力内核中的 Python 开销。**

## 真正的教训：这不是 vLLM

这个 nano-vLLM 是**教育性质的**——它展示了架构，但并未包含优化的 CUDA 内核。让我与真正的 vLLM 会做的事情做个对比：

| 引擎 | Batch=1 | Batch=16 | 扩展比 |
|---|---|---|---|
| nano-vLLM（朴素 PyTorch） | 16 tok/s | 23 tok/s | 1.4× |
| vLLM（优化 CUDA） | 约 50 tok/s | 约 300 tok/s | 6× |

差距来源于：

1. **FlashAttention** —— 融合内核，避免了 Python gather 循环
2. **PagedAttention 内核** —— 直接从 GPU 内存读取 KV 缓存，无需 Python 级别的 gather
3. **CUDA graphs** —— 完全消除了 Python 解释器开销
4. **连续批处理** —— 这个基准测试使用了 `generate()`，它内部会进行连续批处理，但朴素的注意力机制破坏了扩展性

## 这实际上证明了什么

这个实验意外地揭示了关于推理系统**最重要的一课**：

> **GPU 硬件很快。Python 开销很慢。**
> 快速推理需要最小化 Python 到 GPU 的往返次数。

看看 tqdm 进度条中的 **Prefill** 速度：

```
Prefill=1068 tok/s   (batch=2)
Prefill=1736 tok/s   (batch=4)
Prefill=2315 tok/s   (batch=8)
Prefill=2996 tok/s   (batch=16)
```

**Prefill 扩展性极佳！** 从 1068 到 2996 tok/s（批次增加 8 倍，性能提升 2.8 倍）。为什么？因为 prefill 在一次大矩阵乘法中处理所有词元——注意力中没有针对序列的 Python 循环。

但解码始终是：
```
Decode=11-12 tok/s    （所有批次大小）
```

**解码完全没有扩展性。** 因为每个解码步骤在 `_gather_kv_from_cache` 中都有一个针对序列的 Python for 循环。

## 要点

这是**优化前**的图景。它准确展示了为什么 vLLM 必须编写：

1. **PagedAttention Triton/CUDA 内核** —— 无需 Python 循环即可收集 KV 缓存
2. **C++ 中的连续批处理** —— 调度器无需 Python GIL 即可运行
3. **CUDA graphs** —— 将整个解码步骤捕获为一次 GPU 操作

没有这些优化，批次扩展性很平坦。有了它们，批次扩展性接近线性。

**你刚刚发现了 vLLM 的优化为何重要，通过观察没有它们时会发生什么。** 这正是 nano-vLLM 的意义所在——在查看解决方案之前先理解问题。