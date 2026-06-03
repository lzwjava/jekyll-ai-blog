---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自定义Nanochat训练设置指南
translated: true
type: note
---

## 如何设置Nanochat并在自定义数据上训练

### 1. 理解差异

nanoGPT 使用预标记化的 `.bin` 文件（numpy memmap 格式的 uint16 令牌 ID，通过 tiktoken 的 GPT-2 BPE）。

nanochat 使用**原始文本 parquet 文件**，并通过自己的 BPE 分词器即时进行分词。你**不能**重用 nanoGPT 的 `.bin` 文件。

### 2. 准备数据

nanochat 期望 parquet 文件位于 `~/.cache/nanochat/base_data_climbmix/`（或 `NANOCHAT_BASE_DIR` 指向的任何位置）。每个 parquet 文件必须有一个包含原始文本文档的 `text` 列。**最后**一个 parquet 文件用于验证；其余用于训练。

你的源数据是位于 `/mnt/data/zz/datasets/fineweb-edu/` 的 FineWeb-Edu parquet 文件（176 个文件，374GB，已经有一个 `text` 列）。

```bash
# 备份现有的 nanochat 数据 (ClimbMix, 9 个分片, 788MB)
mv ~/.cache/nanochat/base_data_climbmix ~/.cache/nanochat/base_data_climbmix.bak

# 符号链接你的数据
ln -s /mnt/data/zz/datasets/fineweb-edu ~/.cache/nanochat/base_data_climbmix
```

### 3. 训练分词器

nanochat 使用自己的 BPE 分词器（基于 Rust，GPT-4 风格）。它必须在你用于预训练的同一数据上进行训练：

```bash
cd /mnt/data/nanochat

# 备份旧分词器
mv ~/.cache/nanochat/tokenizer ~/.cache/nanochat/tokenizer.bak

# 训练新分词器（默认：32K 词汇量，2B 字符，约 42 秒）
.venv/bin/python -m scripts.tok_train
```

这保存到 `~/.cache/nanochat/tokenizer/`（tokenizer.pkl + token_bytes.pt）。

### 4. 冒烟测试

快速完整性检查（depth=4，5 步，~15 秒）：

```bash
cd /mnt/data/nanochat
.venv/bin/python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=4 \
  --total-batch-size=2048 \
  --num-iterations=5 \
  --eval-every=-1 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=-1 \
  --window-pattern=L \
  --tracker=none
```

关键规则：`--total-batch-size` 必须能被 `device-batch-size * max-seq-len * world_size` 整除。当 device-batch-size=4，max-seq-len=512，1 个 GPU 时：最小 total-batch-size = 2048。

### 5. 实际训练

```bash
tmux new-session -d -s train 'cd /mnt/data/nanochat && \
.venv/bin/python -m scripts.base_train \
  --depth=12 \
  --max-seq-len=2048 \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=10000 \
  --eval-every=500 \
  --core-metric-every=-1 \
  --sample-every=2000 \
  --window-pattern=L \
  --tracker=none \
  --run=fineweb-edu-d12 \
  2>&1 | tee /mnt/data/nanochat/train.log'
```

连接：`tmux attach -t train`

### 关键标志参考

| 标志 | 作用 | VRAM 影响 |
|---|---|---|
| `--depth` | Transformer 层数（4=微小，12=小型，20=默认） | 高 |
| `--max-seq-len` | 上下文长度（512/1024/2048） | 高 |
| `--device-batch-size` | 每 GPU 批次大小 | 高 — OOM 时首先减小 |
| `--total-batch-size` | 每优化步的令牌数（必须能被 device_batch*seq_len*GPU 数目整除） | 无（使用梯度累积） |
| `--num-iterations` | 总训练步数 | — |
| `--eval-every` | 每 N 步验证（-1=禁用） | — |
| `--sample-every` | 每 N 步生成样本（-1=禁用） | — |
| `--window-pattern` | `L`=全注意力，`SSL`=交替滑动窗口（需要 FA3） | — |
| `--tracker` | `wandb`/`mlflow`/`none` | — |
| `--fp8` | FP8 训练（仅 H100+） | 节省 VRAM |

### OOM 故障排除

如果 VRAM 不足，按以下顺序减少：

1. `--device-batch-size 4` (或 2, 或 1)
2. `--max-seq-len 1024` (或 512)
3. `--depth 8` (更小的模型)
4. `--window-pattern L` (全注意力，已经设置)

### 我们的实际运行结果

- 模型：286M 参数（depth=12, dim=768, 12 层, 6 头）
- 吞吐量：在 RTX 4070 上约 55,700 tok/sec
- 预计时间：10K 步（655M 令牌）约 3.3 小时
- 第 32 步损失：7.25（仍在预热，快速下降）
- VRAM：使用约 2.7GB（12GB 上有充足余量）

### 目录结构

```
~/.cache/nanochat/
├── base_data_climbmix -> /mnt/data/zz/datasets/fineweb-edu   # 你的数据
├── base_data_climbmix.bak/                                     # 旧的 ClimbMix 备份
├── tokenizer/
│   ├── tokenizer.pkl
│   └── token_bytes.pt
├── tokenizer.bak/                                              # 旧的分词器备份
└── base_checkpoints/
    └── d4/                                                     # 冒烟测试检查点
        ├── model_000005.pt
        ├── meta_000005.json
        └── optim_000005_rank0.pt
```

### 恢复训练

如果中断，从检查点恢复：

```bash
.venv/bin/python -m scripts.base_train \
  --resume-from-step=5000 \
  --save-every=1000 \
  ...（与之前相同的标志）
```
