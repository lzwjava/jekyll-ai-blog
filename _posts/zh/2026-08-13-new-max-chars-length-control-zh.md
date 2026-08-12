---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新最大字符长度控制
translated: true
type: note
---

已完成。是的，现在您可以通过两种方式控制输出长度：

## `scripts/mix_bilingual.py` 中的两个长度控制选项

| 选项 | 控制内容 | 示例 |
| -------- | ---------- | --------- |
| `--limit N` | 最大写入的**文档**数量（已有） | `--limit 2000` |
| `--max-chars N` | 输出总**字符长度**（新增） | `--max-chars 100000` |

## 新增 `--max-chars`

- 当累计输出（文档 + 控制 token + 换行符）的字符数超过 `N` 时停止写入。
- 可与 `--limit` 同时使用或不使用（哪个先触发即生效）。
- 已测试：`--max-chars 500` → 写入 7 个文档（566 字符）后停止。

您的命令变为：

```bash
python3.12 -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.50 --out mixed.txt --seed 0 \
    --max-chars 1000000
```

两个值得注意的注意事项：

- `--max-chars` 统计的是**字符数**，因此中文文本（多字节 UTF-8 编码）在磁盘上占用的字节数会更大。如果您需要的是字节/类 token 上限，我可以改成统计 UTF-8 字节数（`len(txt.encode("utf-8"))`），或者同时添加两个选项。
- `--max-chars` 会贪婪地读取源生成器并写入文档，因此会在超出上限后的**第一个文档边界**处停止（永远不会在文档中间截断）。这样保证每行输出都是一个完整的封装文档。

需要我再添加 `--max-bytes`（UTF-8 字节上限）吗？还是说基于字符的上限已满足您的需求？
