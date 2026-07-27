---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blackhole P150 AI Accelerator
translated: false
type: note
---

Question: **What's Blackhole@ P150 Series?**

Answer:

**Blackhole P150 Series** is an AI accelerator card from Tenstorrent. It is a competitor to NVIDIA GPUs for AI training/inference, but uses a very different architecture: **RISC-V + Tensix AI cores**, not CUDA GPUs. ([Tenstorrent][1])

![Image](https://images.openai.com/static-rsc-4/nFFF1ELWmmr4deT2uoEeQDXIOtY7SRQvfuFh5kUfJOI5reSgJuoWP1lgNDdINviWHfLvBqr5Gk6Y_7cOToNmr4rzQ3XVefRetheuCIjdR0tFuZi7_Wxu3TdmZ6Yxe9-VHvXuzgT77ojvx_rFf1_l8efTcsnap6V7aTimXlPMb3HITU8T3RNS-6VlQZcxA4H1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pKnUVcMCqocr9IrnJfub8597Z3DRqEQ-qKnlsbtNgE7orowe79kk-dkXD4xMbSJLB946zAfhPhf_fLLhrKctt-XqmPMz-xR4BB_iTRzXbTowNAzelGov6ywDZrE2nnk4E8WX_lMU5XgJFt5fuiAwIpltkhbjGXeoZDaR1ENog6Fp3aKwNkEIsDZdB4RF_Elx?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CFQ9kGiDO_JOMq6i4pRbSnGmkETufczyd-rsXBXl6_GCyokw4ZuA6tw0DUOY1NeWLNge4CNhhRwsp7_Eu1_KGUyRxvR4QcmqVTdt4YjEGI8MSdpARPLsyLs5x6TzDzbwcIjvlNfCGQEv5hOpXSFkPAsrTZVwYQRn4OwRFqbMKmr-WQtau4yM0PWCe8N242LM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/YkwD56dSz4eOAkD5OzFAJ3h7rfZrobL5JGUsGbwEFNSkkU92R92W5nqVzrltL6NNTQLwLoPt9Nmc2AuBf5SM0eK8VBw3nS6DAnkAUYH-O8as3aCMQW3FWqSVZ3-JHDUFO4sBmc1Eer1o4Qh2fKCCE94NhGefPIH9NgxhTPEDMuztBPH6TeZfKdNPGG2Cd4qy?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/z0dsUw_ZOO43tYA6W-5W0TMHzV6rKpE2bILgVoVr7Mesq9NWsYLk9c2KvCWSLMFxSkdCfHS7qjymLqin1cot2FVXXUMewQga2xcsDVXoNS6z9gidBsDancUBCD2JFVFbWZocNlQRDG_IGcnlUs8RzeH6O4dqRIvjp_B9RsL7uGye5Tjb2fTnNZyC-9CizJfo?purpose=fullsize)

## Hardware overview

**Blackhole P150**:

* PCIe Gen 5 AI accelerator card
* One Blackhole processor
* Up to ~300W power
* 4 × QSFP-DD high-speed links for multi-card scaling
* Designed for AI workloads (training/inference) ([Tenstorrent][1])

The P150 is basically a **large AI ASIC + many small RISC-V cores**:

```
Blackhole chip

        RISC-V CPUs
            |
            |
   +----------------+
   | Tensix cores   |
   | AI compute     |
   +----------------+
            |
     SRAM / Memory
            |
       PCIe / Ethernet
```

Tenstorrent's design philosophy:

* NVIDIA:

```
CUDA ecosystem
    |
GPU SMs
    |
Tensor Cores
```

* Tenstorrent:

```
RISC-V control cores
    |
Tensix AI processors
    |
dataflow execution
```

([Spinics][2])

---

## Why is it interesting for AI engineers?

The interesting part is **software openness**.

A Blackhole card can actually run Linux internally because it contains RISC-V cores. The Linux kernel community has added support for Blackhole P100/P150 PCIe cards. ([Spinics][2])

So conceptually:

```
Normal GPU:

CPU
 |
PCIe
 |
NVIDIA GPU
 |
CUDA kernel


Blackhole:

Host CPU
 |
PCIe
 |
Blackhole
 |
  +-- Linux
  +-- RISC-V cores
  +-- AI accelerator cores
```

This is closer to a **distributed AI computer** than a pure GPU.

---

## Performance comparison (rough)

Very roughly:

| Card                       | Architecture    | Main ecosystem   |
| -------------------------- | --------------- | ---------------- |
| NVIDIA H100                | GPU + CUDA      | dominant         |
| AMD MI300X                 | GPU + ROCm      | open alternative |
| Tenstorrent Blackhole P150 | RISC-V + Tensix | emerging         |

Blackhole P150 targets:

* LLM inference
* AI training experiments
* large-scale AI clusters

The P150 is not trying to beat H100 immediately on software maturity. Its bet is:

> "CUDA is a moat today, but future AI hardware should be programmable and open."

This is similar to the philosophy behind RISC-V.

---

## For your setup (RTX 4070 + LLM training)

A P150 is interesting because:

Your current stack:

```
PyTorch
 |
CUDA
 |
RTX 4070
```

would become:

```
PyTorch
 |
TT-Metal / Tenstorrent stack
 |
Blackhole
```

The ecosystem gap is the main issue.

For someone training GPT-2/nanoGPT locally, today:

* RTX 4090 / 5090 → easiest
* MI300X → serious training
* Blackhole → research into future AI architecture

---

## Why people talk about it

Tenstorrent is led by Jim Keller, famous for CPU architecture work (AMD Zen, Apple A-series involvement). The company is trying to build a post-CUDA AI computing platform. ([Tenstorrent][1])

For AI infrastructure builders, Blackhole is interesting because it combines:

* open ISA (RISC-V)
* AI accelerator
* scalable interconnect
* Linux-capable compute nodes

Basically: **"what if AI clusters were built more like computers, not just GPU farms?"**

References:

* ([Tenstorrent][1])
* ([Spinics][2])

[1]: https://tenstorrent.com/en/support?utm_source=chatgpt.com "Support | Tenstorrent"
[2]: https://www.spinics.net/lists/kernel/msg5869923.html?utm_source=chatgpt.com "[PATCH v2 0/8] RISC-V: Add support for Tenstorrent Blackhole SoC — Linux Kernel"
