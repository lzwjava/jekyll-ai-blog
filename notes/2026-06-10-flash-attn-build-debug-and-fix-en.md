---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attn Build Debug and Fix
translated: false
type: note
---

Here's the full summary:

## What I Did on lzw@192.168.1.36

### 1. Diagnosed Failed Build

- Checked for active flash-attn build — none running, previous attempt had died
- Found 104 orphaned CUDA temp files (`tmpxft_*`) in /tmp from the failed build
- Root cause: **disk 98% full** (only 19GB free on 916GB)
- pip cache alone was 15GB

### 2. Freed Disk Space

- `pip cache purge` — removed 3,530 cached files (~16GB)
- Cleaned /tmp CUDA artifacts and pip install dirs
- Result: 19GB → 35GB free

### 3. First Build Attempt (failed approach)

- Started build in tmux session `flash-build`
- Set `TORCH_CUDA_ARCH_LIST="8.9"` — flash-attn **ignored it**
- Build compiled for all 4 architectures (sm80/sm90/sm100/sm120) = 4x waste
- Also discovered **ninja was not installed** — PyTorch fell back to `make`, compiling .cu files one at a time

### 4. Second Build Attempt (correct approach)

- Killed the first build
- Installed ninja: `pip install ninja`
- Set `FLASH_ATTN_CUDA_ARCHS="8.9"` (flash-attn's own env var — respected)
- Set `MAX_JOBS=32`
- Result: single arch `compute_89,code=sm_89` only, but flash-attn's build still compiled .cu files sequentially (one nvcc at a time)
- Build completed in ~45 min

### 5. Verified Installation

- `flash_attn 2.8.3` installed in nanochat venv
- `HAS_FA2 = True`, `USE_FA2 = True` — auto-detected by nanochat

### 6. Smoke Test

- Ran `scripts.base_train` with 5 iterations
- No script modification needed — nanochat auto-detects flash-attn at import time
- First run is slow due to `torch.compile` / inductor kernel compilation
- GPU at 98%, 2.5GB VRAM
- Output buffered (piped through tee), so log only shows 3 lines so far
- Process still running (torch.compile still working)

### Key Learnings

- `TORCH_CUDA_ARCH_LIST` — ignored by flash-attn's build system
- `FLASH_ATTN_CUDA_ARCHS` — the correct env var for flash-attn
- `MAX_JOBS` — requires ninja to be installed
- flash-attn compiles .cu files sequentially regardless of MAX_JOBS
- nanochat has a clean `flash_attention.py` abstraction with FA3 → FA2 → SDPA fallback
