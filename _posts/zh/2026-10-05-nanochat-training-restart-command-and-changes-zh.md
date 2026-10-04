---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoChat训练重启命令与变更
translated: true
type: note
---

以下是完整的重启命令（在 tmux 会话 `1` 中运行）：

```bash
tmux attach -t 1
```

然后在窗格中：

```bash
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache ./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 --device-batch-size=2 \
    --tracker=none --run=d18-climbmix \
    --core-metric-max-per-task=50 \
    --save-every=250
```

与原命令相比的变更：

- `--core-metric-max-per-task=50` — 更精简的 CORE 评估批次（原默认值为 500），避免在第 2000 步/最后一步出现 OOM
- `--save-every=250` — 每 250 步保存一次检查点，这样崩溃不会导致整个运行白费（仅目录：`/mnt/data/nanochat-cache/base_checkpoints/d18/`）

注意：此命令从 **第 0 步** 开始——崩溃的运行从未保存检查点。

要我直接将这些命令发送到 tmux 窗格中吗？
