---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slow Download and VRAM Issues
translated: false
type: note
---

Here's the **summary of issues**:

### 1. 🚧 Model is Gated
You had to accept terms on HuggingFace first, then pass a token. *(Fixed ✓ — token works now)*

### 2. 🐢 Extremely Slow Download (~24 GB)
The model is **12 billion parameters** — roughly **24 GB** of weights.
- After **30 minutes**, only **2.3 GB / ~24 GB** was downloaded (~1.3 MB/s)
- At this rate, it would take **~4-5 hours** to finish

### 3. 💾 GPU VRAM Bottleneck
Your GPU has **12 GB VRAM**, but the model needs **~24 GB** in bfloat16.
→ The script uses CPU offloading, which trades VRAM for **much slower inference**.

### Options to speed things up:

| Option | What to do |
|--------|-----------|
| **Let it finish** | Run overnight — download will complete eventually |
| **Use a smaller model** | Try `black-forest-labs/FLUX.1-dev` (same size) or a distilled version |
| **Use an API instead** | https://fal.ai/models/fal-ai/flux/schnell — no download, pay per image |
| **Use a faster connection** | Download elsewhere and copy the cache folder |

Want me to let it continue downloading in the background? Or would you like to try a different approach?