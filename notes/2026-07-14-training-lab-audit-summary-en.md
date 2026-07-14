---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Lab Audit Summary
translated: false
type: note
---

Here's the full audit of this repo (`zz`, 72 commits):

---

## Total Commits: 72

All on `main`, clean history. Started with FineWeb download scripts, evolved into a full training lab.

---

## Training Frameworks Used (2)

| Framework | Used For |
| ----------- | ---------- |
| **nanoGPT** (Karpathy) | FineWeb 125M & 760M, OpenWebText 125M |
| **nanochat** (Karpathy) | d12 286M pretraining + SFT |
| **transformers+peft+trl** | Notes SFT (Qwen3-4B) |
| **transformers+Whisper** | SPGISpeech (ASR) |

---

## Models You Tried (9 distinct model/run combinations)

### nanoGPT — FineWeb 125M (n_layer=12, 124M params, RTX 4070)

1. **Run #1** — 20,000 steps (`train_log_fineweb.txt`)
2. **Run #2** — ~6,000 steps (`train_log_fineweb2.txt`)
3. **Run #3** — 11,000+ steps (config max_iters=12000, `train_log_fineweb3.txt`)
4. **OpenWebText 125M** — 6,000 steps (`train_log_openweb.txt`)
5. **FineWeb 125M (MI300X)** — 750+ steps (`train_log_do_fineweb.txt`, MFU 163%)

### nanoGPT — FineWeb 760M (n_layer=24, n_embd=1536, 760M params, MI300X)

6. **760M** — 76,000 / planned 445,000 steps (17%, ~2.46B tokens seen). Two log files captured different segments of the same run. MFU 108–113%. Inference quality audit: fluent but hallucinates — "stochastic parrot" at val_loss 3.16.

### nanochat — d12 (depth=12, n_embd=768, n_head=6, ~286M params)

7. **fineweb-edu-d12** — 10,000 steps (base pretrain)
8. **rtx4070-d12-chinchilla** — resumed from above, 87,000 total steps, 28.4h on RTX 4070. Final val bpb: 0.866, smooth train loss: 2.748. Completed fully.
9. **code-sec-fineweb-d12** — 50,000 steps on mixed data (github-code + SEC-EDGAR + FineWeb-Edu)
10. **code-sec-sft (SFT)** — 8,985 steps of SFT on the d12 checkpoint (step 50K). Val bpb: 0.405. SFT taught dialogue format + code patterns, but ~140M too small for reasoning.

### nanochat — Codeparrot d12

11. **Codeparrot-clean d12** — training scripts exist (device-batch-size=4 on RTX 4070, 24.7B Python tokens). Pipeline written but no log evidence it completed.

### Other

12. **Notes SFT (Qwen3-4B)** — finetune pipeline created (`finetune/train.py`)
13. **SPGISpeech (Whisper)** — training scripts created (`spgispeech/train_whisper.py`)
14. **SEC-EDGAR GPT-2 124M** — config added but no training log found

---

## Summary Table

| # | Model | Framework | Params | Hardware | Steps | Status |
| --- | ------- | ----------- | -------- | ---------- | ------- | -------- |
| 1 | FineWeb 125M run1 | nanoGPT | 124M | RTX 4070 | 20K | completed |
| 2 | FineWeb 125M run2 | nanoGPT | 124M | RTX 4070 | 6K | completed |
| 3 | FineWeb 125M run3 | nanoGPT | 124M | RTX 4070 | 11K | completed |
| 4 | OpenWebText 125M | nanoGPT | 124M | RTX 4070 | 6K | completed |
| 5 | FineWeb 125M MI300X | nanoGPT | 124M | MI300X | 750 | smoke test |
| 6 | FineWeb 760M | nanoGPT | 760M | MI300X | 76K/445K | stopped early |
| 7 | fineweb-edu-d12 | nanochat | 286M | RTX 4070 | 10K | base pretrain done |
| 8 | rtx4070-d12-chinchilla | nanochat | 286M | RTX 4070 | 87K | **fully completed** |
| 9 | code-sec-fineweb-d12 | nanochat | 286M | H200? | 50K | completed |
| 10 | code-sec-sft | nanochat | ~140M | H200? | 8,985 | completed |
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | scripts only |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | scripts only |
| 13 | SPGISpeech (Whisper) | transformers | varies | ? | ? | scripts only |

You've done **10 actual training runs** (with log evidence) across **5 distinct model definitions** (FineWeb 125M, FineWeb 760M, nanochat d12, codeparrot d12, Qwen3-4B SFT). The crown jewel is the **d12-chinchilla run** (87K steps, fully completed) and the **code-sec-fineweb-d12 + SFT** pipeline.
