---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ternary Bonsai 2-27B Features
translated: false
type: note
---

**Question:** What is Ternary-Bonsai-2-27B-gguf, and what makes it notable?

**Answer:**

**Ternary Bonsai 2 27B** is a highly compressed large language model released by **Prism ML**, designed to run full 27B-class reasoning on consumer hardware like laptops and single GPUs. Here's a breakdown of what makes it interesting:

---

### What it is

It is a text-generation model built with ternary (2-bit-ish) weight representation, compatible with llama.cpp on CUDA, Metal, and CPU.

The base model is derived from **Qwen3.8-27B**, a 27B hybrid-attention causal language model, with its architecture unchanged.

---

### The key innovation: Ternary Weights

Each weight takes a value from {−1, 0, +1}, with one shared FP16 scale factor for every group of 128 weights. A ternary value carries log₂3 ≈ 1.585 bits of information, giving an effective storage cost of ~1.71 bits/weight — an idealized ~9.3x reduction versus FP16.

The weights are stored in a **rotated basis**: each matrix is transformed blockwise by an orthogonal Hadamard rotation before ternary assignment, and the runtime applies the matching transform to activations at inference time, at no extra memory cost.

---

### Size and Intelligence Retained

The model shrinks from ~54 GB (FP16) down to **5.95 GB** (PTQ1_0 dense packing) or **7.21 GB** (PQ2_0 packing), while retaining **98.2% of FP16 intelligence** — scoring 84.78 average across 14 thinking-mode benchmarks.

Compared to other compressed builds of the same base model:

The conventional "2-bit" IQ2_XXS build is actually 2.8 bits/weight at 9.4 GB, yet scores only 72.59 on the same 14 benchmarks. Bonsai 2 outscores it by more than **12 points at less than two-thirds the size**.

---

### Performance on Hardware

On an Apple M5 Max laptop, the model runs at approximately **47 tokens/second**. On an RTX 5090, it reaches ~130 tok/s. On a low-power 72W L4 datacenter GPU, it still manages ~30 tok/s.

The model also supports a **262K-token context window**, kept practical on-device thanks to its hybrid-attention backbone (~75% linear attention).

---

### Two GGUF Packings

**PTQ1_0** packs trits densely (1.75 bits/weight, 5.95 GB) and is faster on Ada-generation GPUs and the L4. **PQ2_0** stores each trit in a 2-bit slot (2.13 bits/weight, 7.21 GB) and is faster on H100, A100, Blackwell cards, and for prompt processing everywhere.

---

### Important caveat

Stock llama.cpp **cannot run** these files — they require the custom [PrismML-Eng/llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp), which contains the ternary hybrid-attention kernels. Standard llama.cpp will either reject the files or silently produce garbage output.

---

**References:**

- [prism-ml/Ternary-Bonsai-2-27B-gguf · Hugging Face](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- [Bonsai Demo & Examples (GitHub)](https://github.com/PrismML-Eng/Bonsai-demo)
- [PrismML llama.cpp Fork](https://github.com/PrismML-Eng/llama.cpp)
