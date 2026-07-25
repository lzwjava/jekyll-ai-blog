---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bug Fixes and System Updates
translated: false
type: note
---

Fixed! Here's what was wrong and what I fixed:

### Issues found & fixed

**1. `_generate_scenes` didn't pass `api_key`** — The scene generation (LLM call to create titles/subtitles/prompts) called `_openrouter_chat` without the API key, so it always fell back to the env var. Added `api_key` param through the whole chain.

**2. No default LLM model for video generation** — `generate_video_from_content` had no fallback model when `model=None`. Added default to `openrouter/auto-beta` (same as the content generation endpoint).

**3. Import race condition in `LocalGPUProvider`** — Multiple parallel threads tried to `import diffusers` simultaneously. The first ones hit `AttributeError: module 'diffusers' has no attribute 'FluxPipeline'` due to a partial import race. Fixed by pre-loading the model on a single thread before launching the thread pool.

**4. Missing `ffmpeg` on remote** — The video assembly needs `ffmpeg`. Installed it.

### Usage

```bash
# Open the frontend
open https://rc-26cc80c1b835b7a3.radeon.firstdg.ai

# Paste your OpenRouter API key in the 🔑 field, click Check
# Select 🖥️ Local GPU (FLUX.1-schnell is pre-selected)
# Enter a topic, Generate ✨, review content, then Generate Video 🎬
```
