---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 边缘LLM框架与项目
translated: true
type: note
---

问题：目前热门/设备端 AI 项目有哪些？LLM 如何在手机和其他边缘设备上运行？人们使用哪些框架（MLX 等）？

答案：

**LLM 在手机上运行的简要流程**

1. **选择一个小型模型。** 手机大致运行 0.5B 到 4B 参数的模型。根据 2026 年 8 月更新的移动端 LLM 跟踪列表，示例包括 Qwen 3.5（0.8B、2B 及以上）和 Meta 的 MobileLLM-Flash（350M 到 1.4B）。
2. **量化模型。** 权重被压缩到约 4 位，以便适配内存并快速运行。例如，ExecuTorch 的基准测试使用分组 4 位权重和动态量化 8 位激活。
3. **转换为运行时格式。** 常见格式包括 GGUF（llama.cpp）、safetensors（MLX）、.pte（ExecuTorch）和 .litertlm（LiteRT-LM）。
4. **在最佳可用硬件上运行。** 即根据框架和芯片选择 CPU、GPU 或 NPU。在手机上，内存带宽和热节流是真正的限制因素，而非原始算力。

**人们使用的框架**

- **llama.cpp (GGUF)。** 最受欢迎的开源本地推理引擎，GitHub 星标超过 86K。拥有最广泛的硬件和模型支持。可在几乎所有平台上编译，包括 ARM、x86 和 RISC-V 板卡。代价是需要自己完成更多集成工作。
- **MLX (Apple Silicon)。** Apple 的数组框架。支持 Python 绑定（mlx-lm）和 Swift 绑定（mlx-swift），并支持设备端 LoRA 微调。在一项 Apple Silicon 对比中，MLX 的持续生成吞吐量最高。Ollama 0.19 也在 2026 年 3 月增加了 MLX 后端。
- **ExecuTorch (Meta/PyTorch)。** 为 Instagram、WhatsApp 和 Messenger 的 AI 功能提供支持。它使用 torch.export 来避免其他流水线中因单独转换和验证步骤导致的数值不匹配问题。对于跨平台应用，React Native ExecuTorch 提供了支持 Qwen 3、Llama 3.2 和 SmolLM 2 的 useLLM 钩子。
- **LiteRT-LM (Google)。** 这是 TensorFlow Lite 在 LLM 领域的继任者。在 Android 和 iOS 上支持 CPU、GPU 和 NPU，MediaPipe LLM Inference API 现已进入仅维护状态。2026 年 4 月新增的多 token 预测可在移动 GPU 上实现 2 倍以上的解码速度提升。
- **Apple Foundation Models。** 一个 Swift API（iOS 26），用于 Apple 约 3B 参数的设备端模型，是 Apple 开发者最便捷的路径。
- **MLC-LLM。** 一个机器学习编译器与部署引擎。最适合针对特定模型和目标追求峰值编译性能的场景。
- **Cactus。** 一个较新的跨平台 SDK。提供混合云端回退功能。注意，该来源是 Cactus 自身的对比页面，因此它将自身排在第一。

**快速选择指南**

| 目标 | 使用 |
|---|---|
| Mac 或 iPhone，追求最高速度 | MLX（或使用内置模型的 Apple Foundation Models） |
| 任意模型，任意硬件 | llama.cpp + GGUF |
| 跨平台移动应用 | React Native ExecuTorch |
| 搭载 NPU/GPU 的 Android 设备 | LiteRT-LM |
| 使用 PyTorch 原生团队 | ExecuTorch |

**值得关注的边缘端热门项目**

- LiteRT-LM 取代 MediaPipe 和 TFLite 用于 LLM。
- ExecuTorch 扩展到桌面端，支持 CUDA 和 Metal 后端，目前正处于实验阶段。
- Ollama 向 MLX 迁移以支持 Apple Silicon。
- 小型混合模型，如基于 Mamba-2 的 Nemotron-3 Nano、Granite-4.0-H 和 Falcon-H1，已纳入公开的 Apple Silicon 基准测试仓库。
- 像这样的开放基准测试工具，可在同一模型上对比 MLX Swift、llama.cpp、Core ML、LiteRT-LM、ExecuTorch 等框架。

框架排名变化迅速，且许多来源为博客文章或供应商页面。在正式采用前，请查阅相关仓库获取最新版本。

参考文献：
- [awesome-mobile-llm](https://github.com/stevelaskaridis/awesome-mobile-llm)
- [apple-silicon-llm-bench](https://github.com/john-rocky/apple-silicon-llm-bench)
- [2026 年最佳设备端 LLM 框架 (Cactus)](https://cactuscompute.com/compare/best-on-device-llm-framework)
- [在 Apple Silicon 上选择设备端 LLM 运行时](https://medium.com/@michael.hannecke/choosing-an-on-device-llm-runtime-on-apple-silicon-a-decision-framework-beyond-benchmarks-2449067b8b67)
- [运行 Gemma 内容生成与推理](https://ai.google.dev/gemma/docs/run)
- [ExecuTorch 论文](https://arxiv.org/html/2605.08195v1)
- [2026 年最佳边缘 AI 框架 (物联网)](https://cactuscompute.com/compare/best-edge-ai-framework-for-iot)
- [Apple Silicon 上的生产级本地 LLM 推理](https://huggingface.co/papers/2511.05502)
- [在手机上运行 Llama：2026 年设备端 LLM](https://www.buildmvpfast.com/blog/on-device-llm-mobile-llama-ios-android-2026)
- [LiteRT 与 TensorFlow Lite 速查表](https://dev.to/john-rocky/litert-vs-tensorflow-lite-what-changed-plus-the-old-name-new-name-cheat-sheet-40nl)