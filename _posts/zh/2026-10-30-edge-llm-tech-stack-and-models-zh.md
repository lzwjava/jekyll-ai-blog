---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Edge LLM技术栈与模型
translated: true
type: note
---

**问题：** 什么是边缘 LLM 技术栈，人们实际使用哪些模型？

---

**回答：**

## 🧱 边缘 LLM 技术栈（2026）

### 1. 硬件层级

当前边缘 LLM 推理的硬件格局涵盖多种设备：

| 设备 | 内存 | 最佳负载 |
|---|---|---|
| MacBook M3 | 16–36 GB | 最高 70B（MLX、llama.cpp） |
| Windows 笔记本电脑（NPU） | 16 GB | 7B 级别（ONNX） |
| NVIDIA Jetson AGX Orin | 16–64 GB | 13B（TensorRT） |
| Raspberry Pi 5 | 8 GB | 1B（llama.cpp，仅 CPU） |

2026 年存在四大边缘推理目标平台：**Apple ANE**、**Qualcomm Hexagon**、**WebGPU/WebLLM** 和 **NVIDIA Jetson**。

---

### 2. 推理运行时 / 框架

2026 年真正重要的七个运行时：

| 运行时 | 最适合 | 说明 |
|---|---|---|
| **llama.cpp** | CPU / 最大可移植性 | GGUF 格式，可在 x86、ARM、Apple Silicon 甚至 Raspberry Pi 上运行 |
| **Ollama** | 开发者体验 / 原型开发 | 封装 llama.cpp 并提供 HTTP API；2026 年 GitHub 星标突破 16.5 万，因为 `ollama run deepseek-r1` 开箱即用 |
| **MLX** | Apple Silicon | 在 Apple Silicon 上实现最高持续生成吞吐量 |
| **ExecuTorch** | 移动端（iOS/Android） | 支撑 Instagram、WhatsApp、Messenger 和 Facebook 中数十亿用户规模的 AI 功能；Hugging Face 上约 80% 的热门边缘 LLM 都有 ExecuTorch 导出 |
| **MLC-LLM** | 跨平台 GPU | 通用部署，通过 OpenCL、Vulkan、CUDA 和 Metal 在边缘实现高效运行 |
| **TensorRT Edge-LLM** | NVIDIA Jetson（生产环境） | 包含 EAGLE-3 推测解码和 NVFP4 量化；基准测试显示推理速度比未优化方案最高快 5 倍 |
| **LiteRT-LM** | Android / iOS | Google 的移动优先运行时，最适合 Gemma 级别模型 |

---

### 3. 平台特定技术栈

2026 年各平台的标准配置：

- **iOS** → MLX / Apple Foundation Models + Gemma 3n / Phi-4-mini
- **Android** → ExecuTorch / MLC-LLM + Gemma 3n E4B（3 GB 占用）
- **Windows / Linux 笔记本电脑** → Ollama + llama.cpp

NVIDIA Jetson 平台：

- Jetson AGX Thor → **TensorRT Edge-LLM SDK**（生产环境）
- Jetson AGX Orin 64GB → TensorRT-LLM / Edge-LLM
- Jetson Orin Nano / NX → llama.cpp（CUDA），上限 7B @ Q4_K_M
- Raspberry Pi / 单板计算机（ARM）→ llama.cpp（CPU），1B–3B 模型

---

### 4. 量化格式

各目标平台的量化格式选择：

| 目标平台 | 格式 |
|---|---|
| Apple ANE | INT4 权重 + FP16 激活（Core ML） |
| Qualcomm Hexagon | QNN INT8 / INT4 |
| WebGPU / WebLLM | Q4 MLC（q4f16_1） |
| Jetson Orin Nano | Q4 GGUF 或 TRT-LLM INT4 |
| Jetson AGX / Thor | NVFP4 + FP8 KV |

---

### 5. 热门边缘模型

移动端推理由 1B–4B 的专用模型主导：**Apple 的 Foundation Models**、**Google 的 Gemini Nano**、**Llama 3.2 1B/3B**、**Phi-5**、**Qwen3-1.5B**、**DeepSeek Edge**、**TinyLlama**。

对于性能更强的边缘设备（Jetson、M 系列 Mac），人们通常运行：

- **Meta-Llama-3.1-8B-Instruct** — 多语言对话的首选
- **GLM-4-9B-0414** 和 **Qwen2.5-VL-7B-Instruct**（多模态视觉-语言）
- **DeepSeek V4**、**Llama 4**、**Qwen 3.5**、**Mistral Large 3** — 用于边缘部署对比的开源前沿选项
- **Gemma 3n E4B** — 移动端领先者，手机占用仅 3 GB，LMArena Elo 评分超过 1300

---

### 关键结论

"2026 年边缘 AI 真正的创新和生产可行性不在于模型规模的扩大，而在于掌握对更小模型进行极致优化的艺术。"制胜组合是：**合适的模型规模 + 合适的量化格式 + 硬件原生运行时**。

---

**参考资料：**
- [Edge LLM Runtime Stack 2026: llama.cpp, Ollama, TensorRT, ExecuTorch, MLX, LiteRT-LM](https://edgeaistack-site.pages.dev/blog/edge-llm-runtime-stack-2026/)
- [Inference at the Edge: Running LLMs on Consumer GPUs](https://web-9ja.pages.dev/blog/inference-at-edge-llms-consumer-gpus)
- [Edge and On-Device LLM Inference Docs](https://llm-docs.github.io/docs/edge-on-device-inference)
- [Edge AI Hardware: Jetson Orin to Mac Mini — Running Gemma 4 Locally](https://aiindigo.com/blog/edge-ai-hardware-from-jetson-orin-to-mac-mini-running-gemma-4-locally)
- [Cheapest LLM Stack for Edge / On-Device Inference (May 2026)](https://callsphere.ai/blog/llm-comparison-edge-on-device-inference-cheapest-stack-may-2026)
- [Edge Inference — Apple ANE, Qualcomm Hexagon, WebGPU, Jetson](https://learn.traeai.com/t/ai-engineering/phases/17-infrastructure-and-production/12-edge-inference)