---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla K80 24GB GPU Intro
translated: false
type: note
---

Question: Intro to Tesla K80 24GB card

Answer:

![Image](https://images.openai.com/static-rsc-4/if4aBVESRw9nDn8XhY8eRIK2PBvo_qmXyd5UMaRf3YWhiIO3MdQqQ6ffnnIok9A_RwnPvQCl7Y24TDB1bKM2jzJvW2wz-88i09vSIRXyMjGNIpVsiAotVD5Lb2xWwfma3syjH78NXb19sYTxKp3ERWJFcb3PvvDtYdWdFLUIYT2VwosFjDs4fDaHbaj_UGS2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UjvA-wbgCw9VgUBjhNvrdu6rhWXbHOsvhPECnqRBIk3gAmrGCkoARWo-6uVSfKgwf8xi5gHQggUtLDEM8pjhDe-uPIeKs6_HWex3j3HAmaYqEm3WShkZMZ3eryDtniq6w4BzzKK0W6E8FX7ARLaqrER7oGO1_J82Id34gpS5Cd7xGdXmbMVVVMKs-WBmFCb-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/trCkX4jQk0mRJ-ci4hgELTEmGOypSDGW9U3YcaHQgHSSajCIpI17VSTmuxz9hdGFQO2C6h2lJ1i4JeGFSzvzbi0ftqppk6oWCAKj9ee9Y9Fx5CYLNvnafxkSlujxqUnQRKLENB18STWhYodl-E86iK5NK3J3JH4XJgqEona8sy9QD5ptF_8fMls0l7t18NU0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/M59MQogWBMV-7yvMj6nG1bDX7MbGdfavM7kv8521UveLejaq_OAtFgnVToetHlDvr7YyM_HG420XGdT5qfKkrfP2-PvclKZp0I_vZS9iT1XTTBX7UBQWr668Rq9NLTz_mn5DLolstdNR3vxBlXh-7coWFrydpK1U7Zj-ne5SVjnWxzeXQ-wKkWZTNQWBomIY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/C93uvph9HIwHtkI6F0njEclTsCoMWuQEuFPX9o_t-a-0BqsNmC49L190Z8GA-K7rHSoII6k9eLw0VIzfK4-bldrwcyvFreceSl5c1B5EYONTEOmXzj5ZWZHvEaNQsixbpX0MHpFc1ScYZnknzs-A72-UANKMadPD60DjTOc9dInjokHc39Duxd1BIS4HugFc?purpose=fullsize)

The **NVIDIA Tesla K80 24GB** is an old **data center / HPC GPU accelerator** released in 2014. It was designed for scientific computing, CUDA workloads, simulations, and servers — **not gaming**. ([NVIDIA][1])

## Hardware overview

| Item               | Specification                           |               |
| ------------------ | --------------------------------------- | ------------- |
| Architecture       | Kepler GK210                            |               |
| GPU chips          | **2 × GK210 GPUs**                      |               |
| CUDA cores         | 4,992 total (2,496 × 2)                 |               |
| VRAM               | **24GB GDDR5 total**                    |               |
| Memory split       | **12GB per GPU**                        |               |
| Memory bandwidth   | 480 GB/s total (240 GB/s per GPU)       |               |
| PCIe               | PCIe 3.0 x16                            |               |
| Power              | 300W                                    |               |
| Cooling            | Passive heatsink (needs server airflow) |               |
| Display output     | None                                    |               |
| Compute capability | CUDA 3.7                                | ([NVIDIA][2]) |

## Important: "24GB VRAM" is not like RTX 3090 24GB

The K80 is actually **two GPUs on one PCB**:

```
Tesla K80
 ├── GK210 GPU #1
 │    ├── 2496 CUDA cores
 │    └── 12GB GDDR5
 │
 └── GK210 GPU #2
      ├── 2496 CUDA cores
      └── 12GB GDDR5
```

It does **not** have one unified 24GB memory pool. A single CUDA process normally sees two separate GPUs. ([TechYorker][3])

For example:

* Model needs 16GB VRAM → ❌ cannot fit on one K80 GPU
* Two 8GB workloads → ✅ can run separately
* Multi-GPU training with old CUDA frameworks → ✅ possible

## AI / LLM usage today

For modern LLM work, K80 is mostly obsolete.

Problems:

### 1. No Tensor Cores

Modern AI GPUs:

* RTX 3090 → Ampere Tensor Cores
* RTX 4090 → Ada Tensor Cores
* A100/H100 → Data center Tensor Cores

K80:

* no Tensor Core
* no BF16
* no FP8
* no modern mixed precision acceleration

So PyTorch LLM inference/training is extremely slow.

### 2. Old CUDA architecture

K80 = Kepler (`sm_37`).

Many modern CUDA libraries have dropped support.

Examples:

* latest PyTorch versions often cannot use it
* FlashAttention ❌
* modern vLLM ❌
* TensorRT-LLM ❌

### 3. Very inefficient power

Performance:

* ~5.6 TFLOPS FP32
* 300W power consumption

Compare:

* RTX 3090:

  * ~35.6 TFLOPS FP32
  * 24GB GDDR6X
  * Tensor Cores

A used RTX 3090 is many times faster for AI.

## Where K80 is still interesting

Good uses:

### Learning CUDA

Good:

* CUDA programming
* memory management
* kernels
* multi-GPU concepts

Because it is cheap.

### Old scientific software

Good:

* molecular dynamics
* HPC simulation
* CUDA teaching
* legacy research

### GPU repair practice

For your GPU repair experiments, K80 is actually interesting:

* large PCB
* dual GPU
* many VRM components
* server-grade design
* cheap damaged cards exist

It is a good "practice board" before touching expensive RTX cards.

## Compared with your RTX 4070 12GB

|               | Tesla K80  | RTX 4070    |
| ------------- | ---------- | ----------- |
| Year          | 2014       | 2023        |
| VRAM          | 24GB GDDR5 | 12GB GDDR6X |
| GPU count     | 2          | 1           |
| AI speed      | Very slow  | Much faster |
| Tensor cores  | No         | Yes         |
| CUDA support  | Old        | Modern      |
| LLM inference | Poor       | Good        |
| Power         | 300W       | ~200W       |

For LLM work, your **RTX 4070 12GB is massively faster** despite having half the VRAM.

## Used market value

Today K80 cards are usually cheap because cloud providers retired them. The attractive part is "24GB VRAM", but the reality is:

> It is a 2 × 12GB Kepler card, not a cheap 24GB AI GPU.

For AI hobby/research, I would usually choose:

1. RTX 3090 24GB
2. RTX 3060 12GB (cheap)
3. RTX 4090
4. Tesla P40 24GB (if only VRAM matters)

before K80.

References:

* NVIDIA Tesla K80 datasheet ([NVIDIA][1])
* NVIDIA Tesla K80 board specification ([NVIDIA][2])
* TechPowerUp Tesla K80 database ([TechPowerUp][4])

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/TeslaK80-datasheet.pdf?utm_source=chatgpt.com "<visual_element id=\"e1\">"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/Tesla-K80-BoardSpec-07317-001-v05.pdf?cjevent=5c16c62be38411e9804803050a180513&utm_source=chatgpt.com "TESLA K80 GPU ACCELERATOR"
[3]: https://techyorker.com/nvidia-tesla-k80-how-the-dual-gk210-gpu-accelerator-worked/?utm_source=chatgpt.com "NVIDIA Tesla K80 Explained: Dual GK210 GPUs, Specs and CUDA Support"
[4]: https://www.techpowerup.com/gpu-specs/tesla-k80.c2616?utm_source=chatgpt.com "NVIDIA Tesla K80 Specs | TechPowerUp GPU Database"
