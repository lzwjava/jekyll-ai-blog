---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 灵活数据集下载与规划脚本
translated: true
type: note
---

新增了 `scripts/download/plan_and_download_fineweb.py`。它做到了现有脚本没有的功能：

- **按词元数，不按分片数。** 你可以指定 `--target-tokens 10B`（或 `300B`、`1T`）；它会自动选取合适的分片数量。
- **覆盖整个数据集，而非仅 CC-MAIN-2013-20。** 使用 `HfApi.repo_info` 列出仓库中所有 parquet 文件，然后按需过滤，例如用 `--dump CC-MAIN-2024-10` 获取单个快照。
- **支持 FineWeb 或 FineWeb-Edu**，通过 `--dataset fineweb-edu` 可获取你提到的高质量 1.3T 词元子集。
- **`--plan` 模式**，该模式会输出分片数量、总字节数、预估词元数、涵盖的快照，然后退出——让你在消耗带宽前先了解规模。
- **可恢复下载**（HTTP `Range` 头 + `.part` 文件），提供 `--mirror hf-mirror` 用于亚洲加速，并显示进度、MB/s 和预计完成时间。

快速示例：

```bash
# 查看 FineWeb-Edu 10B 词元的下载计划，不实际下载
python scripts/download/plan_and_download_fineweb.py \
    --dataset fineweb-edu --target-tokens 10B --plan

# 通过镜像拉取 100B 词元到 datasets/
python scripts/download/plan_and_download_fineweb.py \
    --dataset fineweb-edu --target-tokens 100B \
    --output-dir datasets/fineweb-edu --mirror hf-mirror

# 仅下载单个快照，适用于 GPT-2 级实验
python scripts/download/plan_and_download_fineweb.py \
    --dataset fineweb --target-tokens 5B --dump CC-MAIN-2024-10
```

关于估算的说明：词元预估使用 4 字节/词元的经验值（基于 GPT-2 BPE 处理英语文本）。当你用实际的分词器处理完第一批数据后，可通过 `--bytes-per-token` 传递实测值以得到更精确的计划。另外，已将 `huggingface_hub` 和 `datasets` 添加至 `requirements.txt`。