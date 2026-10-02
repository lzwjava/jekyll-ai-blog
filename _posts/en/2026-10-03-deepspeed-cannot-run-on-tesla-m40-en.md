---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSpeed Cannot Run on Tesla M40
translated: false
type: note
---

No, **DeepSpeed cannot run** on the Tesla M40. Two hard blockers:

### 1. PyTorch Dependency

DeepSpeed is a PyTorch library. PyTorch dropped CC 5.x support years ago:

| PyTorch | Min CC | Your M40 |
|---------|--------|----------|
| 1.10+ | **6.0** (Pascal) | ❌ |
| 2.x | **7.0** (Volta) | ❌ |

### 2. System RAM

DeepSpeed needs significant host memory for optimizer states, gradient accumulation, data loading, etc. Your machine has **only 3.2GB total** — nowhere near enough.

---

**Bottom line:** Anything that depends on **PyTorch** is out. That's why llama.cpp (which talks to CUDA directly without PyTorch) is the right tool for this hardware.
