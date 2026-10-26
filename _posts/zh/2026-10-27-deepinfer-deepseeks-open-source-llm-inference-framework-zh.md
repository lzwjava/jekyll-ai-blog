---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepInfer：DeepSeek的开源LLM推理框架
translated: true
type: note
---

**DeepInfer 是 DeepSeek 的开源高性能 LLM 推理框架**——它是 DeepSeek-V4.1-Flash 生产服务背后的引擎，以精简但真实可用的系统形式发布，用于离线推理。它是一个 Python + C++（pybind11）技术栈：Python 负责模型/引擎编排，C++ 负责热路径调度，TileLang/CUDA/Ascend 内核负责计算，以及一组随附的 DeepSeek 内核库（FlashMLA、DeepGEMM、DeepEP、DeepSelect）作为 git 子模块。

本工作副本是公开发布版（提交日期为 2026‑10‑20/21，约 8.5 MB，342 个文件），对应 [README.md](README.md)。

![DeepSeek V4.1 Flash 推理系统架构](doc/images/architecture_overview.png)

## 它在生产体系中的位置

[部署问答](doc/inference_deployment_qa.md) 描述了完整的生产系统：**分离式 E/P/D 架构**（视觉编码器 / 预填充 / 解码）、用于解码的 Wide‑EP（EP64–128）、专用 3FS KV-cache 存储、四个负载均衡器（VE、prefill、decode、expert-parallel）、用于 API 编码/解码的 DeepSeek Recipe，以及 72 小时以上的 KV 保留。

本仓库实现了该图景中的**引擎核心**；README 明确说明以下内容*不*包含在内：

- KV cache 存储系统，
- 完整的 VE/Prefill/Decode 分离（大部分引擎钩子已具备），
- 数据并行副本负载均衡。

