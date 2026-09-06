---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式推测解码代码库
translated: true
type: note
---

以下是代码库的导览：

## 架构概览

```
src/bloombee/
├── cli/            → 入口点（run_server.py, run_dht.py）
├── client/         → 面向用户的远程推理API
├── server/         → 托管transformer层的对等节点
├── models/         → 模型适配器（llama, qwen3, mixtral, falcon, gemma4, bloom + 模板）
├── utils/          → 传输、微批处理、量化、P2P粘合
└── flexgen_utils/  → 张量卸载支持（FlexGen风格）

### 1. 服务端（`server/`）—— 托管层的对等节点
- **`server.py` / `backend.py` / `handler.py`** —— 核心逻辑：每个对等节点加载连续的transformer块切片，并通过DHT提供 `forward`、`backward` 和 `inference`（KV缓存步骤）请求服务。
- **`block_functions.py`** —— 服务端块计算；处理序列化、无损压缩和微批切片。
- **`microbatch.py`** —— 微批流水线（计算与通信重叠）。
- **`paged_kv.py`、`memory_cache.py`、`memory_cache_manager.py`** —— 跨阶段的KV缓存管理。
- **`flexgen_tensor_parallel.py`** —— 张量卸载，使单个GPU可承载更多层。

### 2. 推测解码（`server/speculative_pruner/`）—— 最有趣的部分
基于 `PrunerInterface`（抽象基类）的可插拔策略系统。在推测解码过程中，对等节点每次往返发送一个*草稿token树*；修枝器决定在网络其余部分遍历之前保留哪些分支：
- `simple_probability_pruner.py` —— 基于概率的修枝
- `adaptive_neural_pruner.py` —— 可学习的修枝器
- `mid_layer_LM_head.py` + `lm_head_trainer.py` —— 附加在网络中间的轻量级LM头，用于提前评分草稿
- `pruner_manager.py` / `pruner_factory.py` —— 连接与选择

### 3. 客户端（`client/`）
- `remote_sequential.py` —— 将整个P2P网络视为一个 `nn.Sequential`（通过 `sequential_autograd.py` 实现网络内的自动求导）
- `remote_generation.py` / `inference_session.py` —— token生成，在跨跳过程中维护会话
- `routing/` —— 基于DHT的发现机制，用于定位托管各层的对等节点

### 4. 传输层（`utils/lossless_transport.py`、`s2s_activation_quant.py`）
无损激活压缩层 —— 在对等节点之间序列化/反序列化张量，跟踪压缩比和性能分析（`log_comp_ratio_event`、`transport_profile`）。

**典型请求流程：** 客户端 → 通过DHT发现托管层的对等节点 → 发送隐藏状态（压缩后）→ 每个对等节点运行其切片 + 修枝推测解码分支 → 将激活值传递给下一个对等节点 → 最终对等节点运行LM头 → token流式返回。

需要我深入探讨某个部分吗？例如自适应神经修枝器的工作原理，或微批流水线逻辑。
