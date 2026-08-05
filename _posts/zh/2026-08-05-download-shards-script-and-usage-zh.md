---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载Shards脚本及用法
translated: true
type: note
---

添加了 `scripts/download_shards.py` 脚本并已提交。以下是获取真实分片并使用 `python3.12` 运行精确命令的方法：

## 下载两个分片

```bash
cd /mnt/data/bilingual-gpt

# EN: fineweb-edu, sample/10BT shard #0
python3.12 -m scripts.download_shards --source en --out fineweb_edu_shard.jsonl

# ZH: fineweb-2, cmn_Hani train shard #0
python3.12 -m scripts.download_shards --source zh --out fineweb2_cmn_shard.jsonl
```

## 然后你的命令可以直接使用

```bash
python3.12 -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.5 --out mixed.txt
```

## 脚本支持的功能

- **预置选项** — `--source en` / `--source zh` / `--source zh-csg` (opencsg/chinese-fineweb-edu-v2)。这些已在今天针对 HF 验证过：
  - `en` → `HuggingFaceFW/fineweb-edu :: sample/10BT/000_00000.parquet`
  - `zh` → `HuggingFaceFW/fineweb-2 :: data/cmn_Hani/train/000_00000.parquet`（自动选择 `train`，而非 `test`）
  - `zh-csg` → `opencsg/chinese-fineweb-edu-v2 :: data/00000.parquet`
- **手动模式** — `--repo SomeOrg/ds --file data/x.parquet`
- **通用解析** — 支持 `.parquet`（pyarrow）、`.jsonl` 和 `.jsonl.zst`；提取 `text` 列并写入标准 `{"text": ...}` jsonl 格式。
- **`--index N`** — 获取第 N 个分片（FineWeb-2 cmn_Hani 有 370 个，FineWeb-Edu 10BT 有 14 个）。
- **`--limit N`** — 限制行数，用于在完全下载前进行快速冒烟测试。

我已验证：

- 三个预置选项的发现功能都能解析到正确的分片（无需下载）；
- parquet→jsonl 转换在本地测试 parquet 上端到端工作，UTF-8 编码正确（中文保持原始字符）。

两个说明：

- 所有必要的依赖（`huggingface_hub 1.18.0`、`pyarrow 25.0.0`、`pandas 3.0.5`、`zstandard`）已为 `python3.12` 安装，无需额外安装。它们也已添加到 `requirements.txt` 中。
- FineWeb 分片是一个完整的已下载 parquet 文件；首次运行时建议使用 `--limit 5000` 确认整个流程，然后再拉取大文件。

需要我添加一个 `下载 + 混合` 便捷脚本吗（一次调用即可下载正确分片、混合并报告 token 比例）？
