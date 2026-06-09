---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 被消灭的训练指挥部
translated: true
type: note
---

已终止。以下是粘贴到 tmux 中的命令：

    cd /root/nanochat && source .venv/bin/activate && \
    export OMP_NUM_THREADS=1 && \
    export NANOCHAT_BASE_DIR="$HOME/.cache/nanochat" && \
    export WANDB_MODE=disabled && \
    export HIP_FORCE_DEV_KERNARG=1 && \
    export HSA_OVERRIDE_GFX_VERSION=9.4.2 && \
    export PYTORCH_ALLOC_CONF=expandable_segments:True && \
    python -m scripts.base_train \
        --depth=24 \
        --device-batch-size=32 \


        --total-batch-size=524288 \
        --max-seq-len=2048 \
        --window-pattern SSSL \
        --num-iterations=29000 \
        --eval-every=1000 \
        --eval-tokens=1048576 \
        --sample-every=5000 \
        --save-every=5000 \
        --core-metric-every=5000 \
        --core-metric-max-per-task=200 \
        --tracker=mlflow \
        --fp8 \
        --run=mi300x-d24-760m-fa2-fp8 \
        2>&1 | tee /root/nanochat/run_mi300x_d24_fa2_fp8.log


    如果崩溃，请使用以下命令恢复：


        --resume-from-step=<LAST_STEP> \


    （查看日志中最后完成的步骤编号）

    统计信息：约 99,500 tok/sec，36% MFU，约 5.3 秒/步，总计约 42.5 小时。
