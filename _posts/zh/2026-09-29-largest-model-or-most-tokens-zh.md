---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最大模型还是最多词元？
translated: true
type: note
---

我检查了项目中所有的训练运行。以下是总结：

## 最大的模型（按参数量）

**`out-bilingual`** — 约 `232M` 参数的模型（L18/H16/C896，词表大小 65536）
- `iter_num`：4500 / 5000 → 已看到约 **2.36B tokens**（在 434M token 语料上约 6 个 epoch）
- `best_val_loss`：4.368
- 检查点文件：**2.7 GB**（磁盘上最大）

`out-gpt2-200m` 是相同的主体（约 219M），使用 GPT-2 的 50k 词表，但只运行到 2500/8000 次迭代（约 1.31B tokens）。

## 按训练 token 数最大的运行

**`out-github-code-124m`** — 124M 模型，已完全完成：
- `iter_num`：427000 / 427000 → **约 14B tokens**（已完成）
- `best_val_loss`：3.466

## 完整对比

| 运行名称 | 参数量 | 已见 tokens | 进度 | val_loss |
|---|---|---|---|---|
| **out-bilingual** | ~232M | 2.36B | 4500/5000 | 4.368 |
| **out-gpt2-200m** | ~219M | 1.31B | 2500/8000 | 3.459 |
| **out-fineweb-gpt3** | 124M | 7.86B | 15000/19073 | 3.026 |
| **out-github-code-124m** | 124M | **14B** | 已完成 | 3.466 |
| **out-sec-edgar-124m** | 124M | 1.54B | 47000/47400 | **2.278** |
| **out-fineweb** | 124M | 6.29B | 已完成 | 3.331 |
| out-wikipedia | ~85M | 0.59B | 18000/20000 | 4.054 |
| out-helloworld | 124M | smoke | — | — |
| out-shakespeare-char | tiny | smoke | — | — |

**总结：** **最大的模型**是 `out-bilingual`（约 232M 参数，2.7 GB 检查点），**训练时间最长的运行**是 `out-github-code-124m`（14B tokens，已完成）。整体最佳验证损失是 `out-sec-edgar-124m`，为 2.278。

你说的“最大”是指模型大小还是训练 token 数？