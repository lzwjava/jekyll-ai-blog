---
audio: false
generated: true
image: false
lang: en
layout: post
title: Local image generation projects
translated: false
type: note
---

Question: Which projects let me generate images locally, since llama.cpp only handles text and can't produce images?

Answer:

llama.cpp is built for text language models. It can accept images as input with multimodal models, but it can't generate them, so that reply was correct. Image generation needs diffusion models, which run in separate projects.

**Closest to llama.cpp**
- **stable-diffusion.cpp**: a C/C++ project built on the same ggml library, with GGUF quantization and CPU, CUDA, Metal and Vulkan backends. It's the best fit if you like llama.cpp's lightweight approach.

**Full-featured UIs (easiest to get started)**
- **ComfyUI**: a node-based workflow tool and the most actively developed. It supports most current open models (SDXL, Flux, and others).
- **Fooocus**: very simple, with Midjourney-like prompting and minimal settings.
- **InvokeAI**: a polished interface with a canvas for inpainting and editing.
- **AUTOMATIC1111 WebUI**: the long-standing classic, with a large extension ecosystem.

**For developers**
- **Hugging Face Diffusers**: a Python library for scripting image generation in your own code.

**Practical tips**
- Models come from Hugging Face or Civitai. Check each model's license.
- An NVIDIA GPU with 8 GB or more of VRAM is comfortable for SDXL-class models. Smaller GPUs, CPU-only machines and Apple Silicon can still work with quantized models, just more slowly.
- For a quick start, Fooocus or ComfyUI is simplest. For a llama.cpp-style command-line workflow, use stable-diffusion.cpp.

If you tell me your OS and GPU, I can suggest the best option and give install steps.

References:
- [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Fooocus](https://github.com/lllyasviel/Fooocus)
- [InvokeAI](https://github.com/invoke-ai/InvokeAI)
- [AUTOMATIC1111 Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Hugging Face Diffusers](https://github.com/huggingface/diffusers)
