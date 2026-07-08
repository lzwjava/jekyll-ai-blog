---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 处理 Codeparrot 数据集管道
translated: true
type: note
---

完成。新提交了两个脚本：

| 步骤 | 脚本 | 输出 |
| --- | --- | --- |
| 1. 下载 | `scripts/download/download_codeparrot_clean.py` | 位于 `datasets/codeparrot-clean/` 的 `.json.gz` 分片 |
| 2. 转换 | `scripts/extract/convert_codeparrot_for_nanochat.py` | 位于 `datasets/codeparrot-clean-nanochat/` 的 `text` 列 parquet 文件 |
| 3. 分词 | `scripts/extract/tokenize_github_code.py`（已有） | 位于 `datasets/codeparrot-clean-tok/` 的 `.npy` 分词分片 |

**冒烟测试**（验证集，1 个分片，6.1 万份 Python 文件）—— 通过 ✅

**运行完整流程**（全部 53 个训练分片 + 1 个验证分片，压缩后约 12.7 GB）：

**步骤 1 — 下载：**

```bash
python3.11 scripts/download/download_codeparrot_clean.py
```

**步骤 2 — 转换为 nanochat 格式：**

```bash
python3.11 scripts/extract/convert_codeparrot_for_nanochat.py
```

**步骤 3 — 分词：**

```bash
python3.11 scripts/extract/tokenize_github_code.py \
  --input-dir /mnt/data/zz/datasets/codeparrot-clean-nanochat \
  --output-dir /mnt/data/zz/datasets/codeparrot-clean-tok
```

耗时估算：步骤 1 约 15-20 分钟（观测速率 14 MB/s），步骤 2 约 20-30 分钟，步骤 3 约 10-15 分钟。全流程处理 530 万份 Python 文件总计约 1 小时。

该数据集是**纯 Python** 代码——已去重、经质量过滤（自动生成标记、字母比例、行数统计）。正是您进行以 Python 为中心的 nanoGPT 或 nanochat 实验所需的数据。