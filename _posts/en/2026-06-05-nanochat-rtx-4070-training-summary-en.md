---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat RTX 4070 Training Summary
translated: false
type: note
---

Here's the comprehensive summary:

```
============================================================
 NANOCHAT TRAINING RUN SUMMARY (train.log)
============================================================

MODEL ARCHITECTURE
  Layers:         12
  Heads:          6 (6 KV heads, no GQA)
  Embed dim:      768
  Seq length:     2048
  Vocab size:     32,768
  Window pattern: L (full context attention - no sliding window)
  Total params:   286,261,730 (~286M)

NOTE: The run_rtx4070.sh script specifies depth=8/batch=32768/seq=1024/5000 iters,
but the actual run used depth=12/batch=65536/seq=2048/10000 iters.
You ran a custom command, not the script.

TRAINING CONFIG
  Device batch:   8 sequences x 2048 tokens = 16,384 tok/microbatch
  Grad accum:     4 steps
  Total batch:    65,536 tokens
  Iterations:     10,000
  Total tokens:   655,360,000 (~655M)
  Tokens:param:   5.95 (Chinchilla-optimal is ~20, so undertrained)

  Optimizers:     Muon (matrix weights) + AdamW (embeddings, unembeddings, scalars)
  Matrix LR:      0.02 (Muon)
  Embed LR:       0.3 (Adam)
  Unembed LR:     0.008 (Adam)
  Weight decay:   0.099 (scaled from 0.28 for depth 12)
  Warmup:         40 steps
  Warmdown:       starts at step 6500 (65% ratio)
  Final LR frac:  0.05

HARDWARE & SPEED
  GPU:            NVIDIA RTX 4070 (12 GB)
  Flash Attn:     NOT available (SDPA fallback, no FA3 on SM 89)
  FP8:            not used
  Compute dtype:  bfloat16
  Throughput:     ~55,700 tok/sec (steady state)
  Step time:      ~1,177 ms
  Peak VRAM:      9,448 MiB (78% of 12 GB)
  Total time:     196 minutes (~3.3 hours)
  MFU:            shows 0% (peak FLOPS undefined for RTX 4070 in code)

VALIDATION BPB (bits-per-byte) PROGRESSION
  Step     bpb     Notes
  -----    ------  -----
  0        3.221   random init
  500      1.280   big drop, learning fast
  1000     1.167
  1500     1.124
  2000     1.100   samples start showing basic facts
  2500     1.082
  3000     1.070
  3500     1.060
  4000     1.044   warmdown hasn't started yet
  4500     1.031
  5000     1.018
  5500     1.006   crosses below 1.0 bpb
  6000     0.995
  6500     0.985   warmdown begins here
  7000     0.976
  7500     0.967
  8000     0.959
  8500     0.951
  9000     0.945
  9500     0.939
  10000    0.935   final

  Trend: monotonically decreasing, no overfitting. Still improving
  at end of training -> model was NOT saturated, could train longer.

TRAINING LOSS (from first 100 lines)
  Step 0:    10.40  (= log2(32768), expected for random init)
  Step 10:   10.16
  Step 20:    8.71  (rapid warmup gains)
  Step 30:    7.43
  Step 40:    6.80  (warmup peaks here)
  Step 49:    6.51
  Final:      ~2.98

SAMPLE QUALITY AT END (step 10000)
  - "capital of France" -> says "south of the country" (wrong)
  - "chemical symbol of gold" -> loops "gold atom"
  - "if yesterday was Friday" -> gets confused
  - "opposite of hot" -> correct (cold), but loops
  - "planets of solar system" -> lists them correctly!
  - "5x+3=13" -> fails completely

  Verdict: 286M params with 655M tokens. Knows basic facts,
  can list things, but reasoning and factual accuracy are weak.
  Repetition/looping is common at this scale.

PREVIOUS ATTEMPT (run_rtx4070.log)
  The log shows an earlier SFT run (depth=8) that went NaN after
  ~124 steps, likely from LR/data issues. That run also evaluated
  ARC-Easy (25%), ARC-Challenge (25%), MMLU (25%), GSM8K (0%),
  HumanEval (0%) - all at chance level, as expected for a
  model trained on NaN weights.

ASSESSMENT
  + Training completed cleanly, no NaN, no crashes
  + Loss curve smooth, monotonically improving
  + Good throughput on RTX 4070 (~56k tok/sec)
  + VRAM usage comfortable (78%)

  - Tokens:param ratio 5.95 is well below Chinchilla optimal (20)
  - Model was still improving at end -> should train longer
  - Sample quality shows the model is undertrained for its size
  - FA3 not available on RTX 4070 -> SDPA fallback (slower)
  - MFU reporting broken (peak FLOPS lookup missing for RTX 4070)

  To improve: either train for ~40k+ steps (reach Chinchilla ratio),
  or scale down model (fewer params) to match the 655M token budget.
```
