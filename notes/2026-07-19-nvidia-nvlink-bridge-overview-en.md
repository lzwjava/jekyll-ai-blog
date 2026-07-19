---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA NVLink Bridge Overview
translated: false
type: note
---

Question: What is NVIDIA NVLink Bridge (2-slot / 3-slot / 2-way / 4-way) used for, especially for RTX 3090, A6000, A100, H100?

Answer:

![Image](https://images.openai.com/static-rsc-4/IkHwikN9QA4muNyeTGZrzJ2dtez6C-OduZHsv_Yr56HiozSZbiiu297DlmCPLjuu7pzpbR0gFc8bx9JTNFh9O0VjaAD5_3vyqrEY3Y_TEYCO8HQgLTONyqayb8Y2zTrZG1X0eCvlinHucc6R9rQV9nnVU4hKxrkSQd2tJosxevBnWwPem2RHLktVpH6GEiup?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rITK3DB6-D0rJdi8YvDstzZh2btIAjyBOSk86SipOhzR_RjDsJx_AuQJIyNlG6VmL2dipNH-KI6m44C8qzd8uOPXY4yoGUM05eABkgDwZIi-CzZw5EZDZwqAO-1B985hjTSjbgL0jatX5TkA5beg6bB_ApQOKW8rNo-Bzxi-Xj2j7AaFRWWVZEo_09o_Rfcb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/omuFtOu67coKGFWnEXiFQMfOIpOc8fRkKvMFGKz40ZP24sxroAjkcC9xsKB0m7hvSk4z0n5kcA05Ux_jIFYqGWs_D_Y3x0J-tC7teTCMq3aZrC2Y_f4JjvQo44dT7X6uB0uXQXFHBRp21Uz3MEi_Y26IbwlzW1GD4jRTsMVFcGJvrPYdpTOrqVZ3A47oDu11?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5rJoh8iKcemXwIGYkQGmwU04-loq0RHULyB6837s6tNdaLtUl8QwqphwitcoiGK6znlzXs0TyZrg7vy4WF2sdjXvHOuGPJayOId7RU-iVp8fm6SVjtGsRN0yc-qyUKwgebW01MCybkgntd0lzzkYrl3ARFkfHGceNdcmGmbRHdo7COsO34RR46W7wN_PMvYs?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/H2JQAIeEFmVT5xnqHG2jnJ0ovR0brkjyez9SDnIxf61cdYQrtWXWaqUTvETB1mRZ4PIEpBK3YAMPgI1X1UTGUbdMhlbbritdUjoYo7SK16snVXdwbJglHMnmARAc-K52EOFNwTx0WKp_SYaL394udr4P3hsDqUkgxMLQPMFWhxYNy3IjPDxmUay8OsB8tMYX?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4hfUeODPBHNxAZAdLAzn31wyLY0GpyKTEk-mFi1o8k4SdIAwIOgE4Mnr_n_7mYK27xVmj3s9OHlxVeL9ZMUGRd6KKhFhnsBirPjzu-jxDi4uz47k_e6bhpi5PTgb2zib8TXuY51D-u0GCaTA0j0DcTKrM9ffdNTE_oUHhSM3VcEiZPNutlvKqICXv9litv8A?purpose=fullsize)

**NVLink Bridge is a physical connector that links two NVIDIA GPUs together with a high-speed GPU-to-GPU interconnect.** It is not an adapter that combines GPUs into one giant GPU automatically. The software (CUDA, PyTorch, NCCL, etc.) must support multi-GPU communication. ([NVIDIA][1])

Think of it like:

```
Without NVLink:

GPU 0 ---- PCIe ---- CPU ---- PCIe ---- GPU 1

With NVLink:

GPU 0 ===== NVLink ===== GPU 1
```

The second path has much higher GPU-to-GPU bandwidth and lower latency.

---

## 1. What does "2-slot / 3-slot" mean?

It describes the **physical distance between the two GPUs on the motherboard**.

Example:

### 2-slot bridge

```
GPU
[====]

(space)

GPU
[====]
```

The GPUs are separated by 2 PCIe slots.

### 3-slot bridge

```
GPU
[====]

(space)

(empty)

GPU
[====]
```

The GPUs are farther apart.

The bridge is just a rigid connector. You need the correct spacing.

---

## 2. What does "2-way / 4-way" mean?

### 2-way NVLink

Most consumer/workstation cards:

```
GPU0 <==== NVLink Bridge ====> GPU1
```

Examples:

* RTX 3090
* RTX A6000
* RTX 6000 Ada

They support **pairing two GPUs**. ([NVIDIA][1])

---

### 4-way NVLink

This is mainly server/HPC territory:

```
GPU0 ===== GPU1
 ||         ||
GPU2 ===== GPU3
```

Usually requires:

* SXM modules
* NVSwitch
* HGX/DGX systems

Example:

* A100 SXM
* H100 SXM

A normal desktop motherboard with PCIe RTX cards cannot build a 4-way NVLink fabric. ([NVIDIA Developer][2])

---

## 3. RTX 3090 NVLink Bridge

RTX 3090 is special because it is the last GeForce card with NVLink.

Two RTX 3090:

```
RTX3090 24GB
      |
   NVLink
      |
RTX3090 24GB
```

Memory:

```
48GB total VRAM
```

but **not like a single 48GB GPU**.

For example:

Good:

* distributed training
* some CUDA workloads
* model parallelism

Not automatic:

```python
model.to("cuda")
```

does NOT become 48GB.

PyTorch still sees:

```
cuda:0 -> 24GB
cuda:1 -> 24GB
```

You need:

* DDP
* FSDP
* DeepSpeed
* tensor parallel frameworks

---

## 4. RTX 3090 + A6000 bridge compatibility

Interesting point:

The RTX A6000 NVLink bridges are often used for RTX 3090 because Ampere NVLink uses the same generation. Community testing confirmed A6000 2-slot/3-slot bridges can work with RTX 3090. ([Reddit][3])

Example:

```
RTX3090
   |
A6000 3-slot NVLink Bridge
   |
RTX3090
```

This is common in AI workstation builds.

---

## 5. A100 / H100 are different

### A100 PCIe

Similar idea:

```
A100 PCIe
    |
 NVLink
    |
A100 PCIe
```

Two-card setups exist.

### A100 SXM / H100 SXM

These are datacenter accelerators:

```
        NVSwitch
       /   |   \
H100  H100 H100 H100
```

They have much stronger interconnect.

H100 uses 4th generation NVLink:

* H100: 900 GB/s total NVLink bandwidth
* A100: 600 GB/s total NVLink bandwidth ([NVIDIA Developer][2])

---

## 6. For your AI workstation use case

Given your interest in local LLM training/inference:

### Dual RTX 3090

Good:

```
2 x RTX3090
=
48GB VRAM
+
NVLink
```

Useful for:

* 30B~70B quantized models
* LoRA training
* distributed inference

But:

NVLink does **not** magically make:

```
single GPU 48GB
```

Many modern LLM frameworks use PCIe/NCCL efficiently anyway.

---

### Buying priority

For AI:

```
VRAM
  >
GPU compute
  >
memory bandwidth
  >
NVLink
```

Usually:

2 x RTX3090 without NVLink

can still beat

1 x RTX3090 with NVLink

because you get:

* 48GB physical VRAM
* more CUDA cores
* more throughput

NVLink is a bonus.

---

## Simple summary

| Product   | NVLink? | Typical          |
| --------- | ------- | ---------------- |
| RTX 3060  | ❌       | no               |
| RTX 4070  | ❌       | no               |
| RTX 3090  | ✅       | 2 GPU bridge     |
| RTX A6000 | ✅       | 2 GPU bridge     |
| A100 PCIe | ✅       | 2 GPU            |
| A100 SXM  | ✅✅      | NVSwitch systems |
| H100 SXM  | ✅✅      | NVSwitch systems |

For a home AI lab, the interesting one is:

```
2 × RTX3090 24GB
+
A6000 2-slot/3-slot NVLink bridge
```

but only after you have enough PCIe lanes, PSU capacity, and cooling. ([Reddit][4])

References:

* ([NVIDIA][1])
* ([NVIDIA Developer][2])
* ([NVIDIA][5])
* ([Reddit][4])

[1]: https://www.nvidia.com/en-us/products/workstations/nvlink-bridges/?utm_source=chatgpt.com "NVLink High-Speed GPU Interconnect | NVIDIA Quadro"
[2]: https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/?utm_source=chatgpt.com "NVIDIA Hopper Architecture In-Depth | NVIDIA Technical Blog"
[3]: https://www.reddit.com/r/nvidia/comments/kqvbus?utm_source=chatgpt.com "Is there an (un)offiicial GEFORCE RTX NVLINK BRIDGE 2-slot version?"
[4]: https://www.reddit.com/r/nvidia/comments/kdro5w?utm_source=chatgpt.com "3090 2 and 3 Slot Bridges Are Here / Coming Soon!"
[5]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/quadro-product-literature/proviz-print-nvidia-rtx-a6000-datasheet-us-nvidia-1454980-r9-web%20%281%29.pdf?utm_source=chatgpt.com "NVIDIA RTX A6000 datasheet"
