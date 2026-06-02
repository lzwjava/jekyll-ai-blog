---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Gen AI Image Config
translated: false
type: note
---

Here’s a quick overview: the `image_size` parameter isn’t supported in the Google Gen AI (Gemini/Imagen) Python SDK. Instead, you select among model variants (which each have implicit default resolutions), control the **aspect ratio**, and—if you need higher pixel counts—apply an **upscale**. You can also tweak **compression** and **output format**, plus the usual “number of images,” “negative prompt,” “safety” and “person” settings.

## Model Variants

You choose a model name—each variant has its own default resolution and performance profile:

* **imagen-3.0** family:

  * `imagen-3.0-generate-002`
  * `imagen-3.0-generate-001`
  * `imagen-3.0-fast-generate-001`
  * `imagen-3.0-capability-001`
* **imagen-4.0 (Preview)** family:

  * `imagen-4.0-generate-preview-06-06`
  * `imagen-4.0-fast-generate-preview-06-06`
  * `imagen-4.0-ultra-generate-preview-06-06`
* **Legacy**: `imagegeneration@002`, `@005`, `@006` ([Google Cloud][1])

## Default Resolution

By default, a square (“1:1”) output from these models is **1024 × 1024 pixels**. If you need a smaller file, you can downsample locally; if you need higher resolution, see **Upscaling** below. ([raymondcamden.com][2])

## Aspect Ratios

Rather than specifying absolute dimensions, use the `aspect_ratio` field in your `GenerateImagesConfig`. Supported values:

* `1:1` (square)
* `3:4` (taller, social-media portrait)
* `4:3` (classic photography/TV)
* `16:9` (widescreen landscapes)
* `9:16` (tall/portrait, e.g. phone backgrounds) ([Google Cloud][1], [Google AI for Developers][3])

You’ll find the same list documented in community tutorials:

* DataCamp points out those exact five ratios for Imagen 3 ([DataCamp][4])
* CodeSignal’s guide also enumerates them for Gemini/Imagen ([CodeSignal][5])

## Upscaling

If you need true “2K” or “4K” outputs, call the **upscale** mode:

```python
from google.genai import types
config = types.GenerateImagesConfig(
    mode="upscale",
    upscale_config=types.UpscaleConfig(upscale_factor="x2"),
)
```

* `"x2"` doubles each dimension (e.g. 1024 → 2048, roughly 2K)
* `"x4"` quadruples (e.g. 1024 → 4096, roughly 4K) ([Google Cloud][1])

## Compression & Formats

* **JPEG quality**: use `compression_quality` (0–100, default 75) to trade off file size vs. detail ([Google Cloud][1])
* **MIME types**: via `output_options.mime_type`, you can choose
  `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `image/bmp`, `image/tiff`, or `image/vnd.microsoft.icon` ([Google Cloud][6])

## Additional Config Options

Everything else lives in `GenerateImagesConfig`:

```python
config = types.GenerateImagesConfig(
    number_of_images=1,           # how many images to generate
    seed=1234,                    # for deterministic outputs
    enhance_prompt=True,          # LLM-based prompt rewriting
    negative_prompt="exclude dogs",
    language="en",
    safety_filter_level="block_medium_and_above",
    person_generation="allow_adult",
)
```

These let you control randomness, prompt enhancement, safety thresholds, and whether the model can include people. ([Google Cloud][1])

## Recommendation

Remove your `image_size="2K"` line—there is no such flag. Instead:

1. **Pick the right model** for speed vs. quality.
2. Use **`aspect_ratio`** for framing.
3. If you truly need higher pixel counts, generate at base resolution then apply the built-in **upscale** (“x2” or “x4”).
4. Tweak **compression\_quality** or downsample locally for smaller files.

With these knobs you can achieve square or cinematic framing, small or high-res outputs, without an unsupported `image_size` parameter.

[1]: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api "Generate images  |  Generative AI on Vertex AI  |  Google Cloud"
[2]: https://www.raymondcamden.com/2025/01/30/generative-ai-images-with-gemini-and-imagen-an-introduction?utm_source=chatgpt.com "Generative AI Images with Gemini and Imagen"
[3]: https://ai.google.dev/gemini-api/docs/imagen?utm_source=chatgpt.com "Generate images using Imagen | Gemini API | Google AI for ..."
[4]: https://www.datacamp.com/tutorial/imagen-3 "Imagen 3: A Guide With Examples in the Gemini API | DataCamp"
[5]: https://codesignal.com/learn/courses/creating-images-with-geminis-imagen-and-flask/lessons/generating-a-simple-image-with-geminis-imagen-and-flask?utm_source=chatgpt.com "Generating a Simple Image with Gemini's Imagen and Flask"
[6]: https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images?utm_source=chatgpt.com "Generate images using text prompts"
