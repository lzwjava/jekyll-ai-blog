---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分词器运行输出与后续步骤
translated: true
type: note
---

分词器运行成功。以下是该次运行的解读方法及后续步骤。

## 1. 如何解读运行输出

```
training on 1 file(s)
streaming, capped at ~200000000 bytes     ← 你设置的 --max-bytes 已生效

[00:00:04] Pre-processing sequences   …  0 / 0
[00:00:06] Tokenize words             …  3,192,137 / 3,192,137   ← 发现 3.19M 个唯一词
[00:00:04] Count pairs               …  3,192,137 / 3,192,137
[00:00:48] Compute merges            …  65,272 / 65,272         ← 学习了 65,272 个 BPE 合并
saved tokenizer -> tok_mixed/
  vocab size = 65536
```

各阶段含义：
- **Pre-processing sequences** — 扫描 200 MB 数据流，拆分为单词。
- **Tokenize words** (3,192,137) — 训练器看到的 **唯一词** 数量（每个词作为起始符号）。数值巨大是因为中文没有空格，导致许多不同的字符序列。
- **Count pairs** — 统计相邻字节对的出现频率（决定哪些合并获胜）。
- **Compute merges** (65,272) — 反复合并最频繁的字节对，直到词表达到 65,536。此过程约耗时 48 秒（最慢部分）。
- **vocab size = 65536** — 最终词表大小，你的 8 个特殊 token（`<|lang_en|>`, `<|lang_zh|>`, `<|mix_*|>`）占用 id 0–7，已在 `vocab.json` 中确认。

总耗时约 58 秒，峰值内存约 9 GB — 安全。之前出现的冻结问题已完全避免。

## 2. 接下来做什么（流水线顺序）

你现在处于 README 中“实际使用”流程的第 3 步。剩余步骤如下：

**第 4 步 — 测量实际 token 比例**（检查语言平衡）：
```bash
python3.12 -m scripts.measure_token_ratio \
  --input mixed_sample_2gb.txt --out ratios.json --tok-prefix tok_mixed
```
检查英文 / 中文的 **token** 比例是否符合预期（文档数量 ≠ token 数量）。如果 `zh_token_frac` 不准确，用调整后的 `--zh-frac` 重新运行 `mix_bilingual.py`。

**第 5 步 — token 化 → 生成二进制的训练/验证集** (`prepare.py`)：
```bash
python3.12 -m scripts.prepare \
  --input mixed_sample_2gb.txt --tok-prefix tok_mixed --out-dir data --val-frac 0.1
```
这会生成 `data/train.bin` 和 `data/val.bin`（uint16 id），供 nanoGPT/nanochat 使用。

⚠️ **注意 — `prepare.py` 存在与之前相同的内存陷阱**。查看其核心代码：
```python
with open(a.input, "r", encoding="utf-8") as f:
    text = f.read()                      # ← 将整个文件加载到内存
ids = tok.encode(text).ids               # ← 再加 token id 的完整副本
```
对于 2 GB 样本，约需 2 GB 文本 + 2–4 GB id ≈ 6–8 GB → **在你 62 GB 内存的机器上没问题**。但如果指向完整的 11.5 GB `mixed.txt`，则需要约 20–30 GB 以上，可能再次 OOM。

需要我也给 `prepare.py` 打上补丁，使其 **分块流式处理**（逐行或按固定块编码并追加到 `.bin` 文件），从而在任意大小语料库上都安全——就像分词器那样？这样就能让整个流水线安全处理完整的 11 GB `mixed.txt`。