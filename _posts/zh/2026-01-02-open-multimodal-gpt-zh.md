---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 开源极简多模态 GPT 项目
translated: true
type: note
---

Question: What are good open source projects for multimodal GPT-like models, similar to nanoGPT, that can generate or edit images?

Answer:

nanoGPT 是一个非常受欢迎的、用于在纯 PyTorch 中从零开始训练 GPT 风格语言模型的极简教育级实现。对于 multimodal 模型（能够同时处理文本和图像，类似于 GPT-4V），在简单性和教育价值方面最接近的等效项目是 **nanoVLM**。

### Top Recommendation: nanoVLM

- **Description**: nanoVLM 是一个轻量级、极简的 Vision-Language Model (VLM)，完全采用纯 PyTorch 构建，明确受到 nanoGPT 的启发。它包含一个 LLaMA 风格的 decoder 用于语言处理，一个 SigLiP vision encoder，以及一个用于连接两者的 modality projector。
- **Why it's similar to nanoGPT**: 它的设计目标是紧凑、易于理解，并且可以用极少的资源从零开始训练（例如，仅需在单张 H100 GPU 上运行 6 小时，甚至可以在免费的 Google Colab notebook 中获得不错的性能）。
- **Capabilities**: 主要用于 multimodal 理解（例如，image captioning、visual question answering），而非原生的图像生成或编辑。
- **GitHub**: <https://github.com/huggingface/nanoVLM>

### Other Notable Minimal/Educational Multimodal Projects

- **Seemore**: 一个从零开始的 vision-language model 的 PyTorch 实现（包含 image encoder + multimodal projector + decoder LLM）。它是向 Andrej Karpathy 的 makemore/nanoGPT 系列致敬，为了保持简单，使用了简单的 character-level autoregressive model。
- 这些项目对于学习 multimodal 模型底层的工作原理非常有用。

### For Multimodal Understanding (Image Input + Text Output, like most "multimodal GPT")

流行的开源项目包括：

- **LLaVA** (以及 LLaVA-NeXT 等变体)：旨在实现 GPT-4V 级能力的视觉指令微调（visual instruction-tuned）先驱模型之一。易于 fine-tune 并在本地运行。
  - GitHub: <https://github.com/haotian-liu/LLaVA>
- 其他许多模型如 Qwen-VL、InternVL，但它们的规模更大，不像 "nano" 那样精简。

### For Models That Can Generate or Edit Images

真正的 any-to-any multimodal 模型（文本/图像输入 → 文本/图像输出，类似于 GPT-4o）在开源界较为少见，尤其是极简模型：

- **DeepSeek Janus-Pro**: 开源系列模型，支持图像理解和生成。
- **MMaDA**: 基于 diffusion 的 multimodal 模型，用于文本和图像的生成/编辑。
- **OmniGen 2**: 统一模型，支持 text-to-image 生成、图像编辑和 multimodal 任务（类似于 GPT-4o 的融合能力）。
- 这些模型更加先进且消耗资源，不像 nanoGPT/nanoVLM 那样精简。

大多数开源 multimodal 项目专注于 **vision-language understanding**（输入：图像 + 文本，输出：文本），而不是图像的生成/编辑。对于图像生成/编辑，项目通常会将 VLM 与独立的 diffusion 模型（如 Stable Diffusion）结合使用。

如果你正在寻找用于训练自己 multimodal 模型的教育代码，请从 nanoVLM 开始——它是 "nanoGPT 的 vision-language 版" 的直接对应物。

References:

- [nanoVLM GitHub](https://github.com/huggingface/nanoVLM)
- [Awesome Multimodal Large Language Models List](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models)
- [LLaVA GitHub](https://github.com/haotian-liu/LLaVA)
- [DeepSeek Janus Series](https://www.koyeb.com/blog/best-multimodal-vision-models-in-2025)
- [MMaDA GitHub](https://github.com/Gen-Verse/MMaDA)
