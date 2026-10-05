---
audio: false
generated: true
image: false
lang: en
layout: post
title: ComfyUI Installed and Verified on M40
translated: false
type: note
---

Done. ComfyUI is installed and verified running on the Tesla M40.

## Result

**Location:** `~/projects/ComfyUI` (6.6 GB total)

**Working stack:**

| Component | Version | Why |
| --- | --- | --- |
| Python | 3.12.15 (uv venv) | torch 2.7 wheels need ≤3.13 |
| PyTorch | **2.7.0+cu126** | last line with Maxwell `sm_50`/`sm_52` kernels **and** the `list[int]`-aware schema inference that `comfy_kitchen==0.2.37` needs |
| CUDA runtime | 12.6 (bundled) | works with your driver 580 |

**Verified:**

- `torch.cuda.is_available() == True`, device `Tesla M40 (5, 2)`
- `compiled arch list: ['sm_50', 'sm_60', 'sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90']` → Maxwell kernels present
- Real GPU matmul succeeded
- ComfyUI **0.38.0** started, bound to CUDA, and served `GET / → 200` + `/system_stats`

## How to run

```bash
cd ~/projects/ComfyUI
./run.sh                 # or: ./run.sh --port 8188
# then open http://127.0.0.1:8188
```

`run.sh` bakes in `--disable-cuda-malloc` (the M40 pre-dates `cudaMallocAsync`; ComfyUI itself warns about this).

## Two gotchas worth noting

1. **`comfy_kitchen` broke on torch 2.6** — it uses `list[int]` in a `torch.library.custom_op` signature that 2.6's `infer_schema` rejects. That's exactly why I moved to 2.7+cu126 rather than staying on 2.6.
2. **Maxwell has weak FP16.** If you get half-precision errors, run `./run.sh --fp32` (slower, but safe). Your 11.5 GB VRAM fits SDXL in fp32.

## Next step

No models yet. Drop a checkpoint in `~/projects/ComfyUI/models/checkpoints/` (e.g. SD 1.5 or SDXL `.safetensors`) and refresh the browser.

Want me to download a starter SDXL/SD1.5 checkpoint and run an actual end-to-end generation to confirm speed on the M40?
