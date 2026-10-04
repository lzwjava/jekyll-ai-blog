---
audio: false
generated: true
image: false
lang: en
layout: post
title: Edge LLM Frameworks and Projects
translated: false
type: note
---

Question: What are the hot edge/on-device AI projects right now, how do LLMs run on phones and other edge devices, and which frameworks do people use (MLX and others)?

Answer:

**How an LLM runs on a phone (the short version)**

1. **Pick a small model.** Phones run roughly 0.5B to 4B parameter models. Examples are Qwen 3.5 (0.8B, 2B and up) and Meta's MobileLLM-Flash (350M to 1.4B), per a mobile-LLM tracking list updated in August 2026.
2. **Quantize it.** Weights are compressed to about 4-bit so they fit in RAM and run fast. For example, ExecuTorch's benchmarks use group-wise 4-bit weights with dynamically quantized 8-bit activations.
3. **Convert it to the runtime's format.** Common formats are GGUF (llama.cpp), safetensors (MLX), .pte (ExecuTorch) and .litertlm (LiteRT-LM).
4. **Run it on the best available hardware.** That means CPU, GPU or NPU, depending on the framework and chip. Memory bandwidth and thermal throttling are the real limits on a phone, more than raw compute.

**Frameworks people use**

- **llama.cpp (GGUF).** The most popular open-source local inference engine, with over 86K GitHub stars. It has the broadest hardware and model support. It compiles on almost anything, including ARM, x86 and RISC-V boards. The tradeoff is that you do more of the integration work yourself.
- **MLX (Apple Silicon).** Apple's array framework. It has Python bindings (mlx-lm) and Swift bindings (mlx-swift), and supports on-device LoRA fine-tuning. In one Apple Silicon comparison, MLX had the highest sustained generation throughput. Ollama 0.19 also added an MLX backend in March 2026.
- **ExecuTorch (Meta/PyTorch).** It powers AI across Instagram, WhatsApp and Messenger. It uses torch.export to avoid the separate conversion and validation step that causes numerical mismatches in other pipelines. For cross-platform apps, React Native ExecuTorch offers a useLLM hook supporting Qwen 3, Llama 3.2 and SmolLM 2.
- **LiteRT-LM (Google).** This is the successor to TensorFlow Lite for LLMs. It supports CPU, GPU and NPU on Android and iOS, and the MediaPipe LLM Inference API is now maintenance-only. Multi-token prediction, added in April 2026, gives 2x+ faster decode on mobile GPUs.
- **Apple Foundation Models.** A Swift API (iOS 26) to Apple's roughly 3B on-device model, the easiest path for Apple developers.
- **MLC-LLM.** A machine-learning compiler and deployment engine. It's best when you want peak compiled performance for one specific model and target.
- **Cactus.** A newer cross-platform SDK. It offers hybrid cloud fallback. Note that this source is Cactus's own comparison page, so it ranks itself first.

**Quick picks**

| Goal | Use |
|---|---|
| Mac or iPhone, max speed | MLX (or Apple Foundation Models for the built-in model) |
| Any model, any hardware | llama.cpp + GGUF |
| Cross-platform mobile app | React Native ExecuTorch |
| Android with NPU/GPU | LiteRT-LM |
| PyTorch-native team | ExecuTorch |

**Hot edge projects to watch**

- LiteRT-LM replacing MediaPipe and TFLite for LLMs.
- ExecuTorch expanding to desktop with CUDA and Metal backends, now being experimented with.
- Ollama moving onto MLX for Apple Silicon.
- Small hybrid models such as Mamba-2-based Nemotron-3 Nano, Granite-4.0-H and Falcon-H1, included in a public Apple Silicon benchmark repo.
- Open benchmark harnesses like that one, which compare MLX Swift, llama.cpp, Core ML, LiteRT-LM, ExecuTorch and others on the same model.

Framework rankings change quickly, and many of these sources are blog posts or vendor pages. Check the repos for the latest versions before committing.

References:
- [awesome-mobile-llm](https://github.com/stevelaskaridis/awesome-mobile-llm)
- [apple-silicon-llm-bench](https://github.com/john-rocky/apple-silicon-llm-bench)
- [Best On-Device LLM Framework in 2026 (Cactus)](https://cactuscompute.com/compare/best-on-device-llm-framework)
- [Choosing an On-Device LLM Runtime on Apple Silicon](https://medium.com/@michael.hannecke/choosing-an-on-device-llm-runtime-on-apple-silicon-a-decision-framework-beyond-benchmarks-2449067b8b67)
- [Run Gemma content generation and inferences](https://ai.google.dev/gemma/docs/run)
- [ExecuTorch paper](https://arxiv.org/html/2605.08195v1)
- [Best Edge AI Framework for IoT in 2026](https://cactuscompute.com/compare/best-edge-ai-framework-for-iot)
- [Production-Grade Local LLM Inference on Apple Silicon](https://huggingface.co/papers/2511.05502)
- [Running Llama on Your Phone: On-Device LLMs 2026](https://www.buildmvpfast.com/blog/on-device-llm-mobile-llama-ios-android-2026)
- [LiteRT vs TensorFlow Lite cheat sheet](https://dev.to/john-rocky/litert-vs-tensorflow-lite-what-changed-plus-the-old-name-new-name-cheat-sheet-40nl)