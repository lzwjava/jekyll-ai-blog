---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb-Edu nanochat集成步骤
translated: true
type: note
---

好的，我已经了解了全貌。以下是您需要执行的操作：

您的 FineWeb-Edu parquet 文件位于 `/mnt/data/zz/datasets/fineweb-edu/`（176 个文件，374GB），其中已经包含了一个 `text` 列——这正是 nanochat 所需要的。但是，nanochat 无法使用 nanoGPT 的 `.bin` 文件，因为 nanochat 使用自己的 BPE 分词器进行分词。

**分步操作：**

**1. 将您的数据链接到 nanochat 的预期位置**

现有的 `~/.cache/nanochat/base_data_climbmix/` 目录只有 9 个分片（788MB）。请用您的数据替换它：

```bash
# 备份现有数据
mv ~/.cache/nanochat/base_data_climbmix ~/.cache/nanochat/base_data_climbmix.bak

# 创建指向您 FineWeb-Edu parquet 文件的符号链接
ln -s /mnt/data/zz/datasets/fineweb-edu ~/.cache/nanochat/base_data_climbmix
```

**2. 在您的数据上重新训练分词器**

现有的分词器是在 ClimbMix 上训练的。您需要一个在 FineWeb-Edu 上训练的分词器：

```bash
cd /mnt/data/nanochat
.venv/bin/python -m scripts.tok_train
```

此操作会读取 parquet 文件，训练一个 BPE 分词器（默认词汇量为 32K），并将其保存到 `~/.cache/nanochat/tokenizer/`。

**3. 训练模型**

单 GPU（您的 RTX 4070，12GB 显存）：

```bash
cd /mnt/data/nanochat
.venv/bin/python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=4 \
  --total-batch-size=512 \
  --num-iterations=500 \
  --eval-every=100 \
  --eval-tokens=512 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --window-pattern=L
```

根据您的显存调整的关键参数：

- `--depth` — 模型深度（4 = 微型/调试，12 = 小型，20 = 默认）
- `--device-batch-size` — 如果显存不足（OOM），请减少到 1-2
- `--max-seq-len` — 上下文长度（512 节省显存）
- `--total-batch-size` — 每个步骤的总 token 数
- `--window-pattern=L` — 使用全局注意力（SDPA 回退不支持滑动窗口）
- `--num-iterations` — 训练的步数

**重要说明：**

- nanochat 使用**自己的**分词器（BPE，32K 词汇量）——这与 tiktoken 中 GPT-2 的分词器完全不同
- nanoGPT 生成的 `.bin` 文件是使用 GPT-2 分词器预分词的，无法重复使用
- 您的原始文本 parquet 文件正是 nanochat 所需的正确输入
- 374GB 数据量很大——如果训练时间过长，您可以通过仅符号链接部分 parquet 文件来使用子集
