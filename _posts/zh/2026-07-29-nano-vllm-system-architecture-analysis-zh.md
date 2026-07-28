---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nano-vLLM系统架构分析
translated: true
type: note
---

现在我对整个系统有了透彻的理解。以下是我的分析：

---

## Nano-vLLM 的工作原理

Nano-vLLM 是一个**轻量级生产推理引擎**（不是训练/单次推理框架）。它用约 1200 行可读的 Python 代码实现了 vLLM（一个高吞吐量 LLM 服务系统）的核心架构。其架构如下：

### 1. 架构概览

```
LLM（面向用户的 API）
 └─ LLMEngine
     ├─ ModelRunner（加载模型，执行前向传播）
     ├─ Scheduler（管理批处理 + 调度）
     ├─ BlockManager（分页 KV 缓存，支持前缀缓存）
     └─ Sequence（追踪每个请求的状态）
```

### 2. 核心组件

**调度器** (`scheduler.py`)：系统的心脏。它有两种模式：
- **Prefill（首次计算）**：处理提示词 token。支持*分块预填充*——如果提示词过长，会被拆分成多个步骤。
- **Decode（自回归生成）**：每个步骤每个序列产生一个 token。如果 KV 缓存耗尽，它会*抢占*序列（释放其缓存，将其移回等待队列）。

**分页 KV 缓存** (`block_manager.py`)：每个序列不再使用整体 KV 缓存，而是将 KV 缓存拆分为固定大小的**块**（每个块 256 个 token）。`BlockManager` 维护：
- 一个空闲块列表
- 一个从内容哈希到块 ID 的哈希表，用于**前缀缓存**（共享公共前缀）
- 块共享的引用计数（写时复制语义）

**带分页缓存的注意力机制** (`attention.py`)：自定义注意力，执行以下操作：
- 通过 `slot_mapping` 将计算出的 K/V 条目存入分页缓存
- 在带前缀缓存的预填充阶段，*收集*来自分页缓存的缓存 K/V，并与新计算的 K/V 拼接
- 在解码阶段，在调用 `scaled_dot_product_attention` 之前，从分页块中收集所有缓存的 K/V

**张量并行** (`linear.py`, `embed_head.py`)：使用 NCCL 将 QKV 投影、嵌入层和 LM head 分片到多个 GPU 上。对行并行层使用 `all_reduce`，对 LM head 输出使用 `gather`。

**CUDA Graphs** (`model_runner.py`)：将解码迭代捕获到 CUDA graphs 中，使单 token 生成速度提升约 10-30%。当批量大小较大（>512 个序列）或处于预填充阶段时，会回退到 eager 模式。

**采样器** (`sampler.py`)：使用 Gumbel-max 技巧的温度缩放随机采样：`argmax(softmax(logits / T) / exp(1))`。

### 3. 请求的生命周期

```
generate(prompts)
  ├─ add_request() -> 创建 Sequence，添加到等待队列
  └─ while not is_finished():
        step()
          ├─ scheduler.schedule() -> 选择用于预填充/解码的序列
          ├─ model_runner.run(seqs, is_prefill)
          │     ├─ prepare_inputs() -> 构建 input_ids, positions, block tables, slot mappings
          │     ├─ model.forward(input_ids, positions) -> 隐藏状态
          │     │     └─ 每层：attn + MLP（带分页 K/V 存储/加载）
          │     └─ lm_head(hidden_states) -> logits
          └─ scheduler.postprocess() -> 追加 token，检测 EOS
```

---

## 与普通 nanoGPT 推理的差异

### 1. **批处理（连续批处理）**

| nanoGPT | Nano-vLLM |
|---------|-----------|
| 每次处理单个序列 | **多个序列被批处理在一起** |
| 固定批次（所有序列长度相同） | **变长序列动态调度** |
| 无调度开销 | 调度器决定每个步骤运行哪些序列 |

### 2. **内存管理：分页 KV 缓存 vs 整体缓存**

| nanoGPT | Nano-vLLM |
|---------|-----------|
| 每个序列分配 `max_seq_len × num_layers × ...`（浪费） | **按需分配分页块**，无需预分配 |
| 序列之间无共享 | **前缀缓存**：相同的提示词前缀共享 KV 块（通过 xxhash 检测） |
| KV 缓存碎片化 | 由于分页，**无碎片化** |
| 长序列时 OOM | 块优雅地逐出/抢占 |

### 3. **预填充与解码分离**

| nanoGPT | Nano-vLLM |
|---------|-----------|
| 单次前向传播，无区分 | 两个不同的阶段：**预填充**（计算密集，批处理所有提示词 token）和**解码**（内存受限，每序列 1 个 token） |
| 无分块 | **分块预填充**：将超长提示词拆分为多个步骤，避免 GPU OOM |

### 4. **nanoGPT 中缺失的优化**

| 特性 | 作用 |
|---------|-------------|
| **张量并行** | 将模型分片到多个 GPU 上（QKV 拆分，all-reduce） |
| **CUDA Graphs** | 将解码内核启动捕获到可重用的 graph 中，减少 CPU 启动开销 |
| **前缀缓存** | 基于内容的哈希匹配，在具有共享前缀的请求之间重用 KV 缓存块（例如系统提示词） |
| **抢占** | 如果 KV 缓存已满，调度器将正在运行的序列踢出（释放块）并稍后重新调度 |
| **变长批处理 CUDA Graphs** | 预先捕获批量大小 `[1, 2, 4, 8, 16, 32, ... 512]` 的 graph，并选择最接近的一个 |

### 5. **吞吐量导向**
- nanoGPT 的 `sample.py` 推理设计用于**单样本生成**，优先考虑简单性
- Nano-vLLM 设计用于**高吞吐量服务**：基准测试显示在笔记本电脑 RTX 4070 上约 1434 tok/s，与 vLLM 本身匹配/超越

### 6. **架构支持**
- Nano-vLLM 当前具体实现了 **Qwen3** 模型架构
- nanoGPT 支持原始 GPT-2 small/medium/large
- Nano-vLLM 支持现代特性，如 GQA（分组查询注意力）、RoPE（旋转位置编码）、QKV bias、QK-Norm 等

### 7. **采样**
- Nano-vLLM 仅支持**基于温度的随机采样**（无 top-k、top-p 或贪婪采样）
- nanoGPT 支持温度、top-k 和 top-p 采样

简而言之：**nanoGPT** ≈ 单序列推理测试平台；**Nano-vLLM** ≈ 一个完整的生产级推理引擎，实现了与 vLLM 相同的调度、缓存和并行技术，只是代码库更简洁、更小。