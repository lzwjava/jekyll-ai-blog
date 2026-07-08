---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH与运行NanoChat培训
translated: true
type: note
---

当然。SSH 进入机器，然后逐步运行以下命令：

```bash
# 1. 设置 nanochat venv（这会花一些时间——下载 torch）
cd /workspace/nanochat
uv sync --extra gpu

# 2. 激活 venv
source .venv/bin/activate

# 3. 在 FineWeb-Edu 数据上训练 BPE tokenizer（约10分钟）
export NANOCHAT_DATA_DIR=/workspace/zz/datasets/fineweb-edu/
python -m scripts.tok_train

# 4. 运行 d24（760M）预训练测试（约2.6天）
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

对于长时间的训练运行，请使用 `tmux` 以避免断开连接导致中断：
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