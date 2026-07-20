---
audio: false
generated: true
image: false
lang: en
layout: post
title: Is FirePro S7150x2 worth ¥380?
translated: false
type: note
---

Question: **What is AMD FirePro S7150x2 16GB dual GPU professional card? Is it worth ¥380?**

Answer:

![Image](https://images.openai.com/static-rsc-4/rNzCHTFSMW1LQJwaElpYKcPlbD8KmYX8WVuCWWjlDXqDdKT1Q_JZ-MWi5F8QawtN8vERIkS-PGO0Zo54pGF8Bu4XcFMjTPskl1izmymeIm2YAaaVKUNCPddmAQnsNEIJqq-oTT353Xn43JTpH8G-O83jsDM2OmMyRJLrCIwz8-meCnY2HFwTonPXSpsGxXmk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/z-oAg2zULX3VNdWfuwebyjTLl_ou91-mWuI2irnisK0cNn0SLMr760EaDcgRyqFxx7CPwKn5oPSarchSXLA7fHywwLShveq9AC4ig2A0XSkksRcEYrUYpPi7_40pYeR9GyTPXUUlex1fCo1dopjQdoen482hzPTvTYTqAj8jdUKO8jl4fEIQV3hpuTjc207s?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/7B2hWUsqNXxqBdLTOYW9_Cbnr3HQmQSmtH4j0FB0KObz_opGUPAJ9TQ0P2BZdVbQ82wQ-4uDZsafz_bVluovVLND_4Hm8_NdXiQvvmB4VvGIUMEMtNMXOSSYhaI5GBaOu86bNHjW3wLsSUCmWPoh8CHmgfCWyAZLToRhiOdfF0ncmJZczlbbd2N6Z_92K2Fc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/wjI1cWJpUq618pfYFwl1vYv5O5Z2kLxZVg-qBSOXcrdPOx58Jz3xqHIeoukpjKWxi1DFgSuSQuj2d1plOzH3HavmItTnPoW7CfBJrCP29OqqcRqNBdN9wmYLzpN5--4w_kOLaFVPPLjDRHaiMDqdYvEhTWGlaHClkQ7UdiPNHAJdHXShZa3SAW1z7vzogiYV?purpose=fullsize)

The **AMD FirePro S7150x2** is a **server/workstation professional GPU**, not a normal gaming card. It is basically **two FirePro S7150 GPUs on one PCB**, designed for **GPU virtualization (MXGPU), VDI, CAD, rendering farms, and professional workloads**.

Key specs:

|              | FirePro S7150x2                                        |
| ------------ | ------------------------------------------------------ |
| Architecture | AMD GCN (Fiji era)                                     |
| Release      | ~2016                                                  |
| GPU cores    | 2 × 2048 stream processors                             |
| VRAM         | 16GB total (2 × 8GB GDDR5 ECC)                         |
| Memory bus   | 2 × 256-bit                                            |
| Compute      | ~5.8 TFLOPS FP32                                       |
| Power        | ~265W                                                  |
| Interface    | PCIe 3.0 x16                                           |
| Cooling      | Passive server heatsink (usually needs strong airflow) |

The important detail:

**"16GB" does NOT mean one 16GB GPU.**

Internally:

```
PCIe x16
    |
    +---- GPU A
    |       8GB VRAM
    |
    +---- GPU B
            8GB VRAM
```

Software sees two GPUs.

---

## Compared with GPUs you have been looking at

### FirePro S7150x2 vs Tesla M60

Very similar concept:

|                | S7150x2     | Tesla M60 |
| -------------- | ----------- | --------- |
| Year           | 2016        | 2015      |
| GPUs           | 2           | 2         |
| VRAM           | 16GB        | 16GB      |
| Memory         | GDDR5 ECC   | GDDR5 ECC |
| FP32           | ~5.8 TF     | ~8.1 TF   |
| CUDA           | ❌           | ✅         |
| ROCm           | ❌ basically | ❌         |
| Virtualization | Excellent   | Excellent |

Tesla M60 has CUDA ecosystem advantage, but both are old.

---

## For AI / LLM usage

Not recommended.

Reasons:

### 1. No CUDA

Most AI stack:

```
PyTorch
   |
CUDA
   |
NVIDIA GPU
```

FirePro:

```
PyTorch
   |
ROCm? (very limited)
   |
GCN Fiji
```

Modern ROCm does not support Fiji well.

---

### 2. VRAM is fragmented

You cannot run:

```
16GB model
```

like RTX 3090.

Because:

```
GPU0: 8GB
GPU1: 8GB
```

You need model parallelism.

Example:

```
Layer 0-20 -> GPU0
Layer 21-40 -> GPU1
```

but consumer frameworks are not optimized for this.

---

### 3. Very low performance today

Compare:

| GPU             |     FP32 |
| --------------- | -------: |
| FirePro S7150x2 |  ~5.8 TF |
| RTX 3060        | ~12.7 TF |
| RTX 4070        |   ~29 TF |
| RTX 3090        |   ~36 TF |

Your RTX 4070 is roughly **5x faster**.

---

## Where it is actually interesting

For ¥380, it is a fun card for:

### ✅ GPU virtualization lab

This is where it shines.

Example:

```
One physical card

GPU partition:

VM1 -> 4GB
VM2 -> 4GB
VM3 -> 4GB
VM4 -> 4GB
```

AMD calls this:

**MxGPU**

Similar idea to NVIDIA vGPU.

---

### ✅ OpenCL experiments

Can run:

* Blender OpenCL (old)
* scientific workloads
* compute experiments

---

### ✅ Homelab / collection

For a GPU researcher:

```
RTX 4070
RTX 3090
Tesla M60
FirePro S7150x2
MI50
```

It is interesting historically.

---

## The ¥380 question

My rating:

| Usage              | Value   |
| ------------------ | ------- |
| AI training        | ❌ 2/10  |
| LLM inference      | ❌ 2/10  |
| Gaming             | ❌ 1/10  |
| CAD workstation    | ⚠️ 5/10 |
| Virtualization lab | ✅ 8/10  |
| GPU collection     | ✅ 8/10  |

At **¥380 (~$50)**:

* As an AI GPU: skip.
* As a virtualization toy: quite interesting.
* As a collector card: good price.

For your AI experiments (nanoGPT, LLM fine-tuning, agents), a used **RTX 3090 24GB** is still in another universe:

```
FirePro S7150x2:
  2 × 8GB old GCN

RTX 3090:
  24GB unified VRAM
  CUDA
  Tensor cores
  FlashAttention support
  modern PyTorch
```

The S7150x2 is a "server history artifact"; the RTX 3090 is still a practical AI accelerator.
