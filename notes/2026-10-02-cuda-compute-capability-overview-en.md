---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA Compute Capability Overview
translated: false
type: note
---

**CC** = **Compute Capability** (or CUDA Compute Capability).

It's NVIDIA's version numbering for GPU architecture features:

| CC | Architecture | Era |
|----|-------------|-----|
| **3.0** | Kepler | 2012 |
| **3.5** | Kepler (K80) | 2014 |
| **5.0–5.2** | **Maxwell ← Your M40** | 2015 |
| **6.0–6.2** | Pascal (P100, P40) | 2016 |
| **7.0–7.5** | Volta / Turing (V100, T4) | 2018 |
| **8.0–8.9** | Ampere (A100, A6000) | 2020 |
| **9.0** | Hopper (H100) | 2023 |
| **10.0** | Blackwell | 2024 |

Each higher CC means:
- **Newer CUDA features** (like sparse tensor ops, bfloat16 hardware, etc.)
- **Frameworks set a minimum CC** — PyTorch and vLLM require **CC 7.0+**
- **llama.cpp works** because it writes its own raw CUDA kernels, so it can target CC 5.2 directly

Your M40 (CC 5.2) is stuck in the **Maxwell era** — too old for modern ML frameworks, but still capable when you don't go through PyTorch.
