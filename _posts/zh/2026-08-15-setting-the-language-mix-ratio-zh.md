---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设置语言混合比例
translated: true
type: note
---

语言比例是在**数据混合阶段（data-mixing time）**（训练之前）通过 `mix_bilingual.py` 中的 `--zh-frac` 设置的。训练后的模型没有运行时调节项——要改变平衡，你需要重新混合、重新准备、重新训练。

## 当前模型的比例来源

你的训练语料 `mixed_sample_2gb.txt` 在混合时使用了 **73% 中文文档**（127,507 英文 + 345,837 中文）。这就是模型偏向中文的原因。当时使用的参数是 `--zh-frac 0.73`。

## 设置比例——工作流程

```bash
cd /mnt/data/bilingual-gpt

# 1. 用你想要的中文 *文档* 比例（0..1）进行混合
python3.12 -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.50 --out mixed.txt --seed 0

# 2. 测量 *token* 比例（这才是模型实际看到的）
python3.12 -m scripts.measure_token_ratio --input mixed.txt --out ratios.json \
    --tok-prefix tok_mixed
#   查看 ratios.json 中的 "zh_token_frac"

# 3. 微调 --zh-frac，直到 zh_token_frac 符合你的目标，然后：
python3.12 -m scripts.train_tokenizer --input mixed.txt --out-prefix tok_mixed --vocab-size 65536
python3.12 -m scripts.prepare --input mixed.txt --tok-prefix tok_mixed --out-dir data
# 4. 从头重新训练 nanoGPT 模型（语料已改变）
```

## 注意：文档比例 ≠ token 比例

`--zh-frac` 是一个**文档采样概率**，而不是 token 比例。中文文本每个文档切分出的 token 更少，因此 50/50 的文档划分大约是 47% 的中文 token。根据你仓库自己的测量结果（smoke mix）：`tokens_per_doc_en = 4245`，`tokens_per_doc_zh = 3919`（约为英文的 92%）。所以：

| 想要的中文 token 比例 | 设置 --zh-frac ≈ |
| --- | --- |
| 50%（平衡） | 0.51–0.52 |
| 60% | 0.62 |
| 71%（当前模型） | 0.73 |

快速公式：`zh_token_frac ≈ 0.92·zh_frac / (0.92·zh_frac + 1 − zh_frac)`，可通过步骤 2 验证。

## 另一种方案：连续混合旋钮（需要不同的数据）

还有一条 code-switch 路径，可以在生成时使用*连续*比例（`--mix-frac 0.75` 配合 `<|mix_75|>` 标签）——但它需要经过 `build_codeswitch.py` 处理的**句子级对齐平行语料**（例如 WMT zh-en），并且模型必须在这些 `<|mix_N|>` 文档上训练过。你当前的模型没有在这些文档上训练过，所以它还不能做到这一点（这就是 `codeswitch.txt` 一直闲置的原因）。

**总结：** 选择你想要的中文 token 比例（步骤 2 会告诉你真实情况），据此设置 `--zh-frac`，然后重新运行 混合 → tokenizer → prepare → 训练。需要我按某个特定比例重新混合（例如真正的 50/50 token 划分）并启动重新训练吗？
