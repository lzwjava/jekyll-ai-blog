---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 架构概述
translated: true
type: note
---

我现在有了一个全面的了解。以下是 SGLang 代码库的架构概述。

---

# SGLang — 架构概述

**SGLang** 是一个面向 LLM/多模态模型的高性能服务框架，支持从单 GPU 到大规模集群的部署。它为生产环境中的部署提供支持（如 DeepSeek V3/V4、Llama、Qwen 等）。该代码库是一个 **Python + Rust 混合系统**（约 5,200 个 Python 文件，Rust 服务核心）。

## 顶层结构

| 目录 | 角色 |
| --- | --- |
| `python/sglang/lang/` | **前端 DSL** — 使用 `@function` 装饰的 Python 程序，编译为中间表示（`ir.py`、`tracer.py`），并通过解释器（`interpreter.py`）在可插拔后端（`backend/`：OpenAI、运行时端点等）上执行 |
| `python/sglang/srt/` | **SRT（SGLang Runtime）** — 核心服务引擎 |
| `rust/sglang-server/` | **Rust 服务核心** — API 服务器（axum）、分词器/逆分词器、分词器管理器环；通过 pyo3 嵌入 |
| `rust/sglang-grpc/` | Rust gRPC 服务器 + 连接到 Python 调度器的 pyo3 桥接 |
| `rust/sglang-mm/` | 多模态（图像/音频/视频）处理服务器（"inkling"） |
| `proto/sglang/runtime/v1/` | gRPC 协议（`SglangService`：类型化 + OpenAI 兼容 + 管理 RPC） |
| `sgl-model-gateway/` | 模型网关（Rust），路由器/前端 |
| `benchmark/`、`examples/`、`test/`、`docs_new/` | 基准测试、示例、测试、文档 |

## 运行时核心（`python/sglang/srt/`）

```
┌─────────────┐   ┌───────────────────────┐   ┌──────────────────────────────┐
│ entrypoints │──▶│ TokenizerManager      │──▶│ Scheduler ──▶ TpWorker/      │
│ (HTTP/gRPC/ │   │ (请求接收、            │   │ (事件循环、批处理            │
│  engine)    │   │  逆分词、输出)         │   │  规划、缓存管理)             │
└─────────────┘   └───────────────────────┘   └──────────────────────────────┘
                                                       │
                                     ┌─────────────────┼──────────────────┐
                                     ▼                 ▼                  ▼
                              model_runner/      mem_cache/          layers/
                              (CUDA graphs、    (Radix tree KV        (注意力
                               forward、sampler)  缓存、内存池)       后端、MoE 等)
```

**请求流程：** HTTP/gRPC 入口点（`entrypoints/http_server.py`、`grpc_server.py`、`engine.py` 用于离线使用）→ `TokenizerManager`（管理每个请求的状态、分词、逆分词、流式传输）→ 通过请求接收器到 `Scheduler`。

**`Scheduler`**（`managers/scheduler.py`，约 4,850 行）是核心：

- 单线程事件循环（`event_loop_normal` / `event_loop_overlap`），持续执行：接收请求 → 规划下一批次 → 启动 GPU 前向传播 → 处理结果。
- **CPU/GPU 重叠**：调度器在单独的 CUDA 流（`schedule_stream`）上运行，使下一批次的规划与当前前向传播重叠；WAR 屏障（`_apply_war_barrier`）用于保护共享缓冲区的写入。
- 通过可插拔的 **`SchedulePolicy`**（`schedule_policy.py`：FCFS、最长前缀优先等）进行调度。
- 分解为 **`scheduler_components/`** — 请求接收器、输出发送器/流式处理器、指标报告器、空闲休眠器、权重更新器、IPC 通道、不变性检查器等。
- 支持 **prefill–decode 分离**（`disaggregation/`：通过 Mooncake/etcd 进行交换 KV 的独立 prefill/decode 进程）、**DP attention**、**推测解码**（`speculative/`）、**LoRA**（`lora/`）、**弹性 EP**（`elastic_ep/`）以及多模态（`multimodal/`、`managers/mm_utils.py`）。

