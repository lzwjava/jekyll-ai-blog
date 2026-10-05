---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 Runs ComfyUI with Caveats
translated: false
type: note
---

Short answer: **yes, it can run — but with caveats.** And one correction: this isn't a laptop. `chassis_type=3` and `MSI MS-7977` mean it's a **desktop** (Haswell/Skylake-era MSI board). Here's the real picture:

## Your hardware

| Component | Spec | Verdict for ComfyUI |
| --- | --- | --- |
| GPU | NVIDIA **Tesla M40, 11.5 GB VRAM** | ✅ Plenty of VRAM for SD1.5/SDXL |
| GPU arch | **Maxwell, compute 5.2 (sm_52)** | ⚠️ **The main blocker** |
| CPU | i5-6600, 4 cores / 4 threads | 🟡 OK to drive the queue, slow VAE/decode |
| RAM | **7.2 GB** (≈4 GB free, 3.7 GB swap) | ⚠️ Tight |
| Disk | 829 GB free | ✅ Fine |
| OS/driver | Ubuntu 26.04, driver 580, CUDA 13.0 | 🟡 Driver still supports Maxwell (580 is the last branch that does) |

## The critical issue: Maxwell (sm_52)

Recent **PyTorch CUDA wheels have dropped Maxwell/Pascal/Volta kernels**, and the CUDA 13 toolkit no longer targets sm_52. Your driver (580) is the *last* driver branch NVIDIA supports for Maxwell, so it still drives the card — but a fresh `pip install torch` today will likely install a build with **no `sm_52` kernels**, and `torch.cuda.is_available()` or the first kernel launch will fail.

**Fix:** pin an older stack:

- **PyTorch ≤ 2.6.x with CUDA 12.4** (`cu124`) — still ships Maxwell kernels
- **Python 3.11 or 3.12** (you already have 3.12 via uv; system Python 3.14 is too new for those wheels)

## Other M40 quirks

- **No FP16 acceleration** on Maxwell → run ComfyUI with fp32. Expect slower sampling than a modern card.
- **No display output** (server/compute card) — fine, you use the Intel HD 530 for the desktop, M40 for compute.
- 250 W blower card; make sure it has airflow.

## Realistic expectations

- **SD 1.5: comfortable.** SDXL: works, ~10–30 s/image at moderate steps.
- **Flux / video / big models: painful** — M40 is slow and lacks fp16, even though VRAM nominally fits.
- **7 GB RAM is the other bottleneck** — model loading + browser will swap. 16 GB would help a lot.

## Install plan (uses uv, matches your project)

```bash
git clone https://github.com/comfyanonymous/ComfyUI ~/ComfyUI && cd ~/ComfyUI
uv venv --python 3.12
uv pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
  --index-url https://download.pytorch.org/whl/cu124
uv pip install -r requirements.txt
# verify sm_52 works:
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Then launch with `--fp32` (or `--force-fp32`) if you hit half-precision errors.

Bottom line: **it runs, and 12 GB VRAM is genuinely useful — but only with a pinned legacy PyTorch, and it won't be fast.** Want me to set it up and confirm the GPU actually works under torch?
