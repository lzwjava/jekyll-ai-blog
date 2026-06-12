---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nano-vLLM 最小化vLLM重新实现
translated: true
type: note
---

以下是 nano-vllm 的介绍：

---

## nano-vllm — vLLM 的最小化复现

这是一个**从头实现、约1200行Python代码的vLLM复现版本**——vLLM是高吞吐量LLM推理引擎。作者：于兴凯。采用MIT许可证。当前目标为**Qwen3**模型。

目标：展示vLLM的核心思想（PagedAttention、连续批处理、前缀缓存、CUDA图、张量并行）可以用简洁可读的少量代码实现，并且仍能达到与真实vLLM相当的吞吐量。

---

## 架构（6个关键组件）

### 1. LLMEngine（engine/llm_engine.py）——调度器

- 拥有调度器、模型运行器和分词器
- `generate()`循环：添加请求→逐步执行直至完成，报告预填充/解码吞吐量
- `step()`：调度器选择序列→模型运行器执行前向传播→调度器后处理令牌
- 通过`torch.multiprocessing.spawn`支持张量并行——rank 0驱动，rank 1至N运行共享内存事件循环

### 2. 调度器（engine/scheduler.py）——连续批处理

- 两个队列：`waiting`（预填充）和`running`（解码）
- 预填充调度：遵守`max_num_batched_tokens`和`max_num_seqs`，支持首个序列的分块预填充
- 解码调度：当KV缓存满时驱逐（抢占）运行中的序列——经典的vLLM抢占机制
- 后处理：追加生成的令牌，检查EOS/最大令牌数，释放完成的序列

### 3. 块管理器（engine/block_manager.py）——PagedAttention KV缓存

- **这是vLLM的核心创新**，在此重新实现
- 从池中分配固定大小的KV缓存块（默认256个令牌/块）
- `Block`对象跟踪`ref_count`和`hash`以实现前缀缓存
- `allocate()`：查找缓存的前缀块（哈希匹配），仅分配剩余部分的新块
- `hash_blocks()`：基于xxhash的令牌块哈希，实现自动前缀缓存
- 抢占：释放块，将序列放回等待队列

### 4. 模型运行器（engine/model_runner.py）——GPU执行

- 通过safetensors加载Qwen3模型权重，支持打包模块映射（q/k/v→融合qkv_proj，gate/up→融合gate_up_proj）
- 分配单个连续的KV缓存张量：`[2, num_layers, num_blocks, block_size, num_kv_heads, head_dim]`
- **解码的CUDA图捕获**：在批大小[1,2,4,8,16,32,…,512]上预捕获图，实现零开销重放
- 预热阶段测量峰值内存，然后计算剩余GPU内存可容纳的KV缓存块数
- 通过NCCL+共享内存IPC实现张量并行

### 5. 注意力机制（layers/attention.py）——FlashAttention + Triton KV存储

- **Triton内核**`store_kvcache_kernel`：使用slot_mapping将K/V写入分页缓存（无Python循环）
- 预填充：`flash_attn_varlen_func`，支持变长序列和可选的block_table用于前缀缓存
- 解码：`flash_attn_with_kvcache`，使用分页KV缓存

### 6. 模型（models/qwen3.py）——Qwen3ForCausalLM

- 完整Qwen3 transformer：QKV并行线性层、RoPE（配合`@torch.compile`）、QK归一化（Q/K头的RMSNorm）、SiLU门控MLP
- `ParallelLMHead`：词汇并行输出——仅在rank 0上跨TP排名收集logits
- 权重加载处理打包模块（融合QKV、融合gate/up）

### 辅助层

- **RotaryEmbedding**：预计算的cos/sin缓存，前向传播使用`@torch.compile`
- **RMSNorm**：残差连接的融合加法+归一化变体，`@torch.compile`
- **SiluAndMul**：SiLU门控上的`@torch.compile`
- **采样器**：`@torch.compile`，用于采样的Gumbel-max技巧（指数噪声+argmax）

### 关键设计选择

- **禁止贪心采样**（强制`temperature > 1e-10`）——仅随机采样
- 块大小必须是256的倍数
- 默认90% GPU内存利用率
- `enforce_eager=True`禁用CUDA图（用于调试）

---

## 基准测试（来自README）

RTX 4070笔记本电脑，Qwen3-0.6B，256个序列，100-1024输入/输出令牌：

| 引擎       | 令牌数   | 时间   | 吞吐量       |
|-----------|----------|--------|--------------|
| vLLM      | 133,966  | 98.37秒 | 1361 tok/秒 |
| nano-vllm | 133,966  | 93.41秒 | 1434 tok/秒 |

在此工作负载上基本与vLLM持平甚至略优——而代码量减少100倍。

---

## 总结

这是一个**教学级vLLM克隆**，用约1200行代码实现了PagedAttention、连续批处理、前缀缓存、CUDA图和张量并行。是理解vLLM底层工作原理的优秀参考。当前仅支持Qwen3（硬编码模型类）。
