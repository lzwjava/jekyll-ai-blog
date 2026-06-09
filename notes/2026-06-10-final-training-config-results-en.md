---
audio: false
generated: true
image: false
lang: en
layout: post
title: Final Training Config Results
translated: false
type: note
---

Here are all the test results:

```
CONFIG                    STEP     TOK/SEC   MFU     MEMORY   GRAD_ACCUM
─────────────────────────────────────────────────────────────────────────
bs=32, seq=2048, FA2+FP8  5.27s    99,500    36.4%   92 GB    8
bs=64, seq=2048, FA2+FP8  5.16s    101,500   37.1%   170 GB   4
bs=32, seq=4096, FA2+FP8  5.75s    91,200    36.1%   170 GB   4
bs=64, total=1M, FA2+FP8  10.2s    102,700   37.5%   170 GB   8
```

Best config: bs=64, seq=2048 — highest tok/sec with reasonable memory.

Here's your optimized tmux command:

```
cd /root/nanochat && source .venv/bin/activate && \
export OMP_NUM_THREADS=1 && \
export NANOCHAT_BASE_DIR="$HOME/.cache/nanochat" && \
export WANDB_MODE=disabled && \
export HIP_FORCE_DEV_KERNARG=1 && \
export HSA_OVERRIDE_GFX_VERSION=9.4.2 && \
export PYTORCH_ALLOC_CONF=expandable_segments:True && \
python -m scripts.base_train \
    --depth=24 \
    --device-batch-size=64 \
    --total-batch-size=524288 \
    --max-seq-len=2048 \
    --window-pattern SSSL \
    --num-iterations=29000 \
    --eval-every=5000 \
    --eval-tokens=1048576 \
    --sample-every=10000 \
    --save-every=5000 \
    --core-metric-every=5000 \
    --core-metric-max-per-task=200 \
    --tracker=mlflow \
    --fp8 \
    --run=mi300x-d24-760m-final \
    2>&1 | tee /root/nanochat/run_mi300x_d24_final.log
```

Changes vs original:
- device-batch-size: 32 → 64 (+2% throughput)
- eval-every: 1000 → 5000 (less pause overhead)
- sample-every: 5000 → 10000 (less pause overhead)
- gradient accumulation: 8 → 4 (fewer kernel launches)

Result: ~101,500 tok/sec, 37% MFU, ~41.5 hours total.

Resume if crash:
```
    --resume-from-step=<LAST_STEP> \
```
