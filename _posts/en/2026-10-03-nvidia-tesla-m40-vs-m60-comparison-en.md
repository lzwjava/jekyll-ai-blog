---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nvidia Tesla M40 vs M60 Comparison
translated: false
type: note
---

Question: Compare NVIDIA Tesla M60 and M40 chip cards.

Answer:

Tesla **M40** and **M60** are both **Maxwell-generation (compute capability 5.2)** Tesla cards from around 2015, but they target different workloads. M40 is a **single large GPU for compute/AI**, while M60 is basically **two smaller GPUs for virtualization/graphics**. ([NVIDIA Docs][1])

|                  | Tesla M40                      | Tesla M60                 |                 |
| ---------------- | ------------------------------ | ------------------------- | --------------- |
| Architecture     | Maxwell GM200                  | 2 × Maxwell GM204         |                 |
| Purpose          | HPC / machine learning compute | VDI / virtual workstation |                 |
| CUDA cores       | 3072                           | 4096 total (2048 × 2)     |                 |
| VRAM             | 12GB or 24GB GDDR5             | 16GB GDDR5 (8GB per GPU)  |                 |
| Memory bus       | 384-bit                        | 2 × 256-bit               |                 |
| Memory bandwidth | ~288 GB/s                      | ~320 GB/s total           |                 |
| FP32             | ~6.8 TFLOPS                    | ~9.6 TFLOPS total         |                 |
| TDP              | 250W                           | 300W                      |                 |
| PCIe             | PCIe 3.0 x16                   | PCIe 3.0 x16              |                 |
| GPU count        | 1 chip                         | 2 chips                   | ([Microway][2]) |

## Chip difference

### Tesla M40

```
GM200
 |
 +-- 24 SM
 |
 +-- 3072 CUDA cores
 |
 +-- 12/24GB GDDR5
```

It is the same GPU family as Titan X Maxwell.

Advantages:

* Large single GPU memory space
* 24GB version exists
* Better for CUDA compute
* Better for LLM inference experiments (within Maxwell limits)

Disadvantages:

* Old architecture
* No FP16 acceleration (important for modern LLMs)
* No tensor cores
* Only compute capability 5.2

### Tesla M60

```
GPU0: GM204 8GB
GPU1: GM204 8GB

Total:
16GB VRAM
4096 CUDA cores
```

The OS sees it as **two separate GPUs**, not one 16GB GPU.

Example:

```bash
nvidia-smi

GPU 0: Tesla M60 8192 MiB
GPU 1: Tesla M60 8192 MiB
```

You cannot run a model needing 12GB VRAM on "M60 16GB" because each GPU only has 8GB.

Good for:

* Multiple users
* VDI
* Rendering
* Parallel small workloads

Bad for:

* LLM inference
* Large CUDA workloads needing unified memory

([NVIDIA][3])

## For llama.cpp / LLM usage

Between them:

### M40 24GB wins

Example:

```
M40 24GB
        |
        | llama.cpp
        |
        +-- 13B Q4 model (~8GB)
        +-- 30B Q4 model (~18GB)
```

M60:

```
M60

GPU0 8GB
GPU1 8GB

Cannot combine easily

```

A 13B model may fit on one M60 GPU, but you lose the second GPU unless software supports multi-GPU splitting.

## Performance comparison for AI

Approximate:

```
Modern RTX 4090

FP16 Tensor:
330+ TFLOPS

Tesla M40:

FP32:
6.8 TFLOPS

Tesla M60:

FP32:
9.6 TFLOPS
```

The gap is enormous because Maxwell has no Tensor Cores.

For LLM:

```
RTX 3090 24GB
    >>> M40 24GB
    >>> M60
```

But for cheap experimentation:

```
M40 24GB:
good VRAM/$

M60:
mostly interesting for GPU repair/testing
```

## Power / hardware

M40:

* Needs strong PSU
* Usually passive cooling
* Needs server airflow

M60:

* Also server card
* 300W
* Dual GPU means more heat density

Both have:

* no display output
* PCIe x16
* old NVIDIA drivers required

([NVIDIA][3])

## My ranking for your GPU lab / LLM experiments

Given your interest in llama.cpp, nano-vLLM, old Tesla cards:

```
Tesla P40 24GB  >>>  Tesla M40 24GB  >>>  Tesla M60  >>> Tesla K80
```

Reasons:

* P40: Pascal, 24GB, better CUDA support
* M40: Maxwell, but 24GB single GPU
* M60: two 8GB GPUs
* K80: 2×12GB but very slow Kepler

M40 24GB is actually a more interesting "cheap VRAM monster" card than M60 for local LLM experiments.

[1]: https://docs.nvidia.com/datacenter/tesla/pdf/NVIDIA_Data_Center_GPU_Driver_Release_Notes_450_v6.0.pdf?utm_source=chatgpt.com "NVIDIA Data Center GPU Driver version 450.156.00 (Linux) / 453.23 (Windows)"
[2]: https://www.microway.com/knowledge-center-articles/in-depth-comparison-of-nvidia-tesla-maxwell-gpu-accelerators/?utm_source=chatgpt.com "In-Depth Comparison of NVIDIA Tesla \"Maxwell\" GPU Accelerators - Microway"
[3]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/nvidia-m60-datasheet.pdf?ncid=no-ncid&utm_source=chatgpt.com "Data Sheet: Tesla M60"
