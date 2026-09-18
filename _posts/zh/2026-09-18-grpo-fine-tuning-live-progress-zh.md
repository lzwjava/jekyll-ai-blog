---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GRPO微调实时进度
translated: true
type: note
---

非交互式附加并读取窗格 — 以下是 tmux 会话 **`2`**（窗口 0，`.venv/bin/python train_grpo.py`）的实时状态。

## 当前运行内容

使用 TRL 进行 GRPO 微调：**Qwen/Qwen2.5-1.5B**（4-bit + LoRA r=16，可训练参数 18.5M / 1.18%）在合成数学数据集上。

```
run.sh → train_grpo.py --model Qwen/Qwen2.5-1.5B --dataset synthetic \
  --output-dir ./grpo_qwen15b_math --num-epochs 2 --per-device-batch-size 2 \
  --grad-accum 4 --num-generations 4 --max-completion-length 384 \
  --lr 5e-6 --beta 0.02 --temperature 1.0
```

## 当前进度

| | |
| --- | --- |
| 步骤 | **175 / 760（23%）** |
| 已用 / 预计剩余 | 29:12 / **约剩余 48 分钟** |
| 速度 | ~4.93 秒/次 |
| Epoch | 2 中的 0.46 |
| 内部进度条 | 18/20（生成循环） |
| 检查点 | `checkpoint-125`、`checkpoint-150`（最新写入 18:53） |
| GPU | RTX 4070 — 71% 利用率，6.9 / 12.3 GB，47 °C |

## 指标趋势（来自滚动回退）

- **Reward 正在上升**：早期步骤约 0.41–0.44 → 最近步骤大多为 **0.62–1.0**，其中多个为 1.0。`reward_correctness/mean` 现在通常在 0.6–0.9。
- **KL 较低且平稳**（约 0.011–0.05）— 与参考模型无漂移/发散。
- 熵 0.50–0.74，`clip_ratio/*_mean` ≈ 0 — 策略更新温和，clipping 从未触发。
- `frac_reward_zero_std` 通常为 0.5 → 一半组内 reward 完全相同，因此这些组不贡献梯度信号。对简单的合成数学任务是正常的，但这意味着每步的有效学习信号比看起来要低。

## 健康状况

无错误，loss 或 grad_norm 中无 NaN，进程存活（CPU 83%，总运行时间 37:44，包括模型下载/加载）。日志中仅有良性警告：

- `warmup_ratio is deprecated`（transformers 5.x）
- `urllib3/charset_normalizer doesn't match a supported version`
- tokenizer PAD/BOS/EOS 对齐提示

自行附加：`tmux a -t 2`（然后使用 `Ctrl-b d` 分离）。注意还有一个 `0:mihomo` 会话单独运行。

预计完成：约 48 分钟后，即如果吞吐量保持则约 19:41 墙钟时间。
