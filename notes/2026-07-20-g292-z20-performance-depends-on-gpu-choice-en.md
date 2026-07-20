---
audio: false
generated: true
image: false
lang: en
layout: post
title: G292-Z20 Performance Depends on GPU Choice
translated: false
type: note
---

**Question: What token speed and model size can a Gigabyte G292-Z20 8-GPU server run?**

Answer:

The answer depends almost entirely on **which GPUs you put inside**. The G292-Z20 is only the chassis/platform; the GPU choice determines LLM inference speed.

For AI inference, the important numbers are:

```
VRAM capacity  -> model size you can load
GPU compute    -> tokens/sec
GPU interconnect -> multi-GPU scaling
```

---

## Scenario 1: 8 × RTX 3090 24GB (very common used-market build)

Total:

```
8 × 24GB = 192GB VRAM
```

FP16:

```
24GB × 8 = 192GB
```

Quantized:

```
INT4 / Q4:
192GB × ~2 = effectively huge
```

### Models that fit

| Model            | Fits? | Expected speed |
| ---------------- | ----- | -------------- |
| Llama 3.1 8B     | Easy  | 150-300 tok/s  |
| Qwen2.5 14B      | Easy  | 100-200 tok/s  |
| Qwen3 32B        | Easy  | 50-120 tok/s   |
| Llama 3.1 70B Q4 | Yes   | 30-70 tok/s    |
| Qwen2.5 72B Q4   | Yes   | 25-60 tok/s    |
| Mixtral 8x22B Q4 | Yes   | 30-80 tok/s    |

Approximate numbers using vLLM / llama.cpp.

---

## Scenario 2: 4 × RTX 3090

Many people will not populate all 8 slots.

```
4 × 24GB = 96GB VRAM
```

Can run:

| Model  | Speed              |
| ------ | ------------------ |
| 7B-14B | 100+ tok/s         |
| 32B Q4 | 40-80 tok/s        |
| 70B Q4 | possible but tight |

---

## Scenario 3: 8 × Tesla P40 24GB

Cheap Xianyu build:

```
8 × P40
192GB VRAM
```

But older Pascal architecture.

Good for:

* embeddings
* batch inference
* agents

Bad for:

* modern LLM inference

Speed:

```
70B Q4:
~10-25 tok/s
```

because tensor cores are missing.

---

## Scenario 4: 8 × RTX A6000 48GB

This is the dream configuration:

```
8 × 48GB
=
384GB VRAM
```

Can run:

* Llama 405B quantized
* Qwen3 235B quantized
* very large MoE models

Example:

```
Qwen3-235B-A22B
Q4

VRAM:
~150GB

Fits easily
```

Speed:

```
30-80 tok/s
```

depending on framework.

---

# Important: NVLink does NOT exist on RTX 4090 / 4070

The server does not magically combine GPUs.

For example:

```
8 × RTX3090
```

has:

```
192GB VRAM
```

but each GPU still has separate memory.

The framework does tensor parallel:

```
GPU0:
layers 0-10

GPU1:
layers 11-20

GPU2:
layers 21-30
...
```

Communication happens over PCIe.

---

# PCIe bottleneck

G292-Z20 is PCIe based.

Compared:

## A100 SXM

```
GPU <---- NVLink ----> GPU

600GB/s+
```

## RTX3090 server

```
GPU <---- PCIe ----> GPU

~32GB/s
```

So:

* training scaling is worse
* inference is okay

---

# Training capability

For your use case (nanoGPT / small LLM training):

8×3090:

Example:

```
GPT-2 760M
```

Your RTX4070:

```
12GB VRAM
hours
```

8×3090:

```
192GB VRAM

batch size ×16
or ×32

training speed:
~5-8x faster
```

For:

```
7B fine tuning
```

Very comfortable.

---

# The "AI factory" setup

A realistic configuration:

```
Gigabyte G292-Z20
        |
        |
8 × RTX3090
        |
        |
vLLM
        |
        |
OpenAI compatible API
        |
        |
100 agents
```

You could host:

```
Qwen3-32B
+
Qwen3-Coder-30B
+
embedding model
+
reranker
```

simultaneously.

Example:

```
GPU0-3:
Qwen3-32B

GPU4:
embedding

GPU5:
reranker

GPU6-7:
experiments
```

---

## Compared with cloud

A single ¥20k-30k build:

```
8×3090
192GB VRAM
```

is roughly comparable to:

* multiple A10 instances
* one small A100 partition
* several consumer GPU cloud nodes

For experimentation, agents, fine-tuning, and research, it is extremely attractive.

The main limitation is **not compute**; it is **power + cooling + noise**. This machine is closer to a mini AI lab server than a workstation.
