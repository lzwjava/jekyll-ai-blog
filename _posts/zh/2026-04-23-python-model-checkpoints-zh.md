---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型检查点的示例Python代码
translated: true
type: note
---

您有两个可用的检查点。以下是示例命令：

**使用您的 FineWeb 检查点（GPT-2 风格，BPE 分词器）：**
```bash
python sample.py \
    --out_dir=out-fineweb \
    --start="The future of artificial intelligence is" \
    --num_samples=3 \
    --max_new_tokens=200
```

**使用您的莎士比亚字符级检查点：**
```bash
python sample.py \
    --out_dir=out-shakespeare-char \
    --start="To be or not to be" \
    --num_samples=3 \
    --max_new_tokens=200
```

**使用预训练的 GPT-2（无需本地检查点）：**
```bash
python sample.py \
    --init_from=gpt2 \
    --start="Once upon a time" \
    --num_samples=2 \
    --max_new_tokens=100
```

**`sample.py` 的关键参数：**

| 参数                | 默认值    | 说明                                |
| ------------------- | --------- | ----------------------------------- |
| `--num_samples`     | 10        | 生成的样本数量                      |
| `--max_new_tokens`  | 500       | 每个样本的 token 数量               |
| `--temperature`     | 0.8       | 数值越高，随机性越强                |
| `--top_k`           | 200       | Top-k 采样截断值                    |
| `--start`           | `"\n"`    | 提示字符串（或 `FILE:prompt.txt`）  |
| `--device`          | `cuda`    | 若无 GPU，请使用 `cpu`              |
