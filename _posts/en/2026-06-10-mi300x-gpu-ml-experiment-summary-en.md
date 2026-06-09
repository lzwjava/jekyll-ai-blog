---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X GPU ML Experiment Summary
translated: false
type: note
---

Here's a full report of what's been happening on this laptop/machine:

============================================================
  SYSTEM OVERVIEW
============================================================

  Host:     snapshots-gpu-mi300x1-192gb-devcloud-atl1
  OS:       Ubuntu 24.04.4 LTS (Noble Numbat)
  Kernel:   6.8.0-117-generic
  Uptime:   1 hour 12 minutes (booted today Jun 9 at 15:46)
  CPU:      Intel Xeon Platinum 8568Y+ (20 cores @ 2.0GHz, QEMU VM)
  RAM:      235 GB total, ~5.9 GB used
  Disk:     697 GB total, 128 GB used (19%)
  GPU:      AMD MI300X (192 GB VRAM, gfx942) via ROCm 7.2.0
            Currently idle: 44°C, 161W, 0% GPU / 0% VRAM used

============================================================
  ACTIVITY TIMELINE
============================================================

This is a cloud dev server (DigitalOcean GPU droplet) used for
ML/AI experimentation. Here's what has been done:

1. LLAMA.CPP BUILD + QWEN INFERENCE (May 20 - Jun 1)
   - Cloned and built llama.cpp with ROCm/HIP for the MI300X GPU
   - Downloaded Qwen3.5-122B-A10B (IQ1_M quantized, ~122B param MoE)
   - Set up a llama-server on port 8080 serving that model
   - Files: build_llamacpp.sh, run_server.sh
   - 385 MB repo on disk

2. NANOGPT TRAINING — 760M MODEL (Jun 1 - Jun 2)
   - Cloned Karpathy's nanoGPT repo
   - Trained a GPT-2 760M model (24 layers, 24 heads, 1536 embd)
     on FineWeb dataset
   - Trained up to ~29K steps, achieving MFU 108-113% on MI300X
   - Val loss at step 29K: ~3.27
   - Saved checkpoint: out-fineweb-760m/ckpt.pt (8.5 GB)
   - Ran inference quality audit at step 76K:
     - Grammatically correct, coherent paragraphs
     - Factually wrong (hallucinated conferences/dates)
     - Repetitive after ~100 tokens (only 17% trained)
   - 36 GB of training data/logs on disk

3. ZZ PROJECT (Jun 1)
   - A training pipeline with scripts, datasets, and logs
   - Contains training logs for FineWeb, OpenWeb, etc.
   - 40 GB on disk
   - Inference samples: stories, code, facts, AI history

4. NANOCHAT CLONE (Jun 9 - today)
   - Just cloned Karpathy's nanochat (successor to nanoGPT)
   - Includes mlflow.db, run scripts, tasks
   - Appears freshly cloned, not yet heavily used
   - 5.8 MB on disk

5. HERMES AGENT SETUP (Jun 9 - today)
   - Installed Hermes Agent via curl install script
   - Ran hermes model, hermes --yolo
   - Current session: exploring the system

============================================================
  LOGIN HISTORY
============================================================

- Today (Jun 9):  Logged in from 69.63.219.52, system rebooted at 15:46
- Jun 1: Long session (~8+ hrs), multiple terminals, heavy GPU work
- May 20: Short session (~1 hr), llama.cpp setup
- First boot: Mar 16, 2026

============================================================
  DISK USAGE BREAKDOWN
============================================================

  /root/zz/          40 GB  (training data + logs)
  /root/nanoGPT/     36 GB  (mostly checkpoint: 8.5 GB)
  /root/llama.cpp/  385 MB  (source + server binary)
  /root/nanochat/    5.8 MB (fresh clone)
  Pip cache:         ~various (cached packages)

============================================================
  SUMMARY
============================================================

This is a GPU research/dev machine used for:

- Running large language models locally (Qwen 122B via llama.cpp)
- Training GPT-2 scale models from scratch (nanoGPT 760M on MI300X)
- Experimenting with Karpathy's LLM training frameworks
- Now also running Hermes Agent for AI-assisted development

The GPU is currently idle and available. The biggest recent activity
was the nanoGPT 760M training run on Jun 1-2 which used the MI300X
heavily at 108-113% MFU.
