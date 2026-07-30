---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Motherboards for Two RTX 3060
translated: false
type: note
---

Question: What MSI motherboard can fit two RTX 3060 GPUs?

Answer:

For **2 × NVIDIA RTX 3060** cards, you need:

1. **Two physical PCIe x16-length slots**
2. Enough spacing because most RTX 3060 cards are **2-slot thick**
3. A CPU/platform that provides enough PCIe lanes (for normal ML workloads, x8/x8 is fine)

MSI boards that work:

### 1. MSI MAG B760M Mortar WiFi (your current board)

MSI MAG B760M Mortar WiFi has:

* PCIe x16 main slot → GPU 1
* PCIe x16 physical slot (electrical x4) → GPU 2

It can physically hold two RTX 3060 cards, but:

```
RTX 3060 (slot 1)
████████
████████
(blank/spacing)
RTX 3060 (slot 2)
████████
```

The second GPU runs at PCIe 4.0 x4. For LLM training/fine-tuning, this is not ideal because GPU-to-GPU bandwidth is limited, but it works.

---

### 2. MSI PRO Z790-A WiFi / MAG Z790 Tomahawk WiFi (better consumer option)

Example:

MSI MAG Z790 Tomahawk WiFi

Layout:

```
CPU PCIe x16
    |
 RTX 3060 #1  PCIe 4.0/5.0 x16

Chipset PCIe x16 slot
    |
 RTX 3060 #2  PCIe x4
```

Better spacing than many mATX boards.

---

### 3. MSI Creator / Workstation boards (best for multi-GPU)

If your goal is AI training:

MSI Creator X299 / TRX40 / WRX80 platforms are much better.

Example:

```
GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
```

because workstation CPUs expose many PCIe lanes.

---

## Important for RTX 3060 + LLM work

Two RTX 3060 cards:

* VRAM does **not automatically combine**
* 2 × 12GB ≠ 24GB VRAM

Example:

```
GPU0:
12GB VRAM

GPU1:
12GB VRAM
```

A model still sees:

```
GPU0 memory = 12GB
GPU1 memory = 12GB
```

unless using distributed training:

* PyTorch DDP
* FSDP
* DeepSpeed ZeRO
* tensor parallel inference

For your use case (nanoGPT, Qwen fine-tuning, vLLM experiments), a second GPU is useful mainly for:

* larger batch size
* DDP training
* running two models
* inference serving

---

Given your current hardware (RTX 4070 12GB + interest in LLM infra), I would **not buy another RTX 3060 and a motherboard just for VRAM**. A better upgrade path:

```
Current:
RTX 4070 12GB

Better:
RTX 3090 24GB used
+
RTX 4070 12GB
```

You get a real 24GB single-GPU workspace for:

* QLoRA
* larger LLM inference
* CUDA development
* vLLM experiments

A 3090 + 4070 on your B760 board is actually a very practical AI home lab.

References:

* NVIDIA GeForce RTX 3060 specifications: [https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060/](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060/)
* PyTorch Distributed Data Parallel: [https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html](https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)
