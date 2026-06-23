---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 2000 Ada GPU Status
translated: false
type: note
---

Connected. Here's the GPU info:

  GPU: NVIDIA RTX 2000 Ada Generation
  VRAM: 16 GB (16380 MiB)
  Driver: 580.159.04  |  CUDA: 13.0
  Utilization: 0%  |  Temp: 27°C  |  Power: 7W/70W
  Memory used: 2 MiB / 16380 MiB (idle)
  Persistence mode: On  |  ECC: Off

This is a workstation-class Ada Lovelace GPU with 16 GB VRAM — decent for fine-tuning small-medium models with LoRA/QLoRA, running quantized inference, or light training. The RTX 2000 Ada is based on the AD107 die (same as RTX 4060 family) but with professional drivers and ISV certification. Currently idle with no processes running.

Key specs to keep in mind:

- Compute capability: 8.9 (Ada)
- ~3,072 CUDA cores
- 128 GB/s memory bandwidth
- Good for: LoRA fine-tuning 7B-13B models (QLoRA), GGUF inference, flash-attention workloads
- Not ideal for: full fine-tuning of large models, heavy multi-GPU training

Want me to check anything else on that machine (CPU, RAM, disk, installed packages)?
