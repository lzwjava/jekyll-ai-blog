---
audio: false
generated: true
image: false
lang: en
layout: post
title: "CMP 170HX: Poor Man's A100"
translated: false
type: note
---

## Question: Intro to NVIDIA CMP 170HX — the "almost A100" AI accelerator

![Image](https://images.openai.com/static-rsc-4/FHSdxFOE8fxE-hoZI4SdzM9KJtemCgANadIzjqS2C8S0AgUu_-A-1suKUgg0RhCt4ADsdheg6gmNwUSzt7rq8SF5dctPYcyq5lXRBssuhAEqXksNta-cyUvXbCp_5a2QeR1CijhB0c5cUBbsKPp1eEPh3ZRz_jEjoJx_DIXL6cC41RxLV_i4IG6N3D1OTBy-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Hoz66izlEFDWn_7iO41vBUEBTtVFWVwcMUKqRlnPdCuXsIpGoXuKqUGu9COpsslIfvkdVo0vn0fT69LzuIvOAqWwAXbI1z8qJmoaTtG9KoEGxrhiZFrJtwAvrbylvPmKGedZ6Nx9IP4uXUwFIhTvKeb1p3FEwWaW-3VrNiTT4ffldLTWX2TqfKeMUyiWMmwq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dFl_Br3HhcE1_7mV8dWBf3e_KTyUardboGd8cSE0J7sOMXV5_rxFJVe0dB3TD0K5t6CaZm9HN3K4pZ5CzwD7ViEEf29DmG3RQ1hrL75j-e6R-XUqBtxbClj5h5NJfZzXMI1eXGaSig33gxfCGW_n2XzWSenjDlNcri4WnZ81MvItEif_9T4GJOc5V99VNDrC?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5edu3VZlo_pcU8aeIJlabW4Lx0UHAfvsBc7IWcjLX3l2bD5MZylbR2Ct_hlPYJaAKdtOpvotVh5G2Kd6rg7rTkAYlWzcxmh8Cxx6ooMVNnKZPR0jG7YmNj6_BT7t0h7q2jT1SDlTV1pjTao2nQXOvjZiiWhC3ixQPiW8ULL5quAMVf8HtLrhd3d3WRAX0iR3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NMjq2gCfMiaNKijfXyoIAmNqwKWJGOIhp4vsLaUlLUdaWdKVddLFvZuft-mQI3u_hX9yHjQ1AtDeDZErNthSfQy9MAmi4xUdVmw6T-QtJGbuCr-hYzNbdQOk75Vk9IHx4xou0ipzujffnbsEN-X-Du5NyzZLqYrmqxFPA1OZA3_RBvLwPEz_1I2YZUVBDEGB?purpose=fullsize)

## Answer

The **NVIDIA CMP 170HX** is one of the most interesting "accidental AI GPUs" in the second-hand market.

The short version:

> CMP 170HX = a cut-down NVIDIA A100 (GA100) silicon, originally made for crypto mining, but recently unlocked by software to become a ~64GB HBM2e AI accelerator. ([DevQuasar][1])

It is basically a **poor man's A100**.

---

## 1. Origin: why NVIDIA made it

Around 2021, during the crypto mining boom, NVIDIA created the **CMP (Cryptocurrency Mining Processor)** product line.

The CMP 170HX used the same:

* GPU architecture: **Ampere**
* Silicon: **GA100**
* Process: TSMC 7nm
* Memory type: **HBM2e**

The same family powers the famous:

* NVIDIA A100 40GB
* NVIDIA A100 80GB

([DevQuasar][1])

But NVIDIA intentionally crippled it:

| Feature            | A100 PCIe | CMP 170HX       |
| ------------------ | --------- | --------------- |
| GPU die            | GA100     | GA100           |
| CUDA architecture  | SM80      | SM80            |
| HBM2e              | 40/80GB   | 8/10GB exposed  |
| Memory bus         | 5120-bit  | 4096-bit        |
| PCIe               | Gen4 x16  | Gen1 x4         |
| Tensor performance | full      | heavily limited |
| Display            | no        | no              |

([DevQuasar][1])

---

## 2. Why it became famous in 2026

The interesting discovery:

The hardware was not completely destroyed.

NVIDIA mostly used:

* firmware restrictions
* fuse configuration
* protected registers

to disable:

* memory capacity
* compute units
* PCIe speed

The GPU still physically contained much more capability.

([DevQuasar][1])

The community discovered that the restrictions could be bypassed using:

* NVIDIA open kernel drivers
* firmware exploit techniques
* tools like `cmpunlocker`

After unlocking:

Example 8GB CMP 170HX:

```
Before:

VRAM: 8GB
Compute: crippled
PCIe: Gen1 x4


After:

VRAM: ~64GB HBM2e
Compute: close to A100
PCIe: Gen2 x4
```

([GitHub][2])

---

## 3. Why 64GB HBM2e is a big deal for AI

For LLM inference, VRAM is often the bottleneck.

Example:

### Qwen / Llama style models

Approximate memory:

```
7B model FP16:
~14GB

14B FP16:
~28GB

32B FP16:
~64GB
```

So a single unlocked CMP 170HX can potentially run:

* 30B-class models FP16
* 70B-class models quantized
* large embedding models
* inference servers

The important thing is not raw TFLOPS.

It is:

> "Can I fit the model into one GPU?"

A 24GB RTX 4090 is faster, but a 64GB CMP 170HX can hold larger models.

---

## 4. Performance comparison

Rough idea:

| GPU                | VRAM        | AI usefulness               |
| ------------------ | ----------- | --------------------------- |
| RTX 4090           | 24GB GDDR6X | very fast, limited capacity |
| RTX 3090           | 24GB        | good hobby AI GPU           |
| RTX 6000 Ada       | 48GB        | professional                |
| CMP 170HX unlocked | 64GB HBM2e  | cheap large-memory AI       |
| A100 40GB          | 40GB HBM2   | datacenter                  |
| A100 80GB          | 80GB HBM2e  | datacenter                  |

CMP 170HX advantage:

* huge memory bandwidth
* HBM
* ECC-like datacenter design
* 64GB capacity

Disadvantages:

* old Ampere architecture
* no NVLink
* poor PCIe bandwidth
* passive cooling
* weird power connector

([GitHub][2])

---

## 5. Hardware details

The card is unusual:

```
GA100 GPU
 |
 +-- HBM2e stacks
 |
 +-- passive heatsink
 |
 +-- EPS 8-pin power
 |
 +-- no display output
```

It was designed for mining farms.

The 8GB version:

```
PCI ID: 10de:20c2
unlock:
8GB -> 64GB
```

The 10GB version:

```
PCI ID: 10de:2082
unlock:
10GB -> 40GB
```

Important: they are different. Do not assume every CMP 170HX becomes 64GB. ([GitHub][2])

---

## 6. For your AI workstation use case

Given your experiments:

* GPT-2 training
* Qwen models
* vLLM
* llama.cpp
* local inference

CMP 170HX is actually very interesting.

Example:

Your RTX 4070 Ti:

```
12GB VRAM
CUDA 8.9
fast
```

CMP 170HX:

```
64GB VRAM
CUDA 8.0
slower compute
massive memory
```

For:

✅ QLoRA
✅ inference
✅ serving bigger models
✅ experimenting with 30B/70B quantized models

CMP 170HX may be more useful.

For:

❌ image generation speed
❌ CUDA kernel optimization
❌ training small models quickly

RTX 4070/4090 is better.

---

## 7. The current market situation

Before unlocking:

```
$250-$500
```

After the discovery:

```
$1000-$2000+
```

because people realized:

```
cheap mining card
        ↓
A100 silicon
        ↓
64GB HBM AI accelerator
```

([Niconiconi][3])

---

## My view

CMP 170HX is probably one of the biggest "hidden AI hardware arbitrage" discoveries of recent years.

It is not a replacement for H100/B200.

But for a local AI engineer:

```
$1000 CMP 170HX unlocked
vs
$5000+ A100 used
```

the value proposition is extremely attractive.

The main risks are:

1. cooling (passive mining card)
2. driver compatibility
3. second-hand mining abuse
4. unlock software maturity

For someone like you who builds local LLM systems, this card is much more interesting than a normal gaming GPU because **VRAM capacity changes what models you can run**.

[1]: https://devquasar.com/hardware/the-almost-a100-nvidia-cmp-170hx/?utm_source=chatgpt.com "The almost A100 – NVIDIA CMP 170HX – DevQuasar"
[2]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/hardware/board-and-variants.md?utm_source=chatgpt.com "cmp170hx/docs/hardware/board-and-variants.md at main · Consensus-Protocol/cmp170hx · GitHub"
[3]: https://niconiconi.neocities.org/tech-notes/nvidia-cmp-170hx-review/?utm_source=chatgpt.com "All GB/s without FLOPS - Nvidia CMP 170HX Review, Performance Lockdown Workaround, Teardown, Watercooling, and Repair"
