---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla K80 and llama.cpp Limitations
translated: false
type: note
---

Question: Can Tesla K80 24GB run llama.cpp?

Answer:

**Technically yes, but practically it is very limited.** The Tesla K80 can run some old `llama.cpp` CUDA builds, but it is a poor choice for modern LLM inference.

## Why it can work

`llama.cpp` mainly needs:

1. CUDA support
2. GPU compute kernels
3. Enough VRAM

The K80 has:

* CUDA Compute Capability: **3.7**
* 24GB total VRAM (2 × 12GB)
* FP16 support (slow)

So an old CUDA-enabled `llama.cpp` version can potentially compile for it.

Example:

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

make GGML_CUDA=1 \
     CUDA_DOCKER_ARCH=compute_37
```

The important part is:

```bash
CUDA_DOCKER_ARCH=compute_37
```

because K80 is `sm_37`.

## The big problem: modern llama.cpp dropped old GPUs

Modern CUDA toolchains and kernels increasingly assume newer architectures:

* CUDA 12 → no Kepler support
* CUDA 11.8 → last realistic option
* newer PyTorch / CUDA libraries → usually fail

You may need:

* older CUDA toolkit
* older NVIDIA driver
* older gcc

Typical environment:

```
Ubuntu 20.04
CUDA 11.8
NVIDIA driver 470.xx
llama.cpp older commit
```

## VRAM reality

The "24GB" is misleading:

```
K80
 ├── GPU0: 12GB
 └── GPU1: 12GB
```

`llama.cpp` sees:

```
GPU0: 12GB
GPU1: 12GB
```

not:

```
GPU: 24GB
```

So:

| Model           | K80                    |
| --------------- | ---------------------- |
| Llama 3.2 1B Q4 | ✅                      |
| Llama 3.2 3B Q4 | maybe                  |
| Llama 7B Q4     | maybe with CPU offload |
| Llama 8B Q4     | difficult              |
| 13B+            | mostly CPU             |

A 7B Q4 model:

```
weights ~4-5GB
KV cache + overhead
```

could fit into one 12GB GPU, but performance is the issue.

## Expected speed

Rough estimate:

| GPU       | Llama 7B Q4 tok/s |
| --------- | ----------------: |
| RTX 4090  |          100-200+ |
| RTX 3090  |            50-100 |
| RTX 4070  |             30-60 |
| Tesla P40 |             15-30 |
| Tesla K80 |              ~2-8 |

The K80 has many CUDA cores, but they are old Kepler cores:

* low clock
* weak FP16
* no Tensor Core
* poor memory efficiency

## Interesting experiment

For your CUDA/kernel learning, K80 is actually fun:

You can experiment with:

* CUDA kernels
* memory bandwidth
* multi-GPU split
* llama.cpp backend modification

The architecture is simple:

```
llama.cpp
    |
    +-- CUDA kernels
          |
          +-- sm_37
                |
                +-- GK210
```

But for your actual LLM lab (nanochat, vLLM, SGLang, DeepSpeed), the K80 is basically a museum piece.

Given your current RTX 4070 12GB, a used **RTX 3060 12GB** as a second GPU would probably be far more useful than a K80. It supports modern CUDA and can actually participate in current AI tooling.
