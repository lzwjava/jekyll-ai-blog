---
audio: false
generated: true
image: false
lang: en
layout: post
title: Out of Memory Due to Desktop Apps
translated: false
type: note
---

Checked tmux `1` — it failed again, but **this time in a different place**: not the eval, but the very first optimizer step.

**What happened**

```
Step 00000 | Validation bpb: 3.171073     ← startup + step-0 eval OK
...
optimizer.step() → muon_step_fused (compiled kernel)
buf20 = empty_strided_cuda((18, 4608, 1152), ...)   # 184 MiB Muon buffer
torch.OutOfMemoryError: ... 61.81 MiB free
```

The `--core-metric-max-per-task=50` change is fine — the CORE eval never even ran yet. The job died at **step 0, optimizer.step()**, needing a 184 MiB contiguous buffer with only **62 MiB free**.

**Root cause: desktop apps are eating your VRAM now**

| Process | VRAM |
| --- | --- |
| Xorg | 1,184 MiB |
| gnome-shell | 218 MiB |
| **Chromium** | 153 MiB |
| **GitHub Desktop** | 86 MiB |
| **VS Code** | 160 MiB |
| Warp terminal | 204 MiB |
| **Total non-training** | **~2.05 GiB** |

When your original run was alive, those apps only used **~1.05 GiB**. The training process itself needs ~9 GiB (701M params: bf16 weights + grads + AdamW/Muon states ≈ 8.1 GiB, plus eval/optimizer scratch). 9 + 2.05 simply doesn't fit in 11.56 — it's over-committed by ~400-500 MiB.

**Fix: close the three closable apps, then relaunch**

```bash
# 1. free VRAM (~400 MiB)
pkill -f 'snap/chromium'        # Chromium
pkill -f github-desktop         # GitHub Desktop
pkill -f 'snap/code'            # VS Code  (skip if you need it open)

# 2. relaunch (same flags as before)
tmux attach -t 1
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache \
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 --device-batch-size=2 \
    --tracker=none --run=d18-climbmix \
    --core-metric-max-per-task=50 \
    --save-every=250
```

(`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` is belt-and-suspenders against the 648 MiB of fragmented reserved memory the error showed — the script sets `PYTORCH_ALLOC_CONF` which is the primary var in torch 2.9, but adding this costs nothing.)

I can do all of this — kill those 3 apps and relaunch inside tmux `1` — right now. Just confirm: **is it OK to close Chromium, GitHub Desktop, and VS Code?** (Xorg/gnome-shell/Warp can't be closed — they're your session.)
