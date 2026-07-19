---
audio: false
generated: true
image: false
lang: en
layout: post
title: Using image generator for vision test
translated: false
type: note
---

Question: Why does my `ww vision-model test` always get `finish_reason=stop` with empty response?

Answer:

The main issue is likely **model type mismatch**.

You tested:

```
--model black-forest-labs/flux.2-pro
```

`FLUX.2-pro` is an **image generation model**, not a **vision-language model (VLM)**.

Your test sends:

```
image + text prompt
        ↓
expecting:
text response describing/analyzing image
```

But FLUX expects:

```
text prompt
        ↓
generated image
```

So the API can legally return:

```
finish_reason=stop
content=""
```

because there is no textual answer channel.

Use a real vision-language model instead:

Examples:

```
google/gemini-2.5-flash
google/gemini-2.5-pro
openai/gpt-5
anthropic/claude-sonnet-4
qwen/qwen2.5-vl-72b-instruct
```

For OpenRouter style testing:

```bash
ww vision-model test \
  --model google/gemini-2.5-flash \
  --max-tokens 1000
```

Your test image is also extremely small:

```
64x64 blue square
```

A VLM will probably answer something like:

> "The image is a solid blue square."

---

Also check your request handling. Many vision APIs require image content in this format:

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

Not:

```json
{
  "prompt": "Describe image",
  "image": "..."
}
```

---

Your warning is unrelated:

```
RequestsDependencyWarning:
urllib3 ... doesn't match supported version
```

It only means your Python dependency versions are unusual. It won't cause empty model output.

A good debugging sequence:

```bash
# 1. Test text model
ww vision-model test --model google/gemini-2.5-flash

# 2. Test image understanding model
ww vision-model test --model qwen/qwen2.5-vl-72b-instruct

# 3. Test image generation separately
ww image-model test --model black-forest-labs/flux.2-pro
```

So the short version:

**FLUX is the wrong category. It generates images; it does not look at images and describe them.** Use Gemini/Qwen-VL/Claude/OpenAI vision models for `vision-model`.
