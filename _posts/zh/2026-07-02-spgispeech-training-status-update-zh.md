---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SPGISpeech训练状态更新
translated: true
type: note
---

以下是SPGISpeech金融音频模型训练的完整状态：

## 最新提交

**`a503fb5`** — 仅更新了 `.gitignore`（将 `spgispeech/checkpoints/` 添加到忽略列表）。实际训练代码位于提交 `2167e5c` 中。

## 已完成内容

**脚本**（均已提交）：

- `spgispeech/train_whisper.py` — 336行，Whisper微调流程
- `spgispeech/train_cmd.sh` — 启动器，参数为 `--model small --batch-size 16 --grad-accum 2 --lr 1e-5 --epochs 3`

**架构** — 自定义的 pyarrow 支持的 `SPGISpeechDataset`（不使用 HF `datasets` 的 Audio，避免 torchcodec 依赖地狱）：

- 针对12个 parquet 文件（42 GB）构建索引 `[(shard_idx, row_group, offset)]`
- 在内存中缓存行组（每组约1000个样本），每个 epoch 循环约78个行组
- 使用 soundfile 从嵌入的字节中解码 WAV
- `dataloader_num_workers=0`（Dataset 缓存中共享状态）

**训练配置**：whisper-small（2.44亿参数），有效批量大小32，fp16，梯度检查点，每500步评估并保存，WER 指标，TensorBoard 日志记录。

## 训练实际进度

**训练已启动但在10步后被终止。** 从 TensorBoard 日志来看：

| 步数 | 损失   | 梯度范数 | 学习率 | Epoch |
|------|--------|----------|--------|-------|
| 5    | 2.1592 | 46.0     | 0.0    | 0.0005 |
| 10   | 2.3147 | 76.0     | 0.0    | 0.0010 |

- 仍处于预热阶段（学习率 = 0）
- 损失尚未收敛
- 未保存任何模型检查点（save-steps=500，因此第一步保存未能达到）
- 未写入 `train_log.json`
- 唯一的检查点产物：一个单独的 TensorBoard 事件文件

**你已有的 vs 运行所需的内容：**

```
spgispeech/
├── train_whisper.py       # 已提交
├── train_cmd.sh           # 已提交
├── explore.py             # 已提交
├── data/S/                # 12个 parquet，42 GB — 完整存在
├── .venv/                 # 存在，依赖已安装
└── checkpoints/runs/      # 1次中断的 tensorboard 运行（10步）
```

## 如何恢复训练

```bash
cd /mnt/data/zz/spgispeech && source .venv/bin/activate

# 在 tmux 中：
tmux new-session -s whisper \; send-keys 'cd /mnt/data/zz/spgispeech && source .venv/bin/activate && python3 train_whisper.py --model small --batch-size 16 --grad-accum 2 --lr 1e-5 --epochs 3 --save-steps 500 --eval-steps 500 --logging-steps 50 --eval-samples 500 --test-samples 2000' Enter
```

数据集、虚拟环境和代码都已就绪——只需实际启动并让其运行（3个 epoch 大约需要24-30小时）。需要我来启动它吗？
