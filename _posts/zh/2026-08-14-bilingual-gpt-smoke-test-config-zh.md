---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双语GPT冒烟测试配置
translated: true
type: note
---

已完成。以下是设置的内容：

**`data/meta.pkl`**（位于 `/mnt/data/bilingual-gpt/data/`）—— `train.py` 从中读取 `vocab_size`；已设置为 `65536`，以使模型的嵌入层/LM head 与你的 tokenizer 匹配。

**`/mnt/data/nanoGPT/config/train_bilingual_smoke.py`** —— 一个烟雾测试配置：
- `dataset = '/mnt/data/bilingual-gpt/data'`（绝对路径 → `train.py` 在此目录下找到 `train.bin`/`val.bin`/`meta.pkl`；uint16 类型的 ID）
- 小型模型（6 层 / 6 头 / 384 嵌入维度），适配你 4070 约 4 GiB 的可用显存 —— 这里的参数主要被 vocab 65536 占据
- `block_size=256`，`batch_size=8`，`grad_accum=4`，`max_iters=50`，不编译，不使用 wandb —— 快速端到端检查，确保 loss 下降且 checkpoint 能保存

从 nanoGPT 目录运行：

```bash
cd /mnt/data/nanoGPT
python train.py config/train_bilingual_smoke.py
```

注意：
- 显存较紧张（约 4 GiB 可用）。如果出现 OOM，请将 `batch_size` 降至 4 或将 `block_size` 降至 128 后重新运行。
- 这仅是一次烟雾测试运行 —— 实际训练时，请增大 `n_layer`/`n_embd`/`block_size` 和 `max_iters`，并重新启用 `compile = True`（一旦通过第一次评估，请设置 `always_save_checkpoint = True`）。