---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maxwell GPU Upgrade Blocker
translated: false
type: note
---

**The major blocker is the Tesla M40's architecture: Maxwell `sm_52`.**

Everything else is workable. That one fact is what makes this setup fragile:

- **Modern PyTorch/CUDA dropped Maxwell.** CUDA 13 (your driver) no longer targets `sm_52`, and PyTorch removed Maxwell from its `cu128`/`cu129` builds as of 2.8. So the normal `pip install torch` gets you a wheel with **no kernels your GPU can run** — it silently fails at first launch.
- **It forces a frozen stack.** To get Maxwell kernels you must pin `torch==2.7.0+cu126` and Python 3.12. You can't freely upgrade torch without losing the GPU. That's the real cost — not speed, just being locked to an aging toolchain.
- **It drags in the `comfy_kitchen` conflict.** Because you're pinned old, the current `comfy_kitchen` (which needs newer `infer_schema`) nearly broke the install. There's a narrow window (2.7+cu126) where *both* Maxwell kernels and the newer torch API exist — that's the only reason it worked.

Secondary, but not blocking:

- **7 GB RAM** — tight; model loading will swap.
- **Weak FP16** — Maxwell runs fp16 slowly, so fp32 is safer but costs speed/VRAM.

**Bottom line:** the blocker isn't "can it run" — it runs right now. The blocker is **upgradeability**. You're pinned to a legacy corner of the PyTorch/CUDA matrix because your GPU is a 2015 server card whose architecture is end-of-life. A modern 8–12 GB card (RTX 3060 12GB, 4060 Ti 16GB, etc.) would remove the blocker entirely and let you run current torch/Flux/video.

The other practical blocker to *using* it well is that you still need to source a model — I can grab one and benchmark it if you want.
