---
audio: false
generated: true
image: false
lang: en
layout: post
title: Vertex AI's Imagen 4 Models
translated: false
type: note
---

Based on the code snippet you provided, you are using the `genai.Client` to interact with a model for image generation on Vertex AI. The model you've specified is `"imagen-4.0-generate-preview-06-06"`.

Here's a breakdown of what's new and what this model represents:

### The Latest Image Generation Models on Vertex AI

The model you are using, `imagen-4.0-generate-preview-06-06`, is part of the latest **Imagen 4** model family on Vertex AI. This model family also includes:

* **`imagen-4.0-generate-preview-06-06`**: This is the standard Imagen 4 model, offering a balance of speed and quality.
* **`imagen-4.0-ultra-generate-preview-06-06`**: This "Ultra" version is designed for higher quality but is slower and more expensive.
* **`imagen-4.0-fast-generate-preview-06-06`**: This "Fast" variant prioritizes speed and lower latency over the highest possible quality.

These Imagen 4 models are a significant update, building on previous versions like Imagen 3 and Imagen 2. The key features and updates with Imagen 4 include:

* **Improved Image Quality**: The new models are designed to generate images with higher quality compared to their predecessors.
* **Wider Aspect Ratio Support**: Imagen 4 supports several aspect ratios, including `1:1`, `3:4`, `4:3`, `9:16`, and `16:9`, giving you more control over the output.
* **Multilingual Prompting**: While English is the primary language, these models also support text prompts in several other languages, including Chinese (simplified and traditional), Hindi, Japanese, Korean, Portuguese, and Spanish (in preview).
* **Safety Features**: The models include user-configurable safety settings and incorporate digital watermarking (SynthID) to identify AI-generated content.

The `person_generation` and `safety_filter_level` parameters in your code snippet are still relevant and allow you to configure the model's behavior for responsible AI, as you have done with `person_generation="ALLOW_ADULT"` and `safety_filter_level="BLOCK_LOW_AND_ABOVE"`.

### Beyond Image Generation

In addition to the updated Imagen models, Google Cloud has also recently introduced other new generative AI models on Vertex AI, including:

* **Veo 3 and Veo 3 Fast**: These are the latest video generation models, allowing you to create high-quality videos from text or image prompts. Veo 3 is for high-quality, professional videos with features like native audio and lip-syncing, while Veo 3 Fast is optimized for speed.
* **Gemini 2.5 models**: These are the latest versions of the Gemini family of models, including Gemini 2.5 Pro, Gemini 2.5 Flash, and Gemini 2.5 Flash-Lite, offering advanced reasoning, multi-modality, and improved performance for various tasks.
