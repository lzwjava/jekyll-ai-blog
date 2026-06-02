---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Vertex AI的Imagen 4模型
translated: true
type: note
---

根据您提供的代码片段，您正在使用 `genai.Client` 与 Vertex AI 上的图像生成模型进行交互。您指定的模型是 `"imagen-4.0-generate-preview-06-06"`。

以下是该模型的新特性及其代表的含义解析：

### Vertex AI 上最新的图像生成模型

您正在使用的模型 `imagen-4.0-generate-preview-06-06` 属于 Vertex AI 上最新的 **Imagen 4** 模型系列。该系列还包括：

* **`imagen-4.0-generate-preview-06-06`**：这是标准的 Imagen 4 模型，在速度和质量之间取得了平衡。
* **`imagen-4.0-ultra-generate-preview-06-06`**：此“Ultra”版本旨在提供更高质量，但速度较慢且成本更高。
* **`imagen-4.0-fast-generate-preview-06-06`**：此“Fast”变体优先考虑速度和低延迟，而非最高质量。

这些 Imagen 4 模型是一次重大更新，基于 Imagen 3 和 Imagen 2 等先前版本构建。Imagen 4 的主要特性和更新包括：

* **改进的图像质量**：新模型旨在生成比其前代更高质量的图像。
* **更广泛的宽高比支持**：Imagen 4 支持多种宽高比，包括 `1:1`、`3:4`、`4:3`、`9:16` 和 `16:9`，让您能更好地控制输出。
* **多语言提示**：虽然英语是主要语言，但这些模型也支持其他几种语言的文本提示，包括中文（简体和繁体）、印地语、日语、韩语、葡萄牙语和西班牙语（预览版）。
* **安全特性**：模型包含用户可配置的安全设置，并采用数字水印（SynthID）来识别 AI 生成的内容。

您代码片段中的 `person_generation` 和 `safety_filter_level` 参数仍然相关，允许您配置模型行为以实现负责任的 AI，正如您使用 `person_generation="ALLOW_ADULT"` 和 `safety_filter_level="BLOCK_LOW_AND_ABOVE"` 所做的那样。

### 超越图像生成

除了更新的 Imagen 模型，Google Cloud 最近还在 Vertex AI 上推出了其他新的生成式 AI 模型，包括：

* **Veo 3 和 Veo 3 Fast**：这些是最新的视频生成模型，允许您从文本或图像提示创建高质量视频。Veo 3 适用于具有原生音频和唇形同步等特性的高质量专业视频，而 Veo 3 Fast 则针对速度进行了优化。
* **Gemini 2.5 模型**：这些是 Gemini 模型系列的最新版本，包括 Gemini 2.5 Pro、Gemini 2.5 Flash 和 Gemini 2.5 Flash-Lite，为各种任务提供先进的推理能力、多模态支持以及改进的性能。
