---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Model option: AWQ or quota?"
translated: false
type: note
---

LibreChat was already cloned successfully earlier — no action needed there.

Which option do you want for the model? Quick summary:

1. **Smaller AWQ model** (~4 GB) — I'll switch to something like `Qwen2.5-7B-Instruct-AWQ` which fits easily. Available now.

2. **Bump RunPod volume quota to 20+ GB** — If you can increase it in RunPod dashboard, I'll re-download the full Gemma 4 26B AWQ.

3. **Stream-load from HF** — Launch SGLang with the model path pointing to the original HuggingFace repo so it loads on-demand, no full download needed (but needs enough VRAM for the FP16 model which is 50GB — won't fit 16GB VRAM).

4. **Use the original Gemma 4 FP16 with SGLang's quantization** — Load `google/gemma-4-26B-A4B-it` and SGLang quantizes on-the-fly to fit VRAM, but still needs the full ~50 GB download first.

Options 1 or 2 are the most realistic. Which way?