类似地，[llm_engine.py](deepinfer/engine/llm_engine.py#L140) 指出**没有在线服务封装**——这里面向用户的入口是离线 `LLM` 类。

## 请求流转流程

```
LLM.generate()                    deepinfer/entrypoints/llm.py
  └─ add_request() → Sequence     deepinfer/engine/llm_engine.py
      └─ C++ Scheduler            csrc/engine/scheduler.hpp
while unfinished:
  engine.step()                   deepinfer/engine/llm_engine.py#L860
    ├─ scheduler.schedule()       C++: prefix cache, chunked prefill, preemption,
    │                             block alloc, batch-invariant DP coordination
    ├─ _run_workers("execute_model_step")
    │    Worker.execute_model_step   deepinfer/worker/worker.py#L89
    │      1. forward current step (model runner, CUDA graphs)
    │      2. post-process *previous* step   ← overlap trick
    │      3. sample current step
    │      4. post-process current step (deferred in ZOS decode)
    └─ RequestOutput (pooled, zero-copy) → LLM clones them
```

调度器特意用 C++ 实现（`csrc/engine/scheduler.hpp`，包含块管理器、FLOPs 估算器、MTP 簿记），因此每步批量决策开销很低；Python 仅驱动循环（绑定接口见 [_C/engine.pyi](deepinfer/_C/engine.pyi)）。

## 主要子系统

| 领域 | 位置 | 功能 |
| :--- | :--- | :--- |
| 引擎 / 调度器 | [csrc/engine](csrc/engine), [deepinfer/engine](deepinfer/engine) | 迭代级调度、分块预填充、前缀缓存、抢占、KV 块池、**零开销异步调度** |
| Workers | [deepinfer/worker](deepinfer/worker) | 按 rank 的进程执行、CUDA graph 捕获、缓存引擎、ZOS 步骤状态、性能分析 |
| 模型执行器 | [deepinfer/model_executor](deepinfer/model_executor) | V4.1 模块——MLA/index attention、MoE、YoCo、Engram、HC 头；DFlash MTP draft；视觉编码器（ViT + aligner） |
| 内核 | [layers/tilelang_ops](deepinfer/model_executor/layers/tilelang_ops), [csrc](csrc), `vendor/` | TileLang 内核，带有独立的 `cuda/` 和 `asc/` 实现，以及随附的 FlashMLA/DeepGEMM/DeepEP |
| EPLB | [eplb](deepinfer/model_executor/eplb) | 冗余专家、负载统计、定期再平衡、在对称内存上的原地权重洗牌 |
| 结构化输出 | [structure_output](deepinfer/structure_output) | XGrammar 编译/匹配、token 掩码、异步编译线程池 |
| 多模态 | [ve](deepinfer/ve), [vision_encoder](deepinfer/model_executor/models/vision_encoder) | 图像预处理脱离关键路径、共享内存池、VL 元数据 |
| 集群 / 硬件 | [deep_cluster](deep_cluster) | 硬件无关的加速器发现（NVIDIA/Ascend/CPU）、NUMA/CPU 绑定 |
| 稳定 API 类型 | [sampling_params.py](deepinfer/sampling_params.py), [sequence.py](deepinfer/sequence.py), [config.py](deepinfer/config.py) | `SamplingParams`（包括 `so_args`、`seq_seed`）、序列、引擎配置 |
| 测试 / 示例 / 评估 | [tests](tests), [examples](examples/README.md), [eval](eval) | PPL 回归基线、批量不变性和采样器测试、离线 + 基准 + Pareto 扫描脚本 |

## 定义项目的特性

- **零开销批量调度（ZOS）** —— 最核心的优化，默认开启。`schedule(N+1)` 和对 `N-1` 的后处理与 GPU `forward(N) → sample(N)` 重叠，消除了空闲气泡。通过 [worker.py](deepinfer/worker/worker.py#L89) 中的延迟 `WorkerStepState` 流水线实现。
- **DSpark / 可变长度推测解码** —— MTP draft token（默认 5 个），置信度调度的验证，由 TileLang 内核在 GPU 上重新计算每个请求的长度。参见 [mtp/dflash.py](deepinfer/model_executor/models/mtp/dflash.py) 和 `DEEPINFER_ENABLE_MTP_VARLEN`。
- **SWA 有界重放 / YoCo** —— 解码器预填充仅重新计算有界的 128 token 后缀，而非数千个 token，使用 YoCo 截断模式（`DEEPINFER_YOCO_PREFILL_TRUNCATION_MODE=compact`）。参见 [yoco.py](deepinfer/model_executor/models/v4_modules/yoco.py)。
- **批量不变和确定性推理** —— `DEEPINFER_BATCH_INVARIANT=1` 使结果与批量组成无关；确定性采样将其与禁用 MTP 和固定 `seq_seed` 结合（仅限 NVIDIA）。
- **专家并行负载均衡** —— 热门专家在 GPU 间复制，并定期重新平衡；prefill（小 EP，激进再平衡）和 decode（Wide-EP，惰性再平衡）的设置不同。
- **结构化输出** —— 通过 XGrammar 实现 regex / JSON schema / EBNF 约束，通过 `SamplingParams(so_args=...)` 指定。
- **双硬件后端** —— 同一套 Python 代码面向 **NVIDIA SM100** 和 **Huawei Ascend 950**，由 `DEEPINFER_ACCELERATOR` 选择；`setup.py` 构建名为 `deepinfer._C` 的 `CUDAExtension` 或 `NpuExtension`。

## 构建与运行

Linux、Python 3.12、GCC ≥ 13，以及 CUDA 13 或 CANN 9.2（[README.md](README.md#L46)）：

```bash
export DEEPINFER_ACCELERATOR=nvidia    # or ascend
./build.sh                             # installs deps, builds vendor libs + extension
python examples/offline_inference.py --ep 8
python examples/benchmark.py           # throughput/latency, PROF=1 for traces
```

`examples/offline_inference.py` 默认下载 `deepseek-ai/DeepSeek-V4.1-Flash-1017`（或使用 `DEEPINFER_HF_MODEL_DIR`），运行一组固定提示，并打印解码 PPL 和推测解码接受率；[tests/models/offline_decode_ppl.json](tests/models/offline_decode_ppl.json) 存储每个平台/工作负载的 golden PPL 基线。配置几乎完全通过 [environ.py](deepinfer/environ.py) 以环境变量驱动，它实际上相当于一份特性索引，值得一读。

## 本检出版本的实际注意事项

- 它**无法在此直接运行**：`deepinfer._C` 二进制扩展未构建（仅存在 `.pyi` 存根），并且当前平台是 macOS，而代码面向 Linux + CUDA/CANN。
- `vendor/` 子模块（DeepEP、DeepGEMM、FlashMLA、DeepSelect 以及 Ascend 变体）**尚未初始化**——构建前请运行 `git submodule update --init --recursive`。
- 公开代码是服务引擎，而非完整服务：你需要自行提供 KV-cache 存储、请求路由/负载均衡以及 HTTP/API 层。

**一句话总结：** DeepInfer 是面向 DeepSeek-V4.1-Flash 的生产级、双厂商推理引擎，其有趣之处在于带有零开销异步重叠的 C++ 迭代级调度器、具备专家负载均衡和推测解码的 EP/MoE 感知执行、有界 SWA 重计算，以及深度内核优化的模型运行时——开源版去掉了构成完整云服务的基础设施粘合层。