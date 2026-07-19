---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Tesla P100: Cheap but Niche"
translated: false
type: note
---

Question: How is this NVIDIA Tesla P100 16GB for AI / LLM work?

Answer:

The **Tesla P100 16GB HBM2** is an interesting card, but for your use case (LLM training, inference, experimenting with models), I would rate it as **cheap but niche**.

![Image](https://images.openai.com/static-rsc-4/qto6zAIFd_GTNVRUsX-kg1oGoIVToLf7MD3XeyWArjJbx8UPnnB34jqF88H3O5Ak-SkhKIyqQuIoAnCzac5WJvHhugZ2Uu0Dl_3suqyZjCUfB6TE60CdLCIneueEe_KoW9XvpkEXbyJMZ_zBadc-9J3p5QJpSBQnjEX7VoYE4GCLeA3Bh8d2L7tSe9buGBwV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qmu180eNBOiPhGTWTVN36ruOurN2pPIeKZ1glbP6m9Fh-OIxYK2CblEDopAmfWUabmX9gZXq8V3JRfhJUjK303fbY3Kqta5RSFwE1EZiuRnACKePF3gXHbtwHhfa6Ngmz-H7YbOZasBFKBjze3fMHVwvWs_hrb5CRLbKU_zM5ZEgYCo5bprYng_yyOamhvXv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EYQXAAADYVJ9enj9-yuyPcn-loDIWPV5xvN7sjsIP1lEKzNuPw5MfFBP3quc2kA3mRoxgdMOB_4uQT86--Kp1GvOq7twcFC9Br81WlkwjlkxRgolJYmhn79EdHbWQIZbqsayhKdmBHL6uEjEY7rLL-gsw3AU-2qmqi0PkC-fGpioyVR6WMGPLgongTB86eke?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IS5f-M2Kd-gnnUzQw01iOVH7Nynrl76IsE-rWsWCunokIjiJY5FQ959jmb9EzsSkggZT9Ph_LycWZA1U1CCq4JdrCTalTJ5rmwAb1wmWT_hT9K6ivV2sv6fu3CotkpI1y5_unNoadVIRAadSmNQfztnhNIgPwomhvBDeZjDPgM5oweuy0Bg_YjRr7tpE_YEz?purpose=fullsize)

## Specs

|                    | Tesla P100 PCIe         |
| ------------------ | ----------------------- |
| Architecture       | Pascal (2016)           |
| CUDA cores         | 3584                    |
| VRAM               | 16GB HBM2               |
| Memory bandwidth   | ~549 GB/s               |
| FP32               | ~9.3 TFLOPS             |
| Tensor cores       | ❌ None                  |
| NVLink             | Yes (some SXM versions) |
| PCIe               | Gen3 x16                |
| Power              | ~250W                   |
| Compute capability | 6.0                     |

The important point:

**No Tensor Cores.**

That makes a huge difference for modern AI.

---

## Compared with your RTX 4070

Your RTX 4070:

|              | RTX 4070          | Tesla P100  |
| ------------ | ----------------- | ----------- |
| Architecture | Ada Lovelace      | Pascal      |
| VRAM         | 12GB GDDR6X       | 16GB HBM2   |
| Bandwidth    | 504 GB/s          | 549 GB/s    |
| FP32         | ~29 TFLOPS        | ~9.3 TFLOPS |
| Tensor cores | Yes               | No          |
| CUDA         | 7.5? actually 8.9 | 6.0         |
| BF16         | Good              | Poor        |
| FP16 Tensor  | Excellent         | No Tensor   |

For LLM:

* RTX 4070 is **much faster**
* P100 only wins because of **16GB memory**

---

## What can P100 run?

### Good:

### 1. Small LLM inference

Examples:

* Llama 3 8B quantized
* Qwen2.5 7B
* DeepSeek distilled 7B

With llama.cpp:

```
Q4_K_M
7B model
~5GB VRAM
```

works.

Maybe:

```
14B Q4
~10GB VRAM
```

also works.

---

### 2. CUDA experiments

PyTorch:

```
torch.cuda.is_available()
```

works.

Training:

* nanoGPT 124M
* GPT-2 small
* LoRA fine-tuning

possible.

---

## Bad:

### Modern LLM training

Example:

Qwen3 30B:

No.

Even with 16GB:

* model weights
* gradients
* optimizer states
* KV cache

explode.

---

### Flash attention / modern kernels

Problem:

P100 is compute capability 6.0.

Many modern AI libraries assume:

```
sm_80+
```

(Ampere)

or:

```
sm_89
```

(Ada)

You will hit compatibility issues.

Examples:

* FlashAttention-2 ❌
* some Triton kernels ❌
* many optimized inference engines ❌

---

## Compared with RTX 3090

The real competitor:

NVIDIA GeForce RTX 3090

|               | P100 | RTX 3090  |
| ------------- | ---- | --------- |
| VRAM          | 16GB | 24GB      |
| Tensor cores  | No   | Yes       |
| FP16 AI       | weak | huge      |
| BF16          | No   | Yes       |
| LLM ecosystem | old  | excellent |

RTX 3090 is probably **5-10x better for LLM workloads**.

---

## Price judgement

Depends on price.

If:

### < 500 CNY

Interesting.

Reason:

* cheap CUDA card
* HBM2 is cool
* learning GPU architecture
* old HPC experiments

### 500-1000 CNY

I would hesitate.

A used RTX 3060 12GB is often better:

* newer CUDA
* Tensor cores
* better software support
* lower power

### >1000 CNY

No.

Buy something newer.

---

## For your AI hardware path

Given your previous experiments:

* GPT-2 124M training
* nanoGPT
* wanting 32k/100k context
* considering RTX 3090 / RX7900XT

I would rank:

```
RTX 3090 24GB
    >
RTX 4090 24GB
    >
RTX 3060 12GB
    >
RTX 4070 12GB
    >
Tesla P100 16GB
```

The P100 is a "fun HPC collector card", not a serious 2026 LLM card.

The biggest issue is not VRAM. It is **missing Tensor Cores + old CUDA architecture**. For modern PyTorch, a 12GB Ada card can beat this 16GB HBM card easily.
