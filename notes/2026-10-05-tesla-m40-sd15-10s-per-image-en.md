---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 SD1.5 10s Per Image
translated: false
type: note
---

End-to-end generation confirmed on the M40 — real, coherent SD1.5 output.

## Benchmark results — Tesla M40

Workflow: **512×512, 20 steps, Euler, CFG 7, SD 1.5 (fp16)** via the ComfyUI API.

| Run | Wall time |
| --- | --- |
| Run 1 (with initial model load) | 57.8 s |
| Warm run 2 | 10.2 s |
| Warm run 3 | 10.5 s |
| Warm run 4 | 10.6 s |
| **Steady-state average** | **~10.4 s/image** (~0.52 s/step) |

(The "0.5s" from the first attempt was a ComfyUI prompt-cache hit — identical prompts get reused. Varying the seed gave the real numbers above.)

**GPU state during generation:** 3,996 MiB / 11,520 MiB VRAM used, 51 °C, ~72 W — the card is barely stressed. There's tons of VRAM headroom (fits SDXL, and could batch).

## What this means

- **SD 1.5 is very usable** on this hardware — ~10 s per 512×512 image. Interactive enough.
- **SDXL** will be roughly 4–6× heavier (bigger UNet + dual text encoders), so expect **~40–90 s/image** at 1024×1024. VRAM is fine; speed is the limit.
- **FP16 worked without errors** — no `--fp32` needed for SD1.5.

## Your working setup

- Server is **currently running**: <http://127.0.0.1:8189> (background pid from `run.sh`).
- Checkpoint: `models/checkpoints/v1-5-pruned-emaonly-fp16.safetensors`
- Outputs land in `~/projects/ComfyUI/output/` (the astronaut image is `bench_00005_.png`).
- Launch anytime with `cd ~/projects/ComfyUI && ./run.sh`.

Want me to also grab an SDXL checkpoint and time a 1024×1024 run, or install ComfyUI-Manager for custom nodes?
