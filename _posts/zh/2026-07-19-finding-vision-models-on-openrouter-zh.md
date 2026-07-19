---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在OpenRouter上寻找视觉模型
translated: true
type: note
---

问题：如何在OpenRouter上找到**图像分析（视觉-语言模型）**而非**图像生成模型**？

回答：

OpenRouter在界面中并未完美区分这两类模型，请尝试以下方法。

## 1. 按模型能力搜索，而非"图像"

避免使用：

```
image model
image generation
flux
stable diffusion
```

这些关键词大多指向生成模型。

应搜索：

```
vision
multimodal
image understanding
vision-language
VLM
```

优秀的视觉-语言模型示例：

| 模型                              | 类型  | 用途                     |
| -------------------------------- | ----- | ------------------------ |
| `google/gemini-2.5-flash`        | VLM   | 图像+文本 → 文本         |
| `google/gemini-2.5-pro`          | VLM   | 复杂图像推理             |
| `anthropic/claude-sonnet-4`      | VLM   | 文档/图像分析            |
| `openai/gpt-5`                   | VLM   | 图像理解                 |
| `qwen/qwen2.5-vl-72b-instruct`   | VLM   | 开源视觉模型             |
| `qwen/qwen2.5-vl-32b-instruct`   | VLM   | 更经济的选择             |

---

## 2. 查看OpenRouter模型页面

视觉模型应显示类似信息：

```
输入模态：
  文本
  图像

输出模态：
  文本
```

你需要：

```
图像 → 文本
```

而非：

```
文本 → 图像
```

生成模型通常显示：

```
输入：
  文本

输出：
  图像
```

示例：

```
black-forest-labs/flux.2-pro
stabilityai/stable-diffusion
openai/dall-e
```

这些都不是视觉模型。

---

## 3. 使用OpenRouter API模型列表

可执行查询：

```bash
curl https://openrouter.ai/api/v1/models | jq .
```

再过滤：

```bash
curl https://openrouter.ai/api/v1/models \
 | jq '.data[] | select(.architecture.input_modalities | contains(["image"])) | .id'
```

应能看到类似模型：

```
google/gemini-2.5-flash
anthropic/claude-sonnet-4
qwen/qwen2.5-vl-72b-instruct
```

---

## 4. 针对你的 `ww vision-model test`

建议测试：

```bash
ww vision-model test \
  --model google/gemini-2.5-flash \
  --max-tokens 1000
```

或：

```bash
ww vision-model test \
  --model qwen/qwen2.5-vl-72b-instruct \
  --max-tokens 1000
```

预期输出：

```
响应：
图像是一个带有轻微渐变的蓝色方块...
finish_reason=stop
```

出现 `finish_reason=stop` 是正常情况。之前的问题是：

```
content=""
```

因为FLUX没有文本输出。

---

针对你的用例（CLI代理截图理解、`ww vision-model`），推荐排序可能是：

1. Gemini 2.5 Flash — 便宜且快速
2. Qwen2.5-VL — OpenRouter上不错的选择，对中国用户友好
3. Claude Sonnet 4 — 推理能力强
4. GPT-5 视觉版 — 功能最强但价格高

FLUX应移至单独命令，例如：

```
ww image-generate test --model black-forest-labs/flux.2-pro
```

而非放在 `vision-model` 中。