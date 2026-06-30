---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang推理中的冷启动成本
translated: true
type: note
---

**问题：** 在 SGLang 中，作为冷启动成本的“CUDA graph capture”和“KV cache allocation”具体指什么？为什么预热后 TTFT（首 token 生成时间）会从 8.5 秒降至约 17 毫秒？

**回答：**

这些是在首次请求时产生的一次性初始化成本，而非每个 token 的成本。让我分别解释一下。

### CUDA 图捕获

通常，每次 CUDA 内核启动都需要经过 CPU：Python → PyTorch 调度器 → CUDA 运行时 → GPU。对于一个 transformer 解码步骤，你需要启动*数百个*微小的内核（注意力、层归一化、GEMM（通用矩阵乘法）、RoPE（旋转位置编码）、采样）。在小批量大小下，GPU 完成每个内核的速度比 CPU 排队下一个内核的速度更快——你受限于**启动开销**，而非计算能力。GPU 空闲等待 CPU 的分派开销（数百个内核的每个启动约 5–10 微秒）。

**CUDA 图**会将整个内核启动序列一次性记录到一个静态图中，然后通过单个 `cudaGraphLaunch` 调用进行重放。无需 Python，无需逐内核分派。

```python
# 概念上捕获所做的工作：
g = torch.cuda.CUDAGraph()
# 预热，以便 cuBLAS 选择算法，分配器稳定下来
with torch.cuda.graph(g):
    static_out = model.decode_step(static_input)   # 记录所有内核启动

# 之后，每次解码步骤仅需：
g.replay()   # 一次启动，重放数百个内核
```

其成本：SGLang 会为**多个批量大小**（1, 2, 4, 8, … 直到 `--cuda-graph-max-bs`）捕获图。每次捕获都会运行模型、分配静态 I/O 缓冲区，并让 cuBLAS/cuDNN 进行自动调优。这就是你 8.5 秒中的大部分时间。这是启动工作，而非首 token 生成工作——一旦捕获完成，解码步骤重放该图，启动开销便消失了（这是达到 17 毫秒的主要部分）。

### KV 缓存分配

SGLang 会提前预分配**整个 KV 缓存池**，而不是为每个请求进行 `malloc`。它会计算剩余 VRAM 可容纳多少 token，并预留一个巨大的连续块：

```
kv_bytes_per_token = 2 (K 和 V)
                   × num_layers (层数)
                   × num_kv_heads (KV 头数)          # GQA（分组查询注意力）→ 少于查询头数
                   × head_dim (头维度)
                   × dtype_size (数据类型大小)            # fp16/bf16 为 2 字节

total_tokens = floor(free_vram × mem_fraction / kv_bytes_per_token)
```

此块被划分为固定大小的**页面**（PagedAttention 风格）。首次分配会接触/预留所有这些页面——这是一次性的 CUDA 分配器成本。之后，服务请求只需从池中分配页面索引；热路径中无需分配。

### 基数树（RadixAttention）—— 为什么预热后 TTFT 为 17 毫秒

这是 SGLang 的标志性特性，也是为什么第二个请求如果共享前缀就能接近瞬时完成的原因。SGLang 将缓存的 KV 块存储在一个以 token 序列为键的**基数树**中。新请求会遍历该树；任何匹配的前缀都会被重用，而非重新计算。

```
请求 1: "You are a helpful assistant. Translate: hello"
请求 2: "You are a helpful assistant. Translate: world"
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 共享前缀
```

对于请求 2，系统提示词的 KV 已存在于树中——前缀填充阶段完全跳过它，只计算新的后缀 tokens。TTFT 缩减到一次短前缀填充加上通过 CUDA 图重放的首次解码步骤的成本 → 约 17 毫秒。

因此，三种成本对应关系清晰：

| 成本 | 何时发生 | 预热后为何消失 |
|------|----------|----------------|
| CUDA 图捕获 | 首次请求 | 图只记录一次，之后重放 |
| KV 缓存分配 | 首次请求 | 池只预分配一次，页面被重用 |
| 前缀重计算 | 每个请求 | RadixAttention 重用共享前缀的 KV |

8.5 秒降至 17 毫秒并非模型“变热”——而是所有静态基础设施（图 + 缓存池）在第一个请求时构建完成，第二个请求只需为真正的新 token 付费。

**参考文献：**

*   [SGLang RadixAttention 论文 (Zheng et al., 2023)](https://arxiv.org/abs/2312.07104)
*   [SGLang 文档 — 超参数调优与 CUDA 图](https://docs.sglang.ai/backend/hyperparameter_tuning.html)
*   [PyTorch CUDA 图](https://pytorch.org/blog/accelerating-pytorch-with-cuda-graphs/)
*   [vLLM PagedAttention（相同的 KV 分页思想）](https://arxiv.org/abs/2309.06180)