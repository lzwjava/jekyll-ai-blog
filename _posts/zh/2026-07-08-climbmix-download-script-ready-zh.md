---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ClimbMix下载脚本就绪
translated: true
type: note
---

下载脚本已准备就绪。以下是摘要：

**已创建 `/home/xiaoxin/projects/zz/climbmix/download.py`** — 用于 `nvidia/Nemotron-ClimbMix` 的并行下载器

支持三个子集：

| 选项 | 文件 | 大致大小 |
| -------- | ------- | ------------- |
| `--subset small`（默认） | `climbmix_small/` 中的 100 个 parquet 分片 | ~50 GB |
| `--subset main` | 100 个 tokenized JSONL 文件（`part_0..part_99`） | ~2 TB |
| `--subset full` | 上述两者 + 额外文件 | ~2 TB |

特性：

- 通过 `ThreadPoolExecutor` 实现并行下载（默认 8 个工作线程，可通过 `--workers N` 配置）
- 通过 `wget -c` 支持断点续传 — 中断后可安全重跑
- 进度统计（MB/s、预计剩余时间、缓存/错误计数）
- `--shard-range LO-HI` 用于下载指定索引范围（例如 `--subset small --shard-range 0-4`）
- `HF_HUB_ENABLE_HF_TRANSFER=1` 可实现每流速度提升 2-5 倍
- 自动为子文件夹路径（如 `climbmix_small/`）创建父目录

使用示例：

```bash
# 小型子集（冒烟测试，~50 GB）
python3 climbmix/download.py --subset small

# 主数据集，仅分片 10-19
python3 climbmix/download.py --subset main --shard-range 10-19 --workers 16

# 完整数据集，使用 hf_transfer
HF_HUB_ENABLE_HF_TRANSFER=1 python3 climbmix/download.py --subset full --workers 16
```

小型子集已为 parquet 格式，包含 `text` 列，可直接用于 tokenization。主数据集文件为 `.tokenized.jsonl`（LFS），需要使用 `detokenize_climbmix.py` 转换回可读文本。
