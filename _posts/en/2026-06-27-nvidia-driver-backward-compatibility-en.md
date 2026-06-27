---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA Driver Backward Compatibility
translated: false
type: note
---

Correct. The NVIDIA driver is backward-compatible. Driver 580.x supports CUDA 12.0 through 13.0.

When you install `torch==2.5.1+cu124`, it bundles its own CUDA 12.4 runtime libraries inside the pip package. The driver just needs to be *new enough* to support that CUDA version — 580.x is more than sufficient. No driver install, no system CUDA change.

So yes, this machine can run both:

- System CUDA 13.0 (whatever uses it natively)
- CUDA 12.4 wheels in a venv (torch/triton via pip)

They don't conflict — the venv's CUDA runtime is self-contained, talks to the same driver via the kernel module.
