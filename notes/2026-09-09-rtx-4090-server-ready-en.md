---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4090 Server Ready
translated: false
type: note
---

Connected successfully. Here's what's on that server:

## GPU

**NVIDIA GeForce RTX 4090** (1 card)

- **VRAM**: 24 GB (24564 MiB) — currently 0 MiB used, no running processes
- **Driver**: 595.91.07, **CUDA**: 13.2
- Idle state: 26°C, 17W / 450W cap, 0% utilization

## Machine specs

| Resource | Value |
| --- | --- |
| CPUs | 144 cores |
| RAM | 629 GB total (585 GB available) |
| Disk (root) | 30 GB overlay, essentially empty |
| OS | Containerized environment (overlay fs) |

A single RTX 4090 with plenty of CPU/RAM headroom — good for inference or small-scale fine-tuning (e.g. LoRA on 7B–13B models), though the 30 GB root disk is tight if you plan to store large models, so check for any additional mounted volumes if needed.
