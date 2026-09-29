---
audio: false
generated: true
image: false
lang: zh
layout: post
title: d18 训练状态与命令
translated: true
type: note
---

完成 — 下载已终止。以下是当前状态及可在终端中运行的命令。

## 当前状态

- ✅ **Tokenizer** 已训练（32k 词汇量），位于 `/mnt/data/nanochat-cache/tokenizer/`
- 📦 **77/170 train shards + val** 已下载（约 6.9 GB），位于 `/mnt/data/nanochat-cache/base_data_climbmix/`
- ✅ **d18 (702M) 已验证** 可适配：`bs=2, seq=1024` → 9.0 GB 峰值，约 8,100 tok/s，57% MFU

## 终端命令

**1. （可选）完成下载** — 从第 77 个继续，跳过已存在的文件：

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
./.venv/bin/python -m nanochat.dataset -n 170 -w 2
```

**2. 训练 d18 (702M) — 已验证的最大配置：**

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
./.venv/bin/python -m scripts.base_train \
  --depth=18 --max-seq-len=1024 --device-batch-size=2 \
  --tracker=none --run=d18-climbmix
```

**长时间后台运行**（推荐 — 3.9B tokens ≈ 5.6 天）：

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
nohup ./.venv/bin/python -m scripts.base_train \
  --depth=18 --max-seq-len=1024 --device-batch-size=2 \
  --tracker=none --run=d18-climbmix \
  --save-every=500 \
  > /mnt/data/nanochat-cache/train-d18.log 2>&1 &
```

## 重要说明

- **`--save-every=500`** 启用周期性 checkpoint（默认仅在结束时保存 — 对于 5.6 天的运行不利）。
- 稍后使用 **`--resume-from-step=<step>`** 恢复（checkpoint 保存在 `/mnt/data/nanochat-cache/base_checkpoints/d18/`）。
- **不要**使用 `bs=4`（OOM）或在 bs=2 时使用 `--max-seq-len=2048`（可能 OOM）。
- 默认预算 = ratio 12 → **~3.9B tokens**。要缩短运行，添加 `--num-iterations=<N>`（例如 1000 ≈ 1B tokens），或使用 `--target-param-data-ratio=4` 约减半。
- `--tracker=none` 跳过 wandb/mlflow（仓库中有一个旧的 `mlflow.db`，若有需要可启用 mlflow）。

使用以下命令监控进度：

```bash
tail -f /mnt/data/nanochat-cache/train-d18.log
```
