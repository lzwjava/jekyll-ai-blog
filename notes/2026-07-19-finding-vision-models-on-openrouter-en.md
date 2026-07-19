---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding Vision Models on OpenRouter
translated: false
type: note
---

Question: How can I find **image analysis (vision-language) models** instead of **image generation models** on OpenRouter?

Answer:

OpenRouter does not separate them perfectly in the UI, so use these methods.

## 1. Search by model capability, not "image"

Avoid:

```
image model
image generation
flux
stable diffusion
```

Those are mostly generators.

Search:

```
vision
multimodal
image understanding
vision-language
VLM
```

Good VLM examples:

| Model                          | Type | Use                     |
| ------------------------------ | ---- | ----------------------- |
| `google/gemini-2.5-flash`      | VLM  | image + text → text     |
| `google/gemini-2.5-pro`        | VLM  | complex image reasoning |
| `anthropic/claude-sonnet-4`    | VLM  | document/image analysis |
| `openai/gpt-5`                 | VLM  | image understanding     |
| `qwen/qwen2.5-vl-72b-instruct` | VLM  | open vision model       |
| `qwen/qwen2.5-vl-32b-instruct` | VLM  | cheaper                 |

---

## 2. Check OpenRouter model page

A vision model should show something like:

```
Input modalities:
  text
  image

Output modalities:
  text
```

You want:

```
image -> text
```

Not:

```
text -> image
```

Generation models usually show:

```
Input:
 text

Output:
 image
```

Examples:

```
black-forest-labs/flux.2-pro
stabilityai/stable-diffusion
openai/dall-e
```

These are NOT vision models.

---

## 3. Use OpenRouter API model list

You can query:

```bash
curl https://openrouter.ai/api/v1/models | jq .
```

Then filter:

```bash
curl https://openrouter.ai/api/v1/models \
 | jq '.data[] | select(.architecture.input_modalities | contains(["image"])) | .id'
```

You should see models like:

```
google/gemini-2.5-flash
anthropic/claude-sonnet-4
qwen/qwen2.5-vl-72b-instruct
```

---

## 4. For your `ww vision-model test`

I would test:

```bash
ww vision-model test \
  --model google/gemini-2.5-flash \
  --max-tokens 1000
```

or:

```bash
ww vision-model test \
  --model qwen/qwen2.5-vl-72b-instruct \
  --max-tokens 1000
```

Expected output:

```
Response:
The image is a blue square with a slight gradient...
finish_reason=stop
```

That `finish_reason=stop` is normal. The problem before was:

```
content=""
```

because FLUX has no text output.

---

For your use case (CLI agent screenshot understanding, `ww vision-model`), the ranking is probably:

1. Gemini 2.5 Flash — cheap + fast
2. Qwen2.5-VL — good OpenRouter option, China-friendly
3. Claude Sonnet 4 — strong reasoning
4. GPT-5 vision — strongest but expensive

FLUX should be moved to a separate command like:

```
ww image-generate test --model black-forest-labs/flux.2-pro
```

not `vision-model`.
