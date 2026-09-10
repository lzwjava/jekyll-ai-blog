---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练检查点已保存且数据已复制
translated: true
type: note
---

完成。

**通过评估和 checkpoint 确认训练仍在进行：**

- `iter 500: train 6.3077 | val 6.2557` — checkpoint 已保存：`out-wikipedia/ckpt.pt`（344 MiB）
- 进程 670206 仍在运行（运行时间 02:55），GPU 已使用 11,662 MiB / 空闲 178 MiB
- 步时间稳定为 323 毫秒（仅在评估迭代上约 1339 毫秒）

**数据已复制到 `/mnt/data/igpt/data/wikipedia/`** — 该目录现在是自包含的：

| 文件 | 大小 | 状态 |
| --- | --- | --- |
| `train.bin` | 171,940,466 B | 已存在，md5 `abd9f26f…` 与 nanoGPT 源匹配 |
| `val.bin` | 118,116 B | 已存在，md5 `cc47f9dc…` 匹配 |
| `meta.pkl` | 73 B | 已存在（gpt2 BPE，词表 50257） |
| `train_wikipedia.txt` | 435,797,227 B | **已复制** 自 `/mnt/data/nanoGPT/data/wikipedia_local/`，md5 `9fe89b7e…` 匹配 |
| `prepare.py` | 4,797 B | **已复制**（来源/配方） |
| `readme.md` | 489 B | **已复制** |

`data/` 被 git 忽略，因此这些都不会出现在 `git status` 中（只有 `.gitignore` 和 `train.py` 在那里被修改）。

值得指出的一点：`mfu` 数值（约 1800%）是不可能的——`train.py` 计算的是 `params*6*tokens_per_iter/(dt*1e12)`，得到的是实际 TFLOP/s，而不是 MFU。实际数字大约为 18 TFLOP/s，占显卡峰值（约 1–2% MFU）；缺少的除数是 GPU 的峰值 FLOP/s。对训练无害，只是一个标签错误的指标。
