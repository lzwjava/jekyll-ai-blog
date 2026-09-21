---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adam Single-GPU Proof
translated: false
type: note
---

Done. I wrote the single-machine version to `adam/` and verified it runs on your RTX 4070.

## What I created

| File | Purpose |
|------|---------|
| `adam/train_adam_proof.py` | Single-GPU experiment comparing Adam vs SGD/RMSProp/AdaGrad |
| `adam/README.md` | Setup + run instructions |
| `adam/optimizer_comparison.png` + `results.json` | Outputs from a 2-epoch smoke test |

## Key changes from the distributed version

- Removed all DDP/NCCL code — it's now a plain single-GPU script
- Added **validation accuracy** alongside training loss (stronger proof)
- Added `--seed` for reproducible identical model init per optimizer
- Added `--epochs`, `--batch-size`, `--max-train-samples` CLI flags
- Made matplotlib headless-safe (`Agg` backend)

## Environment note (important)

Your box has **two Pythons**:
- Homebrew Python 3.14 (`python3` → `2.10.0+cu128`)
- **System Python 3.12** (`/usr/bin/python3.12` → `2.11.0+cu130`, CUDA working)

Per your instruction I used the system one. It already had `torch`/`torchvision`; I only installed `matplotlib`.

## Run it

```bash
cd /mnt/data/zz/adam
/usr/bin/python3.12 train_adam_proof.py            # full 20-epoch run
```

## Verification already visible

The 2-epoch smoke test on the RTX 4070 already shows Adam's advantage:

| Optimizer | Epoch 2 train acc |
|-----------|-------------------|
| **Adam** | **75.2%** |
| SGD+mom | 37.1% |
| RMSProp | 50.2% |
| AdaGrad | 50.2% |

Run the full 20 epochs to see the clean loss curves (and AdaGrad's late-stage slowdown) that mirror the Adam paper.