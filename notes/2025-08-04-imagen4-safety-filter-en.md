---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use 'BLOCK_LOW_AND_ABOVE' Only
translated: false
type: note
---

You're seeing this error:

```
Only block_low_and_above is supported for safetySetting.
```

This happens when you set `safety_filter_level="BLOCK_MEDIUM_AND_ABOVE"` (or any other value) in `GenerateImagesConfig` for the **Imagen‑4** models—but at the time of your request (August 2025), **the API only allows `"BLOCK_LOW_AND_ABOVE"`** for image safety filtering on those models ([Google Cloud][1]).

---

### ✅ How to fix your code

Simply update the `safety_filter_level` to the supported value:

```python
from google import genai
from google.genai.types import GenerateImagesConfig

client = genai.Client()

image = client.models.generate_images(
    model="imagen-4.0-generate-preview-06-06",
    prompt="A dog reading a newspaper",
    config=GenerateImagesConfig(
        image_size="2K",
        number_of_images=1,
        safety_filter_level="BLOCK_LOW_AND_ABOVE",
        person_generation="ALLOW_ADULT",
    ),
)

image.generated_images[0].image.save("output-image.png")
print(
    f"Created image using {len(image.generated_images[0].image.image_bytes)} bytes"
)
```

* `safety_filter_level="BLOCK_LOW_AND_ABOVE"`: only this is supported for **Imagen 4**. Other thresholds like `"BLOCK_MEDIUM_AND_ABOVE"` will cause the 400 INVALID\_ARGUMENT error ([Medium][2], [Google AI for Developers][3]).
* `number_of_images=1` is explicit so it’s clear you're requesting one image per call.

---

### 🧾 Other optional parameters

* `person_generation="ALLOW_ADULT"` is the default setting, but it's fine to be explicit (blocks children; allows adult-domaint images) ([Google Cloud][1]).
* `image_size="2K"` is valid per your code—just make sure your SDK version supports it.

---

### TL;DR — Quick checklist

| Step | What to do                                                   |
| ---- | ------------------------------------------------------------ |
| ✅ 1  | Change safety\_filter\_level to `"BLOCK_LOW_AND_ABOVE"`      |
| 🧾 2 | Keep `person_generation="ALLOW_ADULT"` (or omit for default) |
| 🚫 3 | Don’t use `"BLOCK_MEDIUM_AND_ABOVE"` or `"BLOCK_ONLY_HIGH"`  |
| ⏱ 4  | Don’t change safety again until Google adds more levels      |

Let me know if you get another error—happy to help!

[1]: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api?utm_source=chatgpt.com "Generate images | Generative AI on Vertex AI"
[2]: https://medium.com/generative-ai/3-ways-to-try-googles-imagen-4-image-generator-if-you-re-outside-the-us-ee2a1895ca9b?utm_source=chatgpt.com "3 Ways to Try Google's Imagen 4 Image Generator if You're ..."
[3]: https://ai.google.dev/gemini-api/docs/migrate?utm_source=chatgpt.com "Migrate to the Google GenAI SDK - Gemini API"
