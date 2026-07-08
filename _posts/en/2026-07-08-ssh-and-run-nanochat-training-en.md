---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH and Run NanoChat Training
translated: false
type: note
---

Sure. SSH into the machine and run these step by step:

```bash
# 1. Set up nanochat venv (this will take a while — torch download)
cd /workspace/nanochat
uv sync --extra gpu

# 2. Activate venv
source .venv/bin/activate

# 3. Train BPE tokenizer on your FineWeb-Edu data (~10 min)
export NANOCHAT_DATA_DIR=/workspace/zz/datasets/fineweb-edu/
python -m scripts.tok_train

# 4. Run d24 (760M) pretraining test (~2.6 days)
python -m scripts.base_train \
  --depth=24 \
  --device-batch-size=16 \
  --total-batch-size=524288 \
  --max-seq-len=2048 \
  --window-pattern SSSL \
  --fp8 \
  --num-iterations=29000 \
  --eval-every=500 \
  --save-every=5000 \
  --run=h200-d24-760m \
  --tracker=wandb
```

For the long training run, use `tmux` so it survives disconnection:
```bash
tmux new -s train-d24
source .venv/bin/activate
export NANOCHAT_DATA_DIR=/workspace/zz/datasets/fineweb-edu/
python -m scripts.base_train \
  --depth=24 \
  --device-batch-size=16 \
  --total-batch-size=524288 \
  --max-seq-len=2048 \
  --window-pattern SSSL \
  --fp8 \
  --num-iterations=29000 \
  --eval-every=500 \
  --save-every=5000 \
  --run=h200-d24-760m \
  --tracker=wandb
```
