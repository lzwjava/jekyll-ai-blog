---
audio: false
generated: true
image: false
lang: en
layout: post
title: Redundant Docker Files Reclaiming Space
translated: false
type: note
---

Here's the full story:

**Where it came from:** AMD Dev Cloud pre-loaded when your GPU Droplet was created (May 20, 2026).

**What's eating 59G:**

| Item | Size | What |
|------|------|------|
| `rocm:latest` image | 36 GB | ROCm 7.2.0 GPU stack in a container (same as host `/opt/rocm-7.2.0/`) |
| Build cache | 36 GB | 14 stale build layers (all 2+ months old, 100% reclaimable) |
| `ubuntu:24.04` image | 119 MB | Base Ubuntu image |
| `rocm` container | 115 KB | Exited 11 days ago, ran Jupyter Lab |

**What the `rocm` container did:**
- Ran `jupyter lab` with ROCm GPU access, notebook dir `/home/rocm-user/jupyter`
- Created May 20, exited ~May 21
- Logs show bots scanning for PHP vulnerabilities (standard internet noise hitting the exposed Jupyter port)

**Key insight:** The `rocm:latest` container image is a **duplicate** of what's already installed on the host at `/opt/rocm-7.2.0/` (22G on root disk). The container image + host install = ~58G of redundant ROCm files.

**What's safe to nuke:**
- `docker container prune` — remove exited `rocm` container (saves ~115K)
- `docker builder prune --all` — remove 36G of stale build cache (saves **36 GB**)
- `docker rmi rocm:latest` — remove container image (saves **36 GB**), since ROCm is already on the host

Total reclaimable: **~72 GB** from root disk. Want me to do it?