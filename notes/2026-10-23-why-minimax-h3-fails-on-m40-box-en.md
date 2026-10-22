---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why MiniMax-H3 Fails on M40 Box
translated: false
type: note
---

The official docs settle it — MiniMax recommends running H3 with **4 GPUs** (`--num-gpus 4`), and Comfy's only quantization that fits near 24GB (`int8_convrot`) is explicitly built for **torch with cu130** (a CUDA-13/Blackwell-era stack).

## Verdict: MiniMax-H3 cannot be set up on `192.168.1.137` — 4 independent blocking walls

**1. Disk — fails immediately.** `.137` has **18 GB free**. The *smallest possible* file set (int8):

| File | Size |
|---|---|
| `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` (32B text encoder) | 27.1 GB |
| `minimax_h3_fl2va_pruned_int8_convrot.safetensors` (diffusion) | 21.0 GB |
| `minimax_h3_video_vae_int8` + audio_vae | 3.4 GB |
| **Total** | **≈ 51.5 GB** (+ComfyUI runtime) — 3× the free disk |

**2. VRAM — fails.** 24 GB card, but the int8 encoder alone is **27 GB**. The full model pipeline (32B Qwen3-VL encoder + FL2VA MoE diffusion) fundamentally needs 4×80GB-class GPUs.

**3. System RAM — fails.** 7.7 GB total. Comfy's standard CPU-offload path for the 32B encoder needs ~28 GB+ of host RAM.

**4. GPU architecture — fails (the core reason).** Tesla M40 = **Maxwell 2015, compute capability 5.2**, and H3 demands the exact opposite of everything Maxwell is:
- All weights ship **BF16/Fp8/Int8-with-Triton-ops** → M40 has **no fp16/bf16 datapath at all**
- H3's recommended runtime is **torch cu130** (Comfy docs above); CUDA ≥12 dropped Maxwell kernels entirely; this box's driver is 550 = CUDA 12.4
- **Empirical proof from the twin box `.34`** (previous session): both torch `2.14.1+cu130` and legacy `1.13.1+cu117` hang the driver in `nvidia_uvm` (D-state, unkillable, needs reboot). The M40 cannot even initialize *any* PyTorch CUDA context on this driver generation.

I deliberately did **not** download 50 GB onto a box with 18 GB free and wedge another driver — it would have died at the disk wall before loading a single weight.

## What I'd suggest instead

1. **Cleanest option** — bring a modern GPU online. Realistic H3 cards: **A100/H100 80GB, 2×RTX 4090, RTX 5090** (Comfy's own guides: H3 wants ≥48 GB VRAM at bf16, or ~40 GB with int8_fp8). None of that exists on this LAN today.

2. **If you want *anything* image-gen on the M40 24GB**: the only stack that reaches this card is 2021-era (torch 1.13+cu117, SD1.5/SD2.1 fp32, ~10-15 it/s at 512px) — and only if driver **550** avoids the UVM hang that 580 had (untested; needs a time-boxed probe and possibly a reboot if it wedges). It can never run H3.

3. **Loose end from earlier**: `.34` still has 3 D-state procs in the wedged GPU driver — it needs a **reboot** when convenient. Say the word and I'll clean up the venvs/caches I created there (`.34`: `~/dsenv`, `~/dslegacy`, uv caches ≈ 40GB; also `~/dsvenv`).

Want me to (a) run the empirical torch probe on `.137` anyway to close out the question for your records, (b) attempt the legacy SD1.5 path on `.137`, or (c) prep a purchase/build spec for a machine that *can* run MiniMax-H3?
