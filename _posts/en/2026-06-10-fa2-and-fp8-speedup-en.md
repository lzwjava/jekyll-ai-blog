---
audio: false
generated: true
image: false
lang: en
layout: post
title: FA2 and FP8 Speedup
translated: false
type: note
---

OUTSTANDING RESULTS! FA2 + FP8 combined gives massive speedup:

      COMPARISON:
      ─────────────────────────────────────────────────────────────
      Config              Step Time  Throughput   MFU     Memory
      ─────────────────────────────────────────────────────────────
      bf16 + SDPA         7.7s       68K tok/s    27.5%   105 GB
      FP8 + SDPA          6.4s       82K tok/s    33.1%   92 GB
      FP8 + FA2 (SSSL)    5.27s      99.5K tok/s  36.4%   92 GB  ← NOW
      ─────────────────────────────────────────────────────────────

      vs bf16 baseline:   1.46x faster, +8.9% MFU
      vs FP8-only:        1.21x faster, +3.3% MFU

      Estimated training time: ~42.5 hours (was 62h bf16, 52h FP8-only)

    Now starting the full training run:
