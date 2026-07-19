---
audio: false
generated: true
image: false
lang: en
layout: post
title: Buy another RTX 3090 for NVLink
translated: false
type: note
---

Question: If using NVLink, what GPU should you buy instead of adding an RTX 3060?

Answer:

For your **i9-13900KF + RTX 4070** system, NVLink changes the answer completely.

First: **RTX 4070 does not support NVLink.**

The RTX 40 series consumer cards removed NVLink:

| GPU         | NVLink support |
| ----------- | -------------- |
| RTX 3090    | ✅ Yes          |
| RTX 3090 Ti | ❌ No           |
| RTX 4090    | ❌ No           |
| RTX 4080    | ❌ No           |
| RTX 4070    | ❌ No           |
| RTX 3060    | ❌ No           |

So you cannot do:

```
RTX 4070 + RTX 3060 + NVLink
```

There is no connector.

---

## If you want NVLink, buy another RTX 3090

The realistic second-hand AI setup is:

```
RTX 3090 24GB
+
RTX 3090 24GB
```

with NVLink bridge.

![Image](https://images.openai.com/static-rsc-4/IkHwikN9QA4muNyeTGZrzJ2dtez6C-OduZHsv_Yr56HiozSZbiiu297DlmCPLjuu7pzpbR0gFc8bx9JTNFh9O0VjaAD5_3vyqrEY3Y_TEYCO8HQgLTONyqayb8Y2zTrZG1X0eCvlinHucc6R9rQV9nnVU4hKxrkSQd2tJosxevBnWwPem2RHLktVpH6GEiup?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EZT8aeMW8dhwl8kl1T3f93MFe7rpBXkrmeMHv-OWFNgl-M_t3uE0NobapgIl-bVs_zWu1Fdc9s8vqI-JJP3jnYPq25P7LQ3bbeUmY7h7C56Zm3f-mq_THhjkhsEAlCkn-tX3YxA2yw8whtB1bnBWh0_tFH2V7lkBWw6MEMXlhtVFCYpLWdkvrgcsmVYHvSzk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GhDXkJnl1dIyCzfyRpBc9w2Zjm3uhZGGwrgzPm1z7EGrp1t4noVvDc287V7t4fSyWT5C9hzj2zmgU4B_BeJF4B9Be40jpfGW3ReMHiYmwI6VFATEDWq3lP68AzqW1TfMoNo-mR7YVt2fwhBVnIHhtlDzpIBBJIImpgmnM-6Chx5YWwe7iCBK50orWo6Ya8_q?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/I7Vzt-CLMwJ-y2vvlJoD87jeMmZnwXj3cQkZ-gQv11iKyFVXbZrPvlmJAwUUaM2NVePfoBk12WmPRangFF_1TfUgghNR3D-5X-A-I9WjekX5oE6fpzQXR2nXSnnzDXsb0uUmZ3CZ454_RQPRtPMLJX7IP06Nivrie8-SBEa9ZXhUa9Pk1C18a2VEQCWHDem7?purpose=fullsize)

You get:

```
GPU 0:
24GB GDDR6X

GPU 1:
24GB GDDR6X

Total:
48GB VRAM
```

NVLink provides a high-bandwidth GPU-to-GPU connection:

```
PCIe:
CPU
 |
PCIe x16
 |
GPU

GPU <-- PCIe --> GPU
```

versus:

```
NVLink:

GPU0 <=======> GPU1
      high bandwidth
```

This helps for:

* model parallel inference
* some distributed training
* tensor parallel workloads

---

## But there is an important catch

NVLink **does not magically merge VRAM**.

This:

```
2 x RTX 3090

24GB + 24GB
```

does not become:

```
one CUDA device with 48GB
```

CUDA sees:

```python
torch.cuda.device_count()

2
```

You need software support:

* DeepSpeed ZeRO
* Megatron-LM tensor parallel
* vLLM tensor parallel
* HuggingFace Accelerate

Example:

```bash
vllm serve Qwen2.5-32B \
 --tensor-parallel-size 2
```

then:

```
GPU0:
layers 0-?

GPU1:
layers ?-?
```

---

## Compared with RTX 4070 + RTX 3060

Your current:

```
RTX 4070
12GB
+
RTX 3060
12GB

= 24GB total
```

Cheap, but:

* no NVLink
* mixed GPU generations
* slower communication

3090 pair:

```
RTX 3090
24GB
+
RTX 3090
24GB

= 48GB
```

Much better for LLM work.

---

## Power requirement

Your current PSU:

```
750W
```

is not enough.

3090:

```
RTX 3090:
350W

two:
700W

CPU:
250W

system:
100W
```

Peak:

```
~1000W
```

You want:

```
1200W PSU
```

minimum.

Examples:

* Corsair HX1200
* Seasonic PRIME TX-1300
* Super Flower Leadex 1200W

---

## Motherboard requirement

For dual RTX 3090:

You need:

```
PCIe slot spacing:

GPU1
|
3-slot gap
|
GPU2
```

Most normal ATX boards are too cramped.

Better:

* ASUS ProArt Z790-Creator WiFi
* Gigabyte Z790 AORUS Master
* MSI MEG Z790 ACE

These have wider spacing.

---

## For your specific situation

Given you already have RTX 4070:

I would **not** buy RTX 3060.

The choices:

### Option A — cheapest AI expansion

```
RTX 4070
+
RTX 3090
```

Pros:

* 36GB total VRAM
* CUDA
* one modern + one large VRAM card

Cons:

* no NVLink
* mixed GPUs

This is probably the sweet spot.

---

### Option B — serious local LLM workstation

Sell RTX 4070:

```
2 x RTX 3090 24GB
NVLink
```

You get:

```
48GB VRAM
```

Can run:

* Llama 70B quantized
* Qwen 72B quantized
* larger context inference

---

### Option C — keep RTX 4070

Honestly, for your workload (nanoGPT training, LoRA, agent development), I would do:

```
Current:
RTX 4070 12GB

Add:
RTX 3090 24GB
```

Total:

```
36GB VRAM
```

Use:

* RTX 3090 → LLM inference/training
* RTX 4070 → experiments/display

This gives much more value than RTX 3060.

The RTX 3090 second-hand market exists exactly because it is still one of the cheapest ways to get **24GB CUDA VRAM**.
