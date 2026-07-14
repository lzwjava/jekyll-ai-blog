---
audio: false
generated: true
image: false
lang: en
layout: post
title: B550M NVMe Storage Advice
translated: false
type: note
---

Question: What storage should I add to this build (R5 5600 + B550M-GAMING WIFI6E V14 + MI50 16GB + 32GB DDR4-3200)?

Answer:

Budget B550M boards like this one typically expose **2 M.2 slots**: one PCIe 4.0 x4 wired directly to the CPU, one PCIe 3.0 x4 wired through the B550 chipset. Confirm this in the manual before buying two Gen4 drives — putting a Gen4 drive in the chipset-side slot just wastes money since it'll run at Gen3 speeds anyway.

**Primary drive: 1TB–2TB NVMe Gen4, in the CPU-direct M.2 slot.**

This is your OS + active model storage. Sizing logic for local inference work:

- Quantized 7B models (Q4_K_M GGUF): ~4-5GB each
- Quantized 13B: ~8GB
- Quantized 70B: ~40GB
- fp16/bf16 originals if you keep them for requantizing: 2x the above

If you're just running inference on models that fit the MI50's 16GB VRAM (so realistically 7B-13B class, maybe a 30B heavily quantized), **1TB is enough** for OS + 15-20 models + datasets. If you're also doing any local fine-tuning experiments, checkpoints eat space fast — go 2TB.

**Don't cheap out on drive quality here** — random 4K read performance matters more than sequential for loading model shards and mmap'd GGUF files. Stick to known controllers (Samsung, WD Black, Crucial P-series, Kingston KC/Fury) over no-name QLC drives, since QLC drives without enough SLC cache stutter badly on large sequential writes (downloading/quantizing models).

**Secondary drive (optional): cheap 2TB+ SATA SSD or HDD for the chipset M.2/SATA ports**, if you're hoarding raw datasets, safetensors originals, or training data that doesn't need NVMe speed.

**Concrete pick:** 2TB Gen4 NVMe (e.g. Crucial P3 Plus, WD Black SN770/SN850X tier) in the CPU-direct slot. Skip a second drive unless you already know you're hoarding raw datasets — add it later, it's a 5-minute upgrade on this board.

References:

- [B550 chipset M.2 slot wiring (CPU-direct vs chipset)](https://www.amd.com/en/products/chipsets/b550)
- [NVMe QLC vs TLC sustained write behavior](https://www.tomshardware.com/reviews/best-ssds,5518.html)
