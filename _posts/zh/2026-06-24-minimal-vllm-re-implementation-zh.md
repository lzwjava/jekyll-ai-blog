---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最小化vLLM重实现
translated: true
type: note
---

以下是 nano-vllm 的介绍：

---

## nano-vllm — 一个极简的 vLLM 重实现

这是一个**从零开始、约 1200 行 Python 代码重实现的 vLLM**——高吞吐量 LLM 推理引擎。作者：Xingkai Yu。MIT 许可证。当前目标为 **Qwen3** 模型。

目标：展示 vLLM 的核心思想（PagedAttention、continuous batching、prefix caching、CUDA graphs、tensor parallelism）可以在一个小巧、可读的代码库中干净地实现——并且仍能达到与真实 vLLM 相当的吞吐量。

---

## 架构（6 个关键组件）

### 1. LLMEngine（engine/llm_engine.py）— 编排器
- 拥有 Scheduler、ModelRunner 和 Tokenizer
- `generate()` 循环：添加请求 → 逐步执行直到完成，报告 prefill/decode 吞吐量
- `step()`：调度器选择序列 → model_runner 执行前向 → 调度器后处理 token
- 通过 `torch.multiprocessing.spawn` 支持 tensor parallelism——rank 0 驱动，rank 1..N 运行一个共享内存事件循环

### 2. Scheduler（engine/scheduler.py）— 连续批处理
- 两个队列：`waiting`（prefill）和 `running`（decode）
- Prefill 调度：遵守 `max_num_batched_tokens` 和 `max_num_seqs`，支持第一个序列的 chunked prefill
- Decode 调度：当 KV 缓存满时驱逐（抢占）正在运行的序列——经典的 vLLM 抢占
- 后处理：追加生成的 token，检查 EOS/max_tokens，释放已完成的序列

### 3. BlockManager（engine/block_manager.py）— PagedAttention KV 缓存
- **这是 vLLM 的核心创新**，在此重新实现
- 从池中分配的固定大小 KV 缓存块（默认 256 token/块）
- `Block` 对象跟踪 `ref_count` 和 `hash`，用于 prefix caching
- `allocate()`：找到已缓存的 prefix 块（hash 匹配），仅为剩余部分分配新块
- `hash_blocks()`：基于 xxhash 的 token 块哈希，实现自动 prefix 缓存
- 抢占：释放块，将序列放回 waiting 队列

### 4. ModelRunner（engine/model_runner.py）— GPU 执行
- 通过 safetensors 加载 Qwen3 模型权重，包含打包模块映射（q/k/v → 融合 qkv_proj，gate/up → 融合 gate_up_proj）
- 分配单个连续 KV 缓存张量：`[2, num_layers, num_blocks, block_size, num_kv_heads, head_dim]`
- **解码时的 CUDA Graph 捕获**：在批大小 [1,2,4,8,16,32,...,512] 下预捕获图，实现零开销重放
- Warmup 阶段测量峰值内存，然后计算剩余 GPU 内存能容纳多少个 KV 缓存块
- 通过 NCCL + SharedMemory IPC 实现 tensor parallelism

### 5. Attention（layers/attention.py）— FlashAttention + Triton KV 存储
- **Triton 内核** `store_kvcache_kernel`：使用 slot_mapping 将 K/V 写入分页缓存（无 Python 循环）
- Prefill：`flash_attn_varlen_func`，支持变长序列和可选的 block_table 用于 prefix 缓存
- Decode：`flash_attn_with_kvcache`，使用分页 KV 缓存

### 6. Model（models/qwen3.py）— Qwen3ForCausalLM
- 完整的 Qwen3 变换器：QKV 并行线性层、RoPE（使用 `@torch.compile`）、QK-norm（Q/K head 上的 RMSNorm）、SiLU 门控 MLP
- `ParallelLMHead`：词汇并行输出——仅在 rank 0 上跨 TP rank 收集 logits
- 权重加载处理打包模块（融合 QKV、融合 gate/up）

### 辅助层
- **RotaryEmbedding**：预计算的 cos/sin 缓存，前向使用 `@torch.compile`
- **RMSNorm**：融合 add+norm 变体用于残差连接，`@torch.compile`
- **SiluAndMul**：在 SiLU 门控上使用 `@torch.compile`
- **Sampler**：`@torch.compile`，使用 Gumbel-max 技巧进行采样（指数噪声 + argmax）

### 关键设计选择
- **禁止贪婪采样**（强制 `temperature > 1e-10`）——仅随机采样
- 块大小必须是 256 的倍数
- 默认 GPU 内存使用率 90%
- `enforce_eager=True` 禁用 CUDA graphs（用于调试）

---

## 基准测试（来自 README）

RTX 4070 笔记本，Qwen3-0.6B，256 个序列，100-1024 输入/输出 token：

| 引擎      | Token 数  | 时间   | 吞吐量       |
|-----------|-----------|--------|--------------|
| vLLM      | 133,966   | 98.37s | 1361 tok/s   |
| nano-vllm | 133,966   | 93.41s | 1434 tok/s   |

在该工作负载上基本与 vLLM 持平或略有超越——而代码量只有其 1/100。

---

## 总结

这是一个**教学质量的 vLLM 克隆**，在约 1200 行代码中实现了 PagedAttention + continuous batching + prefix caching + CUDA graphs + tensor parallelism。是理解 vLLM 底层工作原理的绝佳参考。当前仅支持 Qwen3（硬编码的模型类）。