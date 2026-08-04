---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在五个数据集上运行评估
translated: true
type: note
---

你的评估仍在后台运行——5个数据集中已完成3个（gsm8k、math500、humaneval），当前正在处理mbpp，接下来是alpaca。

以下是自行运行该命令的方式：

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py \
  --dataset gsm8k,math500,humaneval,mbpp,alpaca \
  --num-samples 100 \
  --max-new-tokens 128
```

**可调整的参数：**

- `--dataset` — 逗号分隔，可选值：`gsm8k, math500, aime25, aime24, humaneval, mbpp, lbpp, livecodebench, mt-bench, alpaca, arena-hard-v2, swe-bench`
- `--num-samples` — 每个数据集的采样数（默认为3；在此GPU上约3.5秒/个采样）
- `--max-new-tokens` — 输出长度；保持≤128以在12GB显存内运行
- `--target_name_or_path` / `--draft_name_or_path` — 默认使用toy FP8配置

**后台运行并记录日志：**

```bash
cd /mnt/data/DeepSpec
nohup bash -c 'CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py --dataset gsm8k,math500,humaneval,mbpp,alpaca --num-samples 100 --max-new-tokens 128' > /tmp/eval_big.log 2>&1 &
tail -f /tmp/eval_big.log   # 查看进度
```

请在一个新的终端中运行（GPU在后台任务完成前会保持忙碌状态）。需要我在`toy_run/`目录下添加一个记录此命令的README说明吗？
