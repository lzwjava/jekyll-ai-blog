---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用图像生成器进行视力测试
translated: true
type: note
---

问题：为什么我的 `ww vision-model test` 总是返回 `finish_reason=stop` 且响应内容为空？

答案：

主要问题很可能是**模型类型不匹配**。

你测试时使用了：

```
--model black-forest-labs/flux.2-pro
```

`FLUX.2-pro` 是一个**图像生成模型**，而不是**视觉语言模型（VLM）**。

你的测试发送的是：

```
图像 + 文本提示
        ↓
期望：
描述/分析图像的文本响应
```

但 FLUX 期望的是：

```
文本提示
        ↓
生成的图像
```

因此 API 可以合法地返回：

```
finish_reason=stop
content=""
```

因为没有文本回答通道。

请改用真正的视觉语言模型：

示例：

```
google/gemini-2.5-flash
google/gemini-2.5-pro
openai/gpt-5
anthropic/claude-sonnet-4
qwen/qwen2.5-vl-72b-instruct
```

OpenRouter 风格的测试：

```bash
ww vision-model test \
  --model google/gemini-2.5-flash \
  --max-tokens 1000
```

你的测试图像也非常小：

```
64x64 蓝色正方形
```

一个 VLM 可能会回答类似：

> "图像是一个纯蓝色正方形。"

---

另外请检查你的请求处理方式。许多视觉 API 要求图像内容采用以下格式：

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "Describe this image"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "data:image/png;base64,..."
      }
    }
  ]
}
```

而非：

```json
{
  "prompt": "Describe image",
  "image": "..."
}
```

---

你的警告与此无关：

```
RequestsDependencyWarning:
urllib3 ... doesn't match supported version
```

它仅表示你的 Python 依赖版本不常见。它不会导致模型输出为空。

一个良好的调试流程：

```bash
# 1. 测试文本模型
ww vision-model test --model google/gemini-2.5-flash

# 2. 测试图像理解模型
ww vision-model test --model qwen/qwen2.5-vl-72b-instruct

# 3. 单独测试图像生成模型
ww image-model test --model black-forest-labs/flux.2-pro
```

所以简而言之：

**FLUX 属于错误的类别。它生成图像，而不是查看并描述图像。** 请使用 Gemini / Qwen-VL / Claude / OpenAI 的视觉模型进行 `vision-model` 测试。
