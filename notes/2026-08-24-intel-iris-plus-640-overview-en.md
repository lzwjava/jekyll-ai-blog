---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intel Iris Plus 640 Overview
translated: false
type: note
---

Question: **What is Intel Iris Plus Graphics 640?**

Answer: **Intel Iris Plus Graphics 640** is an integrated GPU (iGPU) from Intel's **7th-generation Kaby Lake** era, launched around **2016–2017**.

### Quick specs

| Spec            | Iris Plus Graphics 640              |
| --------------- | ----------------------------------- |
| Architecture    | Intel Gen9.5                        |
| CPU generation  | Kaby Lake (7th gen Core)            |
| Execution Units | **48 EUs**                          |
| Max clock       | ~1.0–1.05 GHz, depending on CPU     |
| VRAM            | **Shared system RAM**               |
| API             | DirectX 12, OpenCL 2.1              |
| FP32            | roughly **0.4–0.5 TFLOPS**          |
| Typical systems | MacBook Pro, MacBook, Intel laptops |
| Power           | Very low; integrated into CPU       |

The important distinction is that this **doesn't have dedicated VRAM** like your RTX 4070. It uses part of the computer's DDR4/LPDDR3 memory.

### Where it sits in GPU performance

Very roughly:

```text
RTX 4070                  ████████████████████████
GTX 1060                  ███████████
GTX 1050                  ███████
Iris Xe 96 EU             ████
Iris Plus 640             ██
Intel HD 620              █
```

So Iris Plus 640 is **not remotely comparable to a modern discrete GPU**.

It's primarily designed for:

* desktop rendering
* video playback
* 4K video output
* light Photoshop/video work
* older/light games
* very lightweight ML experimentation

### For ML / LLM work

This is the important part for you:

**Don't consider Iris Plus 640 a practical CUDA/LLM GPU.**

It has no NVIDIA CUDA support, only Intel's GPU compute ecosystem. Its compute capability is tiny by modern LLM standards.

For example, even a relatively small model:

```text
7B parameters × 2 bytes (BF16)
≈ 14 GB just for weights
```

Iris Plus 640 doesn't have anything remotely like that amount of dedicated high-bandwidth memory.

If you're seeing this GPU in a machine inventory, I'd interpret it as:

> **"This is an old Intel laptop/desktop iGPU, useful for display/video and basic graphics, not serious GPU compute."**

The interesting thing is that **Iris Plus 640 was actually a fairly good iGPU for its time**—it was substantially faster than Intel HD Graphics 620 because Intel increased the EU count from 24 → **48 EUs**.