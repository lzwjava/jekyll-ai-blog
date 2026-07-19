---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为OpenRouter打造的中国友好型视觉模型
translated: true
type: note
---

问题：如果ChatGPT/Gemini违反中国大陆用户条款，我可以在OpenRouter上使用哪些视觉模型？

回答：

是的，这是一个实际问题。对于中国大陆用户，**官方ChatGPT/Gemini消费者服务可能存在可用性限制**，OpenAI明确表示从不受支持的国家访问ChatGPT/API可能导致账户被封禁或暂停。([OpenAI帮助中心][1]) OpenAI的条款还要求用户遵守适用的贸易法律和限制。([OpenAI][2])

对于`ww vision-model` CLI，我会避免仅依赖以下模型：

```
google/gemini-2.5-flash
openai/gpt-5
anthropic/claude-sonnet-4
```

尽管从技术上讲它们是优秀的VLM。

更好的选择：

## 1. Qwen-VL（最适合中国用户）

OpenRouter：

```bash
qwen/qwen2.5-vl-72b-instruct
```

或：

```bash
qwen/qwen2.5-vl-32b-instruct
```

架构：

```
image
  |
  v
vision encoder
  |
  v
LLM
  |
  v
text answer
```

示例：

```bash
ww vision-model test \
  --model qwen/qwen2.5-vl-72b-instruct \
  --max-tokens 1000
```

适用场景：

* 截图理解
* OCR
* UI代理
* 中文文档
* 图表

---

## 2. 开源VLM

在OpenRouter上搜索：

```
vl
vision-language
multimodal
```

查找：

```
input:
  text
  image

output:
  text
```

示例：

```
qwen/qwen2.5-vl-72b-instruct
qwen/qwen2.5-vl-32b-instruct
qwen/qwen2.5-vl-7b-instruct
mistralai/pixtral
google/gemma-3
```

---

## 3. 自托管（可能适合你）

既然你已经运行GPU/训练，本地VLM会很有趣。

RTX 4070 12GB：

可能的选择：

```
Qwen2.5-VL-3B
Qwen2.5-VL-7B
MiniCPM-V
InternVL
```

示例：

```bash
ollama pull qwen2.5vl:7b

ollama run qwen2.5vl:7b
```

无服务条款依赖。

架构：

```
image
 ↓
CLIP/SigLIP vision tower
 ↓
projector
 ↓
Qwen LLM
 ↓
answer
```

---

## 4. 针对你的`ww`代理用例

我会设置默认优先级：

```
1. qwen2.5-vl-72b（云端）
2. qwen2.5-vl-7b（本地）
3. gemini-2.5-flash（如可用）
4. claude-sonnet（如可用）
```

因为截图代理主要需要：

* 坐标理解
* OCR
* UI元素检测
* 简短推理

而不是纯粹的基准测试智商。

---

一个有用的OpenRouter过滤思路：

```python
for model in models:
    if "image" in model.input_modalities:
        if "text" in model.output_modalities:
            print(model.id)
```

你想要：

```
image -> text
```

而不是：

```
text -> image
```

FLUX是：

```
text -> image
```

这就是为什么你的测试返回了：

```
finish_reason=stop
content=""
```

对于中国友好的AI代理栈，Qwen-VL + 本地Ollama/vLLM可能是最简洁的路径。

[1]: https://help.openai.com/en/articles/9131992-chatgpt-and-api-services-in-unsupported-countries-and-territories?utm_source=chatgpt.com "ChatGPT and API services in unsupported countries and territories | OpenAI Help Center"
[2]: https://openai.com/policies/terms-of-use/?utm_source=chatgpt.com "Terms of Use | OpenAI"
