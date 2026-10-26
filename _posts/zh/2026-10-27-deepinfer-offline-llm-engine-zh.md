---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepInfer：离线大语言模型引擎
translated: true
type: note
---

以下是 **DeepInfer** 的简介：

## 概览

**DeepInfer** 是 DeepSeek 的 **high-performance LLM inference engine**，用于在生产环境中 serving DeepSeek 模型，已开源（Apache 2.0）。本次发布仅为 **offline inference** — 通过 Python API 进行 batch generation — 包含大规模 serving 所需的核心机制，但不包含 online serving 组件（KV cache system、disaggregation infra、load balancing）。

它是 **vLLM** 的一个 fork/衍生项目（代码注释中明确说明："Derived from vLLM; modified by DeepSeek"），并借鉴了 SGLang 和 TensorRT-LLM 的思路。

## 关键信息

- **目标模型：** DeepSeek-V4.1-Flash（默认 checkpoint `deepseek-ai/DeepSeek-V4.1-Flash-1017`）
- **硬件：** NVIDIA SM100 (Blackwell) GPU 和华为 Ascend 950 NPU
- **规模：** 约 46K 行 Python + 约 6K 行 C++（外加 vendored kernels）
- **技术栈：** PyTorch 2.7+ / CUDA 13 / CANN 9.2，GCC ≥ 13，Python 3.12
- **状态：** Beta，非常新的仓库 — 仅 4 个提交（初始提交 + 文档/版本更新）

## 架构

**Python 核心**（`deepinfer/`）：

- `engine/llm_engine.py`（约 1K 行）— 编排器：scheduler loop、request lifecycle、batch processing、async (zero-overhead) scheduling、stats、profiling
- `worker/` — `model_runner.py`、`worker.py`、`cache_engine.py`，以及用于 prefill/decode 的 **CUDA graph runners** 和一个 flash-decoding graph runner
- `model_executor/models/deepseek.py` — 模型本身，由 V4 模块构建：MoE MLP、MTP (multi-token prediction)、**DFlash** draft model、**Engram** (ngram matching)、**HC** (hybrid-cross? attention/heads)、YOCO cross-layers，以及 multimodal embedding 支持
- `model_executor/layers/` — sampler、attention backends、tilelang_ops（自定义 TileLang kernels）

**C++ 引擎**（`csrc/engine/`）— hot path，通过 pybind11 暴露：

- `scheduler.hpp` — zero-overhead batch scheduler、block manager、flops estimator
- `prepare_sample.cpp` / `mtp_varlen.hpp` — sampling prep 和 MTP variable-length verification
- `zos.cpp`（ZOS status）、sequence/request-output 处理

**Vendored kernels**（git submodules）：FlashMLA、DeepGEMM、DeepEP、DeepSelect、TileKernels，以及 Ascend 变体 — 外加一个类似 Triton 的自定义 TileLang op 集合。

## 显著特性

- **Parallelism：** attention DP / balanced CP，MoE **EP with EPLB**（expert-parallel load balancing）
- **DSpark / confidence-scheduled verification** — 通过 confidence-gated verification 实现 draft-token 加速（环境变量 `DEEPINFER_ENABLE_MTP_VARLEN=1`）
- **SWA bounded replay** — 将 decoder prefill 截断为有界后缀（`DEEPINFER_YOCO_PREFILL_*` 环境变量）
- **Batch-invariant inference & deterministic sampling** — 无论 batch 组成如何，结果一致
- **Structured outputs** — regex / JSON schema / EBNF grammar 约束生成
- **默认启用 Async scheduling**，将 CPU scheduling 与 GPU execution 重叠

## 配套组件

- `eval/` — 离线 benchmark harness，支持 AIME 2026、HLE（包括图像任务）、GPQA Diamond；分离的 generate-then-score 阶段，报告 Pass@1
- `examples/` — offline inference、benchmarks、sweeps、YOCO tests
- `build.sh` / `setup.py` — 构建 CUDA/NPU 扩展（`DEEPINFER_ACCELERATOR=nvidia|ascend`）
- Vendored `deep_cluster` 包，用于 hardware-aware tuning（bf16 TFLOPS limits）

**总结：** 这是 DeepSeek 经过实战检验的生产级 inference stack，精简为面向 offline、batch 的 API，并作为 reference/serving infrastructure 发布 — 大量使用自定义 kernels 和 C++ scheduling 来提升吞吐量，可大规模提供 DeepSeek-V4.1-Flash（prefill 在 4 个 SM100 上，decode 在 64 个上）。
