---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SPGISpeech S Whisper 微调指南
translated: true
type: note
---

全部测试通过。以下为摘要：

**SPGISpeech S — 已准备好用于 Whisper 微调**

| 项目 | 数值 |
|---|---|
| 训练集 | 77,073 条样本 |
| 验证集 | 39,304 条（评估时使用 500 条） |
| 测试集 | 39,341 条（评估时使用 2,000 条） |
| 音频 | 16kHz 单声道 WAV，嵌入 parquet 文件 |
| 模型 | whisper-small（2.44 亿参数） |
| VRAM | 约 7–8 GB（batch 16，grad_accum 2，fp16） |
| 预计时间 | 3 个 epoch 约 24–36 小时 |

脚本位于 `/mnt/data/zz/spgispeech/train_whisper.py`。运行方式：

```bash
cd /mnt/data/zz/spgispeech && source .venv/bin/activate

# --- 在 tmux 中（推荐） ---
tmux new-session -s whisper \; send-keys 'cd /mnt/data/zz/spgispeech && source .venv/bin/activate && python3 train_whisper.py --model small --batch-size 16 --grad-accum 2 --lr 1e-5 --epochs 3 --save-steps 500 --eval-steps 500 --logging-steps 50 --eval-samples 500 --test-samples 2000' Enter

# --- 或使用 shell 脚本 ---
# tmux new-session -s whisper \; send-keys 'cd /mnt/data/zz/spgispeech && source .venv/bin/activate && bash train_cmd.sh' Enter
```

**可根据需要调整的参数：**
- `--model medium` — 如需更高准确率（可能需要将 `--batch-size` 改为 8）
- `--freeze-encoder` — 训练更快，仅训练解码器
- `--epochs 1` — 先快速跑一轮，验证 WER 是否改善
- `--resume` — 若训练中断，从上次检查点恢复

使用 `tensorboard --logdir /mnt/data/zz/spgispeech/checkpoints` 或 tail 日志文件进行监控。