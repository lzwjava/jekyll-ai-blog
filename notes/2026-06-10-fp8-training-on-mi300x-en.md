---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 Training on MI300X
translated: false
type: note
---

Training is running with FP8! Confirmed 82,370 tok/sec, 33.3% MFU on step 1.

    ============================================================
      FP8 TRAINING ACTIVE ON MI300X
    ============================================================

    WHAT WAS DONE:

    1. UPGRADED PYTORCH to 2.12.0+rocm7.2
       - Old: torch 2.9.1+rocm6.4 (FP8 broken: "needs ROCm 6.5+")
       - New: torch 2.12.0+rocm7.2 (FP8 functional)
       - Source: download.pytorch.org/whl/rocm7.2

    2. DISCOVERED AMD FP8 DTYPE DIFFERENCE
       - NVIDIA uses: float8_e4m3fn, float8_e5m2
       - AMD uses:    float8_e4m3fnuz, float8_e5m2fnuz (unsigned zero)
       - Different max ranges: NVIDIA e4m3 max=448, AMD e4m3 max=240
       - Auto-detection code added to nanochat/fp8.py

    3. PATCHED nanochat/fp8.py FOR AMD SUPPORT
       - Added platform auto-detection (_IS_AMD flag)
       - FP8_E4M3 = float8_e4m3fnuz on AMD, float8_e4m3fn on NVIDIA
       - FP8_E5M2 = float8_e5m2fnuz on AMD, float8_e5m2 on NVIDIA
       - Updated forward pass to use FP8_E4M3
       - Updated backward pass to use FP8_E5M2

    4. UPDATED base_train.py HELP TEXT
       - Now mentions AMD MI300X support

    PERFORMANCE COMPARISON:

      Metric           bf16        FP8         Change
      ──────────────── ─────────── ─────────── ──────────
      Step time        7.7s        6.4s        -17%
      Throughput       68K tok/s   82K tok/s   +20%
      MFU              27.5%       33.1%       +5.6%
      Peak VRAM        105 GB      92 GB       -13 GB
      Est. total time  62 hours    52 hours    -10 hours
      Layers converted -           145/158     92%

    WHY NOT FULL 2x SPEEDUP:
      - Attention (SDPA) still runs in bf16 (FP8 only helps Linear layers)
      - 13 small Linear layers skipped (dim < 128)
      - Value embeddings (604M params) not FP8-convertible
      - Gradient accumulation overhead unchanged

    TRAINING PROCESS:
      Session ID: proc_c2b08249fb7b
      PID:        282186
      Log:        /root/nanochat/run_mi300x_d24_fp8.log
      Monitor:    tail -f /root/nanochat/run_mi300x_d24_fp8.log

    COMMAND TO RESTART (if crash):
      cd /root/nanochat && source .venv/bin/activate
      export HIP_FORCE_DEV_KERNARG=1
      export HSA_OVERRIDE_GFX_VERSION=9.4.2
      export PYTORCH_ALLOC_CONF=expandable_segments:True
      python -m scripts.base_train \
          --depth=24 --fp8 --tracker=mlflow \
          --resume-from-step=<LAST_STEP> \
          --run=mi300x-d24-760m-fp8
