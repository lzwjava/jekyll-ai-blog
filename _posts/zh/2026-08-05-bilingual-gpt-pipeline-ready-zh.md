---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双语GPT流水线就绪
translated: true
type: note
---

完成。我已将您的问答答案转化为一个可运行、经过测试的预训练与生成流水线，位于 `/mnt/data/bilingual-gpt`，并已提交至 git。

## 目录结构

| 文件 | 功能 |
| ------ | ------ |
| `scripts/mix_bilingual.py` | 中文/英文文档混合，支持 `--zh-frac` 参数及 `<\|lang_en\|>` / `<\|lang_zh\|>` 控制标记 |
| `scripts/measure_token_ratio.py` | 对语料进行分词，并报告实际的分词比例（对应您提到的“不要相信文档计数”的观点） |
| `scripts/train_tokenizer.py` | 从头训练联合字节级 BPE，将控制标记注册为特殊标记 |
| `scripts/prepare.py` | 生成 nanoGPT 格式的 `train.bin` / `val.bin`（若词表大小 >65536，自动将 uint16 转为 uint32） |
| `scripts/generate.py` | 生成时支持 `--lang`（二值）和 `--mix-frac`（连续值）两档控制 |
| `scripts/build_codeswitch.py` | 生成代码切换文档，按 `<\|mix_0/25/50/75/100\|>` 分桶，用于连续值控制 |
| `scripts/make_synthetic.py` | 生成合成英文/中文/平行数据，方便在不下载 FineWeb 的情况下进行快速测试 |
| `README.md`、`requirements.txt`、`.gitignore` | 文档及依赖 |

## 端到端验证通过

已在合成数据上完整运行流程：**50/50 文档拆分实际仅产生约 38.8% 的中文分词比例**——这正是您回答中的关键洞察，现已自动测量，便于您调整 `--zh-frac` 以达到目标比例。

## 在使其可运行过程中发现并修复的 Bug

- `mix_bilingual.py` 出现 `KeyError`（展开后的标记字符串被 `main` 函数重新按 `LANG_TOK` 索引）。
- `measure_token_ratio.py` 假设控制标记与文本在同一行，但混合器将其分成了两行——已重写为结构感知的文档解析器；同时修复了正则表达式，使其匹配真正的 `...\|>` 结尾（而非匹配到 `...\|`），并修复了捕获 `lang_en` 而非 `en` 的分组。
- `build_codeswitch.py`：`nearest_bucket()` 将输入视为 0..1 区间的小数，但 `main` 函数传入了绝对值桶——导致所有非零值都坍缩为 `<\|mix_100\|>`。现已改为直接按显式桶构建标签。

## 实际运行方式

```bash
pip install -r requirements.txt
python -m scripts.mix_bilingual --en fineweb_edu_shard.jsonl --zh fineweb2_cmn_shard.jsonl --zh-frac 0.5 --out mixed.txt
python -m scripts.measure_token_ratio --input mixed.txt --out ratios.json --tok-prefix tok_mixed   # 迭代调整 --zh-frac
python -m scripts.train_tokenizer --input mixed.txt --out-prefix tok_mixed --vocab-size 65536
python -m scripts.prepare --input mixed.txt --tok-prefix tok_mixed --out-dir data
# 然后将 data/train.bin + data/val.bin 输入 nanoGPT，或将 nanochat 的 tok_train.py 指向混合后的分片（将控制标记加入其特殊标记列表）
```

需要我接下来接入一个最小的 nanoGPT 训练循环，使其能够读取 `data/train.bin` 并引入 `generate.py` 的控制旋钮吗？
