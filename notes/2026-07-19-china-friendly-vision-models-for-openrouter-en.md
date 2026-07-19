---
audio: false
generated: true
image: false
lang: en
layout: post
title: China-friendly vision models for OpenRouter
translated: false
type: note
---

Question: If ChatGPT/Gemini violate terms for Chinese mainland users, what vision models can I use from OpenRouter?

Answer:

Yes, this is the practical problem. For users in mainland China, **official ChatGPT/Gemini consumer services may have availability restrictions**, and OpenAI explicitly says accessing ChatGPT/API from unsupported countries can result in account blocking or suspension. ([OpenAI Help Center][1]) OpenAI's terms also require users to comply with applicable trade laws and restrictions. ([OpenAI][2])

For a `ww vision-model` CLI, I would avoid depending only on:

```
google/gemini-2.5-flash
openai/gpt-5
anthropic/claude-sonnet-4
```

even though technically they are excellent VLMs.

Better options:

## 1. Qwen-VL (best fit for China users)

OpenRouter:

```bash
qwen/qwen2.5-vl-72b-instruct
```

or:

```bash
qwen/qwen2.5-vl-32b-instruct
```

Architecture:

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

Example:

```bash
ww vision-model test \
  --model qwen/qwen2.5-vl-72b-instruct \
  --max-tokens 1000
```

Good for:

* screenshot understanding
* OCR
* UI agents
* Chinese documents
* charts

---

## 2. Open-source VLMs

Search OpenRouter:

```
vl
vision-language
multimodal
```

Look for:

```
input:
  text
  image

output:
  text
```

Examples:

```
qwen/qwen2.5-vl-72b-instruct
qwen/qwen2.5-vl-32b-instruct
qwen/qwen2.5-vl-7b-instruct
mistralai/pixtral
google/gemma-3
```

---

## 3. Self-host (probably your style)

Since you already run GPUs/training, local VLM is interesting.

RTX 4070 12GB:

Possible:

```
Qwen2.5-VL-3B
Qwen2.5-VL-7B
MiniCPM-V
InternVL
```

Example:

```bash
ollama pull qwen2.5vl:7b

ollama run qwen2.5vl:7b
```

No ToS dependency.

Architecture:

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

## 4. For your `ww` agent use case

I would make the default priority:

```
1. qwen2.5-vl-72b  (cloud)
2. qwen2.5-vl-7b   (local)
3. gemini-2.5-flash (if available)
4. claude-sonnet   (if available)
```

Because screenshot agents mostly need:

* coordinate understanding
* OCR
* UI element detection
* short reasoning

not pure benchmark IQ.

---

A useful OpenRouter filter idea:

```python
for model in models:
    if "image" in model.input_modalities:
        if "text" in model.output_modalities:
            print(model.id)
```

You want:

```
image -> text
```

not:

```
text -> image
```

FLUX was:

```
text -> image
```

which is why your test returned:

```
finish_reason=stop
content=""
```

For a China-friendly AI agent stack, Qwen-VL + local Ollama/vLLM is probably the cleanest path.

[1]: https://help.openai.com/en/articles/9131992-chatgpt-and-api-services-in-unsupported-countries-and-territories?utm_source=chatgpt.com "ChatGPT and API services in unsupported countries and territories | OpenAI Help Center"
[2]: https://openai.com/policies/terms-of-use/?utm_source=chatgpt.com "Terms of Use | OpenAI"