**`TpWorker`**（`managers/tp_worker.py`）驱动实际的 GPU 工作：`model_runner.py` + `runner/`（eager、CUDA-graph 解码/预填充运行器、flashinfer 自动调优）+ `layers/` — 注意力机制拥有 **20 多种后端实现**（flashinfer、flash-attention、Triton、torch-native、MLA 变体、稀疏/混合/NSA 等），以及 MoE 内核（deep_gemm、eplb）。

**`mem_cache/`** — 内存管理：**RadixAttention**（`radix_cache.py`，层次化 radix-tree 前缀缓存，实现跨请求的自动复用）、统一内存池/分配器、块缓存、mamba 池、HiCache 混合卸载、淘汰策略以及 C++ radix tree 绑定。

**`distributed/`** — 张量/流水线/数据并行（`parallel_state.py`、NCCL 设备通信器、引导程序），由 `connector/`（例如 DeepSeek 连接器）、`eplb/`（专家并行负载均衡）使用。

**`hardware_backend/`** — GPU/CPU/NPU/XPU/MLX/MUSA 抽象；`platforms/` 用于各加速器检测。**`constrained/`** — 结构化输出：xgrammar/llguidance/outlines 语法后端，带有压缩 FSM 推理器。**`checkpoint_engine/`**、**`model_loader/`**、**`weight_cache/`** — 模型加载与权重管理。**`tokenizer/`**、`configs/`、`arg_groups/` — 分词器 + 类型化配置组。**`observability/`**、`plugins/`、`state_capturer/`、`compilation/`（torch.compile）、`dllm/`（分离式长 LLM）。

## Rust 服务核心（`rust/sglang-server/`）

前端的性能关键重写，**通过 pyo3 嵌入 Python**（`cdylib`）：

- **线程布局**：axum API 服务器（tokio，核心集合 A）→ 分词器（固定的 OS 线程，集合 B）→ 逆分词器（分片，集合 C）→ TM 入口/出口（环形缓冲区，`ring.rs`）。
- `api_server/` — `openai.rs`、`native_api.rs`、`submit.rs`、流式传输帧。
- `tokenizer_manager/{ingress,egress}.rs` — 驱动请求接收/输出的 FSM；Python 的 `TokenizerManager` 清空入口 / 跨 FFI 边界推送批次。
- `runtime.rs` 引导所有组件；`request_shutdown` 使用有界 join 中止进行中的工作。
- `sglang-grpc/` — Rust gRPC 服务程序，其 `RuntimeHandle` 回调 Python 的调度器（`grpc_bridge.py`）；编译为 `sglang/srt/grpc/_core.so`。

## 进程拓扑

- **单进程**：调度器 + GPU 工作器 + 分词器管理器；Rust 服务器在同一进程中运行，使分词/逆分词/HTTP 操作脱离 Python GIL。
- **分布式**：多个调度器进程通过 Redis/NATS（分离用的 etcd）、用于 PD 分离的 gRPC KV 传输、用于集群启动的 Ray 以及用于路由/负载均衡的 `sgl-model-gateway` 进行协调。

## 关键架构理念

1. **RadixAttention** — 前缀缓存作为核心优化；所有 KV 内存都采用树状结构并在请求之间共享。
2. **零开销连续批处理** — 紧密的调度器循环与 CPU/GPU 重叠；批处理是默认模式，而非特殊模式。
3. **prefill–decode 分离** — 分离 prefill（计算密集型）和 decode（内存密集型）池，并在两者之间传输 KV 缓存。
4. **处处可插拔** — 注意力后端、调度策略、语法后端、硬件平台、模型实现（`models/` 包含约 150 多种模型类）以及运行器后端均基于注册表/类实现。
5. **前端/后端分离** — `lang` DSL 与任何运行时解耦；后端（`runtime_endpoint.py`、OpenAI 等）均可互换。

最近的提交显示正在积极开发 Rust 服务器（TCP TTFT 延迟问题）、量化内核以及运行时上下文配置重构，旨在实施按角色命名空间强制执行。
