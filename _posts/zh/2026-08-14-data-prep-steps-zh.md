---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据准备步骤
translated: true
type: note
---

以下是当前情况以及下一步操作。

## 当前进度

- ✅ `tok_mixed/` 已包含全新的联合BPE（词表大小65536，8个控制标记）。
- ⚠️ 现有的 `data/train.bin`（90 KB）和 `data/val.bin`（10 KB）是**过时的烟雾测试产物**——它们并非使用此分词器和此数据生成。你必须重新运行 `prepare.py`。
- ❌ 你还**不能运行 `generate.py`**——它需要 `--model out/ckpt.pt`，即训练好的GPT检查点。此仓库仅包含数据预处理和生成功能；实际训练需要使用 [nanoGPT](https://github.com/karpathy/nanoGPT) 或 [nanochat](https://github.com/duyn/nanochat) 指向你生成的 `data/` 目录。

因此顺序为：**数据准备 → 训练（nanoGPT/nanochat）→ 生成**。

## 第一步 ——（可选但推荐）检查实际标记比例

`ratios.json` 已过时（仅约7.6k个标记）。在样本上重新测量，以确认 `zh_token_frac` 符合预期，避免浪费计算资源进行训练：

```bash
python3.12 -m scripts.measure_token_ratio \
    --input mixed_sample_2gb.txt --out ratios.json --tok-prefix tok_mixed
```

如果 `zh_token_frac` 过低，请在 `mix_bilingual.py` 中调高 `--zh-frac` 并重新混合。（注意：2 GB样本是 `mixed.txt` 的一部分；测量结果仅为近似值，并非精确值。）

## 第二步 —— 将数据分词为 `.bin` 格式（这是“下一步”操作）

```bash
python3.12 -m scripts.prepare \
    --input mixed_sample_2gb.txt \
    --tok-prefix tok_mixed \
    --out-dir data \
    --val-frac 0.05
```

注意事项：
- `prepare.py` 会将**整个文件及标记ID加载到内存中**。在62 GB内存环境下，2 GB样本（甚至11 GB的 `mixed.txt`）均可正常处理；请勿指向超过内存大小的文件。
- 词表大小正好为65536 → `prepare.py` 使用 **uint16**（其检查条件为 `vocab_size <= 65536`）。因此 `.bin` 文件约为2字节/标记。可忽略训练器稍显保守的警告。
- 我使用了 `--val-frac 0.05`，避免在较小的语料库上浪费10%用于验证。可根据需要调整。
- 此操作会覆盖旧的 `data/train.bin`/`val.bin`（这正是你需要的）。

如果最终希望使用**完整**语料库进行训练，请针对 `mixed.txt`（约11 GB）运行。对于在4070显卡上的首次运行，2 GB样本是一个合理的起点。

## 第三步 —— 训练模型（在此仓库外部进行）

此仓库不包含 `train.py`。克隆 nanoGPT（或 nanochat），将其 `data_dir` 指向 `/mnt/data/bilingual-gpt/data`，设置 vocab_size=65536，并使用控制标记。nanoGPT 的基本流程如下：

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
# 编辑 train.py: vocab_size=65536, 数据集路径 -> /mnt/data/bilingual-gpt/data
python train.py config/train_gpt2.py \
    --device cuda --dtype bfloat16 \
    --n_layer 12 --n_head 12 --n_embd 768 \
    --batch_size 12 --block_size 1024 --grad_clip 1.0 \
    --learning_rate 3e-4 --warmup_iters 100 --lr_decay_iters ... \
    --out_dir out
```

在12 GB的4070显卡上，请保持 `block_size`≤1024 并适当控制 `batch_size`（或使用梯度累积）。约125M参数的模型在此环境下较为可行。如需更大模型，建议考虑 nanochat 路径或使用更小的语料库。

## 第四步 —— 生成文本（仅在此之后进行）

```bash
python3.12 -m scripts.generate \
    --model out/ckpt.pt --tok-prefix tok_mixed \
    --lang zh --prompt "机器学习是什么？" --max-new-tokens 200
```

因此：请**立即运行第二步**，之后即可准备训练。需要我为你执行 `measure_token_ratio` 和 `prepare` 操作吗？