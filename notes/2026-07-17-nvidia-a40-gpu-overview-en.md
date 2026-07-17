---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA A40 GPU Overview
translated: false
type: note
---

Question: What's NVIDIA A40 GPU?

Answer:

NVIDIA A40 is a **professional workstation / data center GPU** based on the **Ampere architecture** (same generation as RTX 30 series), mainly designed for **AI inference, rendering, simulation, and virtual workstations**.

![Image](https://images.openai.com/static-rsc-4/Vr2K_1Fxu0NxqrfEqt3XE15XYmO5KopWHuuQq6_-CiXM_K_tdKPL15Qg4NMbvZIneiugBAk0rm2sbYb3WlzrwUwZ3kwnMSAVaZegm58gqH8q_lz_MkEvHXuBF35bu0g0ElrcDvy3a4BUxhryVPyc_I8tO7CPTw1p83thtKQT4TlRKgBDv0vTCghok_Ll6d1Z?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4hdQyQuN1rCsxHPmuUzJUiSoTaLIEftk4_nvysfVuyZ8xUDOE9XR6ds2m8-5CHvh0t0zKQkoQJXeWpVZtQxCNyoA4IGhG64t5TEUVku2ZiMWjUeDSbCGnUzR9W2rl9E8L9Q2pQCmuJuTPz0t63rW0rmoiNV4sQ6qs8o5iDAybj2L3RhD3HQhl63jcb-m5rvY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/sCWXd28rq86GYXTG9J1M_88nVZJfOyepSuV0ShwPCTffuyxH9-FK9g7sfc1AjIm2w2bbxjq_RhW_Cv4pDIFqveBXG9vo5l0llZxe-6BX5Ihzzb6P6jPIu54MMad9cu3Vv0eZUJOzLN1lRZq8WBQQYihTpDFrvMfnvUTTHdbgFXwsQe9tDV_SjX-lGeBxYYiK?purpose=fullsize)

Key specs:

|                    | NVIDIA A40                  |
| ------------------ | --------------------------- |
| Architecture       | Ampere                      |
| CUDA cores         | 10,752                      |
| Tensor cores       | 336 (3rd gen)               |
| VRAM               | **48GB GDDR6 ECC**          |
| Memory bus         | 384-bit                     |
| Memory bandwidth   | ~696 GB/s                   |
| FP32               | ~37.4 TFLOPS                |
| Tensor performance | ~149.7 TFLOPS (FP16 Tensor) |
| TDP                | 300W                        |
| Form factor        | Passive PCIe card           |
| NVLink             | No                          |

### Compared with GPUs you care about

| GPU          | VRAM               | Memory    | FP32         | AI use                   |
| ------------ | ------------------ | --------- | ------------ | ------------------------ |
| RTX 4070     | 12GB GDDR6X        | 504 GB/s  | ~29 TFLOPS   | good hobby GPU           |
| RTX 3090     | 24GB GDDR6X        | 936 GB/s  | ~35.6 TFLOPS | excellent LLM hobby card |
| **A40**      | **48GB ECC GDDR6** | 696 GB/s  | ~37.4 TFLOPS | enterprise AI            |
| A6000 Ampere | 48GB ECC GDDR6     | 768 GB/s  | ~38.7 TFLOPS | workstation              |
| H100         | 80GB HBM3          | 3.35 TB/s | ~67 TFLOPS   | frontier training        |

The interesting part is **VRAM**, not raw compute.

For LLM:

* GPT-2 1.5B:

  * RTX 4070 12GB → possible with tricks
  * A40 48GB → easy
* Llama 7B:

  * RTX 4070 → inference with quantization
  * A40 → full FP16 weights (~14GB) + KV cache + larger context
* Llama 70B:

  * A40 → possible with quantization, not ideal
  * H100/A100 class preferred

### A40 vs RTX 3090

For local LLM development:

**A40 advantages**

* 48GB VRAM
* ECC memory
* stable drivers
* server/workstation reliability
* lower power than dual 3090

**RTX 3090 advantages**

* much higher memory bandwidth
* faster training throughput
* cheaper second-hand market
* active cooling (A40 needs server airflow)

A40 is basically:

> "A professional RTX 3090 with twice the VRAM, but slower memory."

### Second-hand market view (2026)

Typical used prices:

* RTX 3090 24GB: ~¥5k-7k CNY
* A40 48GB: ~¥7k-10k CNY (varies)
* A6000 Ampere 48GB: ~¥10k+

For your use case (nanoGPT, distributed training, ROCm experiments, LLM infra):

* **one GPU learning:** RTX 3090 is usually better value
* **large model inference / fine-tuning:** A40's 48GB is very attractive
* **multi-GPU server:** A40 makes more sense because it is passive and designed for racks

A40 is basically the "cheap poor man's A6000/A100" in the used market.
