---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 谷歌生成式AI图像配置
translated: true
type: note
---

以下是一个快速概览：Google Gen AI（Gemini/Imagen）Python SDK 不支持 `image_size` 参数。您需要选择模型变体（每个变体都有隐含的默认分辨率），控制**宽高比**，并且如果需要更高像素数量，可以应用**放大**功能。您还可以调整**压缩**和**输出格式**，以及常见的“图像数量”、“负面提示”、“安全”和“人物”设置。

## 模型变体

您需要选择模型名称——每个变体都有其默认分辨率和性能特征：

* **imagen-3.0** 系列：

  * `imagen-3.0-generate-002`
  * `imagen-3.0-generate-001`
  * `imagen-3.0-fast-generate-001`
  * `imagen-3.0-capability-001`
* **imagen-4.0（预览版）** 系列：

  * `imagen-4.0-generate-preview-06-06`
  * `imagen-4.0-fast-generate-preview-06-06`
  * `imagen-4.0-ultra-generate-preview-06-06`
* **旧版**：`imagegeneration@002`、`@005`、`@006`（[Google Cloud][1]）

## 默认分辨率

默认情况下，这些模型的方形（“1:1”）输出为 **1024 × 1024 像素**。如果您需要更小的文件，可以在本地进行下采样；如果您需要更高的分辨率，请参阅下面的**放大**部分。（[raymondcamden.com][2]）

## 宽高比

与其指定绝对尺寸，不如在您的 `GenerateImagesConfig` 中使用 `aspect_ratio` 字段。支持的值包括：

* `1:1`（方形）
* `3:4`（竖版，社交媒体肖像）
* `4:3`（经典摄影/电视）
* `16:9`（宽屏风景）
* `9:16`（竖版/肖像，例如手机背景）（[Google Cloud][1]、[Google AI for Developers][3]）

您可以在社区教程中找到相同的列表：

* DataCamp 指出 Imagen 3 完全支持这五种宽高比（[DataCamp][4]）
* CodeSignal 的指南也为 Gemini/Imagen 列举了这些宽高比（[CodeSignal][5]）

## 放大

如果您需要真正的“2K”或“4K”输出，请调用**放大**模式：

```python
from google.genai import types
config = types.GenerateImagesConfig(
    mode="upscale",
    upscale_config=types.UpscaleConfig(upscale_factor="x2"),
)
```

* `"x2"` 使每个维度翻倍（例如 1024 → 2048，约 2K）
* `"x4"` 使每个维度翻四倍（例如 1024 → 4096，约 4K）（[Google Cloud][1]）

## 压缩与格式

* **JPEG 质量**：使用 `compression_quality`（0–100，默认 75）在文件大小和细节之间进行权衡（[Google Cloud][1]）
* **MIME 类型**：通过 `output_options.mime_type`，您可以选择
  `image/jpeg`、`image/png`、`image/gif`、`image/webp`、`image/bmp`、`image/tiff` 或 `image/vnd.microsoft.icon`（[Google Cloud][6]）

## 其他配置选项

其他所有选项都在 `GenerateImagesConfig` 中：

```python
config = types.GenerateImagesConfig(
    number_of_images=1,           # 生成多少张图像
    seed=1234,                    # 用于确定性输出
    enhance_prompt=True,          # 基于 LLM 的提示词重写
    negative_prompt="排除狗",
    language="en",
    safety_filter_level="block_medium_and_above",
    person_generation="allow_adult",
)
```

这些选项让您可以控制随机性、提示词增强、安全阈值以及模型是否可以包含人物。（[Google Cloud][1]）

## 建议

移除您的 `image_size="2K"` 行——没有这样的标志。相反：

1. **选择合适的模型**以平衡速度与质量。
2. 使用 **`aspect_ratio`** 来控制构图。
3. 如果您确实需要更高的像素数量，请在基础分辨率下生成图像，然后应用内置的**放大**功能（“x2”或“x4”）。
4. 调整 **`compression_quality`** 或在本地进行下采样以获得更小的文件。

通过这些控制选项，您可以实现方形或电影般的构图，小尺寸或高分辨率输出，而无需使用不受支持的 `image_size` 参数。

[1]: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api "生成图像 | Vertex AI 上的生成式 AI | Google Cloud"
[2]: https://www.raymondcamden.com/2025/01/30/generative-ai-images-with-gemini-and-imagen-an-introduction?utm_source=chatgpt.com "使用 Gemini 和 Imagen 生成 AI 图像"
[3]: https://ai.google.dev/gemini-api/docs/imagen?utm_source=chatgpt.com "使用 Imagen 生成图像 | Gemini API | Google AI for ..."
[4]: https://www.datacamp.com/tutorial/imagen-3 "Imagen 3：Gemini API 示例指南 | DataCamp"
[5]: https://codesignal.com/learn/courses/creating-images-with-geminis-imagen-and-flask/lessons/generating-a-simple-image-with-geminis-imagen-and-flask?utm_source=chatgpt.com "使用 Gemini 的 Imagen 和 Flask 生成简单图像"
[6]: https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images?utm_source=chatgpt.com "使用文本提示生成图像"
