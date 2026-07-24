---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nano-vLLM 架构与性能
translated: true
type: note
---

以下是 **Nano-vLLM** 的全面介绍：

---

## 什么是 Nano-vLLM？

**Nano-vLLM** 是对 [vLLM](https://github.com/vllm-project/vllm)（一个高性能 LLM 推理引擎）的轻量级、从零开始的重新实现。它用 **约 1,200 行 Python 代码** 实现了 **与 vLLM 相当的吞吐量**（在基准测试中甚至略快），是了解现代 LLM 推理引擎内部运作原理的极佳学习资源。

---

## 架构概览

项目按以下层次组织：

```
nanovllm/
├── llm.py              # 入口点（继承 LLMEngine）
├── config.py            # 配置数据类
├── sampling_params.py   # 采样参数（temperature, max_tokens）
├── engine/
│   ├── llm_engine.py    # 主要编排循环（generate, step）
│   ├── scheduler.py     # 批处理与调度逻辑
│   ├── model_runner.py  # GPU 模型执行、KV 缓存、CUDA graphs
│   ├── sequence.py      # 请求/序列状态跟踪
│   └── block_manager.py # KV 缓存块分配与前缀缓存
├── models/
│   └── qwen3.py         # Qwen3 模型定义（transformer 层）
├── layers/
│   ├── attention.py     # FlashAttention 封装 + 自定义 KV 缓存 Triton 内核
│   ├── linear.py        # 张量并行线性层
│   ├── embed_head.py    # 支持张量并行的嵌入层与 LM 头
│   ├── sampler.py       # 温度缩放采样（torch.compiled）
│   ├── activation.py    # SiLU 激活函数
│   ├── layernorm.py     # RMSNorm
│   └── rotary_embedding.py  # RoPE
└── utils/
    ├── context.py       # 线程局部上下文（prefill/decode 元数据）
    └── loader.py        # 支持张量并行分片的 Safetensors 权重加载器
```

---

## 关键特性

### 1. **连续批处理**（`scheduler.py`）
与 vLLM 类似，Nano-vLLM 使用 **迭代级调度**——每步之后，调度器决定处理哪些序列：
- **Prefill 阶段**：处理新序列的提示词 token，支持 **分块预填充**（部分提示词处理）以最优填充批次。
- **Decode 阶段**：为批次中每个活跃序列生成一个 token。
- **抢占**：当 KV 缓存不足时，运行中的序列被驱逐回等待队列（其块被释放）。

### 2. **分页 KV 缓存**（`block_manager.py`, `model_runner.py`）
KV 缓存被划分为固定大小的 **块**（默认每个块 256 个 token），由 `BlockManager` 管理：
- **动态分配**：块按需分配，随着序列增长而分配。
- **前缀缓存**（`hash_blocks` / `can_allocate`）：使用 **xxhash** 计算 token 块的哈希值。当新请求与之前请求共享公共前缀时，缓存的 KV 块被 **重用**（引用计数），避免重复计算。

### 3. **张量并行**（`linear.py`, `embed_head.py`）
支持将模型层拆分到多个 GPU：
- `QKVParallelLinear`、`MergedColumnParallelLinear`、`RowParallelLinear`——沿隐藏/注意力头维度分片权重。
- `VocabParallelEmbedding` / `ParallelLMHead`——通过 `all_reduce` / `all_gather` 在 GPU 间分布词汇表。
- 使用 `torch.multiprocessing` 的多进程设置，通过共享内存（`SharedMemory`）进行进程间通信。

### 4. **FlashAttention 集成**（`attention.py`）
使用 `flash-attn` 库进行预填充（`flash_attn_varlen_func`）和解码（`flash_attn_with_kvcache`）。一个自定义 **Triton 内核**（`store_kvcache_kernel`）高效地将 KV 缓存条目写入分页缓存块。

### 5. **CUDA Graph 捕获**（`model_runner.py`）
对于 **解码** 步骤（操作大小固定），CUDA graphs 捕获整个模型前向传播，消除了 Python 和 CUDA 启动开销。当 `enforce_eager=True` 时禁用。

### 6. **Torch 编译的采样器**（`sampler.py`）
采样步骤使用 `@torch.compile` 实现更快的 top-k 风格采样，并带有温度缩放。

---

## 性能

在 RTX 4070 笔记本（8GB）上，使用 Qwen3-0.6B（256 个序列）：

| 引擎       | 吞吐量 (tok/s) |
|------------|----------------|
| vLLM       | 1,361.84       |
| Nano-vLLM  | **1,434.13**   |

---

## 端到端工作原理

1. **用户调用** `llm.generate(prompts, sampling_params)`。
2. **请求被排队** 为 `Sequence` 对象。
3. **调度器** 决定每次迭代运行哪些序列（预填充或解码）。
4. **ModelRunner** 准备输入（token ID、位置、槽映射、块表），运行模型，并采样输出 token。
5. **结果** 被收集并解码回文本。

这是一个极好的资源，适合任何想要深入了解 LLM 推理内部机制的人——批处理、KV 缓存管理、前缀缓存、张量并行和 GPU 优化技术——全部以可读、自包含的代码呈现。