---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地图像生成项目
translated: true
type: note
---

问题：有哪些项目可以让我在本地生成图像？因为 llama.cpp 只处理文本，无法生成图像。

回答：

llama.cpp 是为文本语言模型构建的。它可以配合多模态模型接受图像输入，但无法生成图像，因此之前的回答是正确的。图像生成需要扩散模型，这些模型运行在独立的项目中。

**最接近 llama.cpp 的项目**

- **stable-diffusion.cpp**：一个基于相同 ggml 库的 C/C++ 项目，支持 GGUF 量化，以及 CPU、CUDA、Metal 和 Vulkan 后端。如果你喜欢 llama.cpp 的轻量级方式，这最适合你。

**功能完善的用户界面（最容易上手）**

- **ComfyUI**：一个基于节点的工作流工具，也是开发最活跃的。它支持当前大多数开源模型（SDXL、Flux 等）。
- **Fooocus**：非常简洁，采用类似 Midjourney 的提示方式，设置极少。
- **InvokeAI**：界面精致，带有画布，支持修补和编辑。
- **AUTOMATIC1111 WebUI**：长期以来的经典之作，拥有庞大的扩展生态。

**面向开发者**

- **Hugging Face Diffusers**：一个 Python 库，用于在自己的代码中编写图像生成的脚本。

**实用建议**

- 模型来自 Hugging Face 或 Civitai。请检查每个模型的许可证。
- 拥有 8 GB 或更多显存的 NVIDIA GPU 可以流畅运行 SDXL 级别的模型。较小的 GPU、纯 CPU 机器和 Apple Silicon 仍可使用量化模型，只是速度较慢。
- 想要快速上手，Fooocus 或 ComfyUI 最简单。如果喜欢 llama.cpp 风格的命令行工作流，可使用 stable-diffusion.cpp。

如果你告诉我你的操作系统和 GPU，我可以推荐最佳方案并提供安装步骤。

参考文献：

- [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Fooocus](https://github.com/lllyasviel/Fooocus)
- [InvokeAI](https://github.com/invoke-ai/InvokeAI)
- [AUTOMATIC1111 Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Hugging Face Diffusers](https://github.com/huggingface/diffusers)
