---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺失的python3.10-dev已修复
translated: true
type: note
---

已修复。问题在于**缺少 `python3.10-dev`**——triton CUDA 模块需要 `Python.h` 来编译驱动模块。安装后问题得以解决。

现在你可以从 tmux 会话重新启动训练：

```bash
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