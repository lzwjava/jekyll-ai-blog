---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: DeepSeek OCR性能与效率分析
translated: true
type: note
---

### DeepSeek OCR 表现如何？

DeepSeek OCR 是 DeepSeek AI 于 2025 年 10 月 20 日最新发布的 30 亿参数视觉语言模型（VLM），专门针对光学字符识别（OCR）和结构化文档处理进行了优化。根据早期评估和基准测试，其表现相当出色：

- **压缩效率**：采用“光学上下文压缩”技术，将视觉数据压缩为更少的标记（例如，相同内容仅需 100 个视觉标记而非 1000+ 个文本标记），在 10 倍压缩比下实现约 97% 的解码精度，20 倍压缩比下仍能保持近乎无损的效果。这使得它在处理大型文档时非常高效，且不会丢失关键细节。

- **吞吐量**：在单 GPU 上每日可处理超过 20 万页文档，这对于档案数字化或表单自动提取等实际应用而言是重大突破。

- **基准测试表现**：在文档理解任务中超越其他开源 OCR 模型，在结构化输出精度方面媲美或接近 GPT-4V 等闭源领先模型。早期测试突显了其在处理复杂布局、表格和多语言文本方面的优势。

不过，由于该模型非常新，实际应用才刚刚开始。有报告称本地部署存在一些挑战（如在 Apple Silicon 或 NVIDIA 设备上需要调整配置），但一旦运行起来，用户反馈其实验用途“相当不错”。总体而言，如果您需要高效、高精度的文档 OCR，这是一个可靠的选择——特别是作为开源方案。对于通用图像 OCR（如表情包或手写文字），与 Tesseract 等专用工具相比可能仍需微调。

### 什么是视觉标记？

在 AI 模型中，特别是像 OpenAI、DeepSeek 或 LLaVA 这样的多模态视觉语言模型（VLM）中，**视觉标记**是一小块视觉数据的紧凑数值表示。具体说明如下：

- **工作原理**：图像不会直接输入语言模型（后者处理文本）。相反，图像被分割成固定大小的图块（如 14x14 像素）。每个图块被嵌入为一个向量——即“标记”——类似于文本中单词被转换为标记的方式。这些视觉标记捕获边缘、颜色或纹理等特征，使模型能够结合文本标记来“理解”并推理图像内容。

- **重要性**：这种标记化实现了高效处理。例如，一张 512x512 的图像可能生成数百个视觉标记，但先进技术（如 DeepSeek OCR 所用）会进一步压缩它们，以在保持精度的同时降低计算成本。这对于图像描述、视觉问答或 OCR 等任务至关重要，因为模型需要融合视觉和文本信息。

- **示例**：在 GPT-4V 中，上传的照片会被转换为约 85 个视觉标记（经过调整大小和分块处理），模型将这些标记视为提示词来生成响应。

视觉标记弥合了像素与语言之间的鸿沟，使 AI 能够以计算可行的方式“看见”世界。

**参考资料**
[DeepSeek 刚刚发布 30 亿参数 OCR 模型](https://www.marktechpost.com/2025/10/20/deepseek-just-released-a-3b-ocr-model-a-3b-vlm-designed-for-high-performance-ocr-and-structured-document-conversion/)
[DeepSeek-OCR 的关键不是 OCR，而是标记压缩](https://medium.com/@olimiemma/deepseek-ocr-isnt-about-ocr-it-s-about-token-compression-db1747602e29)
[DeepSeek 新款 OCR 模型单 GPU 日处理超 20 万页](https://analyticsindiamag.com/ai-news-updates/deepseeks-new-ocr-model-can-process-over-2-lakh-pages-daily-on-a-single-gpu/)
[标记：AI 与机器学习定义](https://www.ultralytics.com/glossary/token)
[革命性 AI 视觉技术：视觉感知标记](https://kitemetric.com/blogs/revolutionizing-ai-vision-introducing-visual-perception-tokens)
