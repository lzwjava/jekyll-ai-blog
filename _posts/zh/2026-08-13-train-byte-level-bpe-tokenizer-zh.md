---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练字节级BPE分词器
translated: true
type: note
---

该脚本会在混合语料上从头训练一个字节级BPE分词器。要使用`mixed_sample_2gb.txt`，只需将其作为`--input`参数传入：

```bash
python -m scripts.train_tokenizer \
    --input mixed_sample_2gb.txt \
    --out-prefix tok_mixed \
    --vocab-size 65536
```

### 功能说明
- 在混合中英文数据上联合训练一个**字节级BPE**分词器，使中文能够实现真正的字符/词合并，而非每个字符占用约3个token。
- 将控制标记（`<|endoftext|>`、`<|lang_en|>`、`<|lang_zh|>`及`<|mix_0|>`..`<|mix_100|>`）注册为特殊标记，确保它们不会被拆分。
- 保存分词器目录（`tok_mixed/`），其中包含`vocab.json`和`merges.txt`文件。

### 参数选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` | （必填） | 单个文件路径，或包含`.txt`/`.jsonl`分片的目录路径 |
| `--out-prefix` | `tok_mixed` | 输出目录名称 |
| `--vocab-size` | `65536` | 词表大小（建议≤65536以保持`prepare.py`使用uint16） |
| `--min-frequency` | `2` | 合并的最小词对频率 |
| `--special-tokens` | 默认列表 | 覆盖特殊标记设置 |

### 注意事项
- 该脚本也支持**目录**形式的分片输入，因此您可以直接指向分片目录，而非单个文件。
- 脚本文档说明：若您使用**nanochat**，请跳过此脚本，改用nanochat的`tok_train.py`处理混合分片目录（使用相同的rustbpe），只需将控制标记添加到其特殊标记列表中即可。

需要我现在用`mixed_sample_2gb.txt`运行吗？