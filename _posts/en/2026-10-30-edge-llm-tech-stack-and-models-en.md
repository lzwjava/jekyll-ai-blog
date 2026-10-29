---
audio: false
generated: true
image: false
lang: en
layout: post
title: Edge LLM Tech Stack and Models
translated: false
type: note
---

**Question:** What is the edge LLM tech stack, and what models do people actually use?

---

**Answer:**

## 🧱 Edge LLM Tech Stack (2026)

### 1. Hardware Tiers

The current hardware landscape for edge LLM inference spans a wide range of devices:

| Device | RAM | Best Workload |
| --- | --- | --- |
| MacBook M3 | 16–36 GB | Up to 70B (MLX, llama.cpp) |
| Windows Laptop (NPU) | 16 GB | 7B class (ONNX) |
| NVIDIA Jetson AGX Orin | 16–64 GB | 13B (TensorRT) |
| Raspberry Pi 5 | 8 GB | 1B (llama.cpp, CPU only) |

Four main edge targets exist in 2026: **Apple ANE**, **Qualcomm Hexagon**, **WebGPU/WebLLM**, and **NVIDIA Jetson**.

---

### 2. Inference Runtimes / Frameworks

The seven runtimes that actually matter in 2026:

| Runtime | Best For | Notes |
| --- | --- | --- |
| **llama.cpp** | CPU / max portability | GGUF format, runs on x86, ARM, Apple Silicon, even Raspberry Pi |
| **Ollama** | Developer DX / prototyping | Wraps llama.cpp with HTTP API; crossed 165k GitHub stars in 2026 because `ollama run deepseek-r1` just works |
| **MLX** | Apple Silicon | Achieves the highest sustained generation throughput on Apple Silicon |
| **ExecuTorch** | Mobile (iOS/Android) | Powers AI features in Instagram, WhatsApp, Messenger, and Facebook at billions-of-users scale; ~80% of popular edge LLMs on Hugging Face have ExecuTorch exports |
| **MLC-LLM** | Cross-platform GPU | Universal deployment, enabling efficient operation on edge via OpenCL, Vulkan, CUDA, and Metal |
| **TensorRT Edge-LLM** | NVIDIA Jetson (production) | Includes EAGLE-3 speculative decoding and NVFP4 quantization; benchmarks show up to 5× faster inference compared to unoptimized counterparts |
| **LiteRT-LM** | Android / iOS | Google's mobile-first runtime, best for Gemma-class models |

---

### 3. Platform-Specific Stack

The standard per-platform setup in 2026:

- **iOS** → MLX / Apple Foundation Models + Gemma 3n / Phi-4-mini
- **Android** → ExecuTorch / MLC-LLM + Gemma 3n E4B (3 GB footprint)
- **Windows / Linux laptop** → Ollama + llama.cpp

For NVIDIA Jetson:

- Jetson AGX Thor → **TensorRT Edge-LLM SDK** (production)
- Jetson AGX Orin 64GB → TensorRT-LLM / Edge-LLM
- Jetson Orin Nano / NX → llama.cpp (CUDA), 7B @ Q4_K_M ceiling
- Raspberry Pi / SBC (ARM) → llama.cpp (CPU), 1B–3B models

---

### 4. Quantization Formats

Quantization format choice per target:

| Target | Format |
| --- | --- |
| Apple ANE | INT4 weights + FP16 activations (Core ML) |
| Qualcomm Hexagon | QNN INT8 / INT4 |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 |
| Jetson AGX / Thor | NVFP4 + FP8 KV |

---

### 5. Popular Edge Models

Mobile inference is dominated by 1B–4B specially designed models: **Apple's Foundation Models**, **Google's Gemini Nano**, **Llama 3.2 1B/3B**, **Phi-5**, **Qwen3-1.5B**, **DeepSeek Edge**, **TinyLlama**.

For beefier edge devices (Jetson, M-series Mac), people commonly run:

- **Meta-Llama-3.1-8B-Instruct** — top pick for multilingual dialogue
- **GLM-4-9B-0414** and **Qwen2.5-VL-7B-Instruct** (multimodal vision-language)
- **DeepSeek V4**, **Llama 4**, **Qwen 3.5**, **Mistral Large 3** — open-source frontier options compared for edge deployment
- **Gemma 3n E4B** — mobile leader with a 3 GB phone footprint and >1300 LMArena Elo

---

### Key Takeaway

The "true innovation and production viability for edge AI in 2026 lies not in scaling up, but in mastering the art of extreme optimization for smaller models." The winning combo is: **right model size + right quantization format + hardware-native runtime**.

---

**References:**

- [Edge LLM Runtime Stack 2026: llama.cpp, Ollama, TensorRT, ExecuTorch, MLX, LiteRT-LM](https://edgeaistack-site.pages.dev/blog/edge-llm-runtime-stack-2026/)
- [Inference at the Edge: Running LLMs on Consumer GPUs](https://web-9ja.pages.dev/blog/inference-at-edge-llms-consumer-gpus)
- [Edge and On-Device LLM Inference Docs](https://llm-docs.github.io/docs/edge-on-device-inference)
- [Edge AI Hardware: Jetson Orin to Mac Mini — Running Gemma 4 Locally](https://aiindigo.com/blog/edge-ai-hardware-from-jetson-orin-to-mac-mini-running-gemma-4-locally)
- [Cheapest LLM Stack for Edge / On-Device Inference (May 2026)](https://callsphere.ai/blog/llm-comparison-edge-on-device-inference-cheapest-stack-may-2026)
- [Edge Inference — Apple ANE, Qualcomm Hexagon, WebGPU, Jetson](https://learn.traeai.com/t/ai-engineering/phases/17-infrastructure-and-production/12-edge-inference)
