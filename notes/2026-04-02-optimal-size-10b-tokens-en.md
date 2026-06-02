---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Model Size for 10B Tokens
translated: false
type: note
---

For **10B tokens** on an H200:

**124M** → too small. You'd have ~80,000 tokens per parameter — way more than needed, you'll overfit or just memorize. Wastes the GPU.

**500M** → better, but still undersized by Chinchilla scaling laws. For 10B tokens, optimal is closer to **1B-2B**.

**My pick:** Go **1B or 1.5B** — you have the VRAM for it. With `bf16` mixed precision, a 1.5B model should fit comfortably on the H200 with room for a decent batch size.

Quick memory estimate for 1.5B:
- Weights: ~3GB (bf16)
- Adam states: ~12GB
- Gradients + activations: ~20-30GB
- **Total: ~40-50GB** — fits with room to spare

Want me to pull a config for 1.5B from nanoGPT examples?
