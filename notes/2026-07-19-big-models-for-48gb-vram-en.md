---
audio: false
generated: true
image: false
lang: en
layout: post
title: Big Models for 48GB VRAM
translated: false
type: note
---

Question: What big models can we run with 48GB VRAM (2 × RTX 3090)?

Answer:

Two RTX 3090s give you:

* **VRAM:** 24GB × 2 = **48GB**
* **Memory bandwidth:** ~936 GB/s per card → ~1.9 TB/s aggregate (but depends on parallelism)
* **FP16 compute:** ~35.6 TFLOPS each → ~71 TFLOPS total
* **NVLink:** possible on RTX 3090 (unlike RTX 4070), giving GPU-GPU memory bandwidth boost for supported workloads

The key constraint for LLM inference is:

```
Model memory ≈ parameters × bytes per parameter + KV cache + runtime overhead
```

Typical sizes:

| Model |  FP16 |  INT8 | 4-bit |
| ----- | ----: | ----: | ----: |
| 7B    |  14GB |   7GB |   4GB |
| 13B   |  26GB |  13GB |   7GB |
| 34B   |  68GB |  34GB |  17GB |
| 70B   | 140GB |  70GB |  35GB |
| 100B  | 200GB | 100GB |  50GB |

So 48GB VRAM is actually a very interesting range.

## Comfortable models

### Qwen3 / Qwen2.5 32B

Example:

* Qwen3-32B
* Qwen2.5-Coder-32B

4-bit:

```
32B × 0.5 byte ≈ 16GB
```

With KV cache:

```
~20-25GB
```

A single 3090 can almost run it, two cards run it easily.

Good use:

* coding agent
* local Copilot
* RAG
* fine-tuning LoRA

---

## 70B class models

This is where 48GB becomes useful.

Examples:

* Llama 3.1 70B
* Qwen2.5-72B
* DeepSeek-R1-Distill-70B

4-bit:

```
70B × 0.5 byte = 35GB
```

Runtime overhead:

```
+5-10GB
```

Total:

```
40-45GB
```

So:

```
2 × RTX3090 = yes
```

Typical setup:

```
GPU0: 24GB
GPU1: 24GB

llama.cpp:
--split-mode layer
```

or

```
vLLM tensor parallel = 2
```

You can run 70B quantized models locally.

---

## DeepSeek models

Interesting case.

### DeepSeek-V3

671B parameters.

Even 4-bit:

```
671B × 0.5 byte
≈ 335GB
```

Need:

```
~8-10 × RTX3090
```

not practical.

But:

### DeepSeek-R1-Distill-Qwen-32B

Very practical:

```
32B
4-bit
```

2×3090:

excellent.

---

## Training / fine-tuning

48GB is even more interesting.

### LoRA fine-tuning

Possible:

* 7B full fine tune
* 14B LoRA
* 32B LoRA
* 70B LoRA (with aggressive settings)

Example:

Qwen2.5-Coder-32B:

```
base model:
32B × 2 bytes = 64GB FP16

LoRA:
train only adapters

VRAM:
~35-45GB
```

2×3090 works.

---

## Compared with your RTX 4070 12GB

Your current card:

```
RTX4070
12GB VRAM
```

can run:

* 7B FP16
* 14B Q4
* 32B Q4 barely with offload

2×3090 changes the game:

```
12GB → 48GB
```

A 4x increase.

The practical jump:

```
7B models
        ↓
32B models
        ↓
70B quantized models
```

This is a huge capability jump.

---

## NVLink note

RTX 3090 supports NVLink:

```
3090 GPU0
    |
 NVLink bridge
    |
3090 GPU1
```

But:

* CUDA kernels need to use it
* PyTorch Distributed can use NCCL
* llama.cpp can use multi-GPU without NVLink requirement

For inference:

```
PCIe x16 + x16
```

is often already enough.

For training:

NVLink helps more.

---

For your use case (training small GPTs, agents, local models), **2×3090 is probably the sweet spot in used GPU market**:

* 48GB VRAM
* CUDA ecosystem
* cheap second-hand
* can run Qwen3-32B / Qwen2.5-Coder-32B
* can run 70B Q4 inference
* can do serious LoRA training

It is basically the "poor man's A6000 48GB" setup.
