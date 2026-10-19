---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang-Omni音频服务框架
translated: true
type: note
---

**问题：** 什么是 `sglang-omni`，它有什么作用？

**回答：**

**SGLang-Omni** 是一个面向音频模型（TTS、ASR）和统一多模态模型的高性能服务框架，由 `sgl-project` 组织开发。它本质上是 [SGLang](https://github.com/sgl-project/sglang) 生态系统的扩展，专注于语音和全模态（omni-model）工作负载。

---

### 核心设计

SGLang-Omni 是一个用于全模态、语音和 TTS 模型的多阶段服务运行时。其设计目标是**多阶段解码**：将生成过程拆分到具有不同计算模式、依赖结构和资源需求的异构阶段中。它拥有管线拓扑、阶段生命周期、阶段间传输、模型家族集成层以及 OpenAI 兼容的服务接口，同时在适用场景下与 SGLang 组合，以实现高性能自回归调度和模型执行。

---

### 关键架构支柱

- **多阶段运行时** — 将模型生成建模为协调阶段：预处理、编码器、自回归引擎、讲话器（talker）、解码器、声码器和聚合器。
- **阶段专用调度** — 每个阶段都在与其工作负载匹配的调度器后运行，从 SGLang 支持的自回归调度到轻量级预处理和流式声码器循环。
- **传输感知执行** — 控制平面协调请求，而中继数据平面通过共享内存、NCCL、NIXL 和 Mooncake 后端传输张量负载。
- **API 接口** — OpenAI 兼容端点提供多模态对话、语音生成、批量语音、流式语音、上传声音和转写功能。

---

### 可以服务的内容

- **全模态对话/语音**：Qwen3-Omni、Ming-Omni — 多模态输入，文本/音频输出。
- **音乐生成**：MiniMax Music 3 — 歌词 + 描述 → 32 kHz 立体声歌曲。
- **TTS（文本转语音）**：Higgs Audio v3、MOSS-TTS、Fish Speech S2-Pro、Qwen3-TTS、Voxtral TTS 等 — 通过 `/v1/audio/speech`、批量、流式和上传声音实现。
- **ASR/转写**：Qwen3-ASR、Fun-ASR、ARK-ASR、MOSS-Transcribe-Diarize — 通过 `/v1/audio/transcriptions`，支持说话人标签和时间戳。
- **SGLang-Omni 路由器**：一个多工作节点的 OpenAI 兼容前端，用于健康检查、就绪状态、生命周期和能力发现。

---

### 硬件支持

| 后端 | 状态 |
| --- | --- |
| NVIDIA CUDA | 完全支持（默认，覆盖全部模型） |
| Apple Silicon | 实验性（通过 MLX 或 Torch MPS 在 macOS arm64 上运行 Qwen3-ASR） |
| Intel GPU (XPU) | 实验性（通过 PyTorch XPU 支持 Intel Arc GPU） |

---

### 简而言之

SGLang-Omni 填补了基础 SGLang 框架未覆盖的空白：**多模态音频推理**（语音输入、语音输出以及两者之间的所有场景）。如果说 SGLang 是 LLM 服务的骨干，那么 SGLang-Omni 就是其面向语音和音频模型管道的专业兄弟——全部位于熟悉的 OpenAI 兼容 API 之后。

---

**参考：**

- [sgl-project/sglang-omni](https://github.com/sgl-project/sglang-omni)
- [官方文档](https://sgl-project.github.io/sglang-omni/)
- [SGLang（基础框架）](https://github.com/sgl-project/sglang)
