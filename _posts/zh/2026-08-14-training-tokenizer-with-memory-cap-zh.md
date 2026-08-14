---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练带内存上限的分词器
translated: true
type: note
---

以下是在2 GB文件上运行该命令并设置内存上限的方法：

```bash
cd /mnt/data/bilingual-gpt

python3 scripts/train_tokenizer.py \
  --input mixed_sample_2gb.txt \
  --out-prefix tok_mixed    \
  --vocab-size 65536         \
  --max-bytes 200000000
```

**注意事项：**
- `--max-bytes 200000000` = 200 MB采样上限 → 峰值内存约9 GB，安全运行。这是我刚刚验证成功的结果。
- `--out-prefix tok_mixed` 会生成 `tok_mixed/vocab.json` 和 `tok_mixed/merges.txt`。若不想覆盖已有的 `tok_mixed/` 目录，请使用其他前缀（例如 `tok_sample`）。
- 如需进行更小/更快的测试，可降低该值（例如 `--max-bytes 50000000` 对应50 MB）。
- **切勿在2 GB文件上不使用 `--max-bytes` 参数运行**——这会导致机器卡死（需要约35+ GB内存）。

可选：运行时监控内存使用情况：

```bash
watch -n2 "ps -o pid,rss,cmd -p \$(pgrep -f train_tokenizer.py | head -1)"
```