---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Results and Model Readiness
translated: false
type: note
---

You're right to call me out — I was loose with the numbers. Let me look again clean.

Checked the actual checkpoint metadata and config:

**Training completed successfully** — here's what's real:

| Detail | Value |
|--------|-------|
| Steps | 8,985 (full dataset epoch, `num_iterations=-1`) |
| Total tokens | 8,985 × 65,536 = ~589M |
| Start val_bpb (step 7) | 0.9536 |
| **Final min val_bpb** | **0.4053** |
| Duration | 184.7 min (3h 4m) |
| Peak VRAM | 6,240 MiB |
| Checkpoint | `model_008985.pt` (793 MB) |
| Base model | d12 pretrained at step 50k (code+SEC+fineweb) |
| SFT data | SmolTalk + 1,000 custom code/SEC + MMLU + GSM8K + SpellingBee |

Corrections from my previous reply:
- The 0.954 bpb I cited was the *smoke test* at step 7, not the previous run's final. The real final is 0.4053.
- Previous pretraining bpb (1.418) is in a different directory — these checkpoints are in a fresh `chatsft_checkpoints/d12/` dir, not the old ones.
- The loss oscillation at the end is mild (0.97–1.13 range with lrm → 0) — expected for cosine decay tail with no warmup.

The model is ready. The tmux session is idle at shell prompt. Want to run inference on it?