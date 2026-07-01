---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC-EDGAR 10-K 下载摘要
translated: true
type: note
---

## SEC-EDGAR 数据集 — 会话概要

**数据集:** HuggingFace 上的 kapilrao/SEC-EDGAR  
**来源:** SEC EDGAR 申报文件（10-K、10-Q、144、20-F、3、4、5、8-K、S-1、S-8）  
**总计可用:** 2,551 个分片，总计 274.8 GB

---

**我们下载的内容:**

- 目标: ~10 GB
- 已下载: 10-K（年报）的 17 个分片，共 10 GB
- 位置: `/mnt/data/zz/datasets/sec-edgar/10-K/`
- 行数: 约 26,000 份申报文件
- 耗时: 首次运行约 55 分钟 + 重试 30 秒
- 速度: 每个分片约 3 MB/s，重试时约 222 MB/s（由 CDN 缓存加速）

**文件格式（parquet 模式）:**

- `content` — 原始 HTML
- `text` — 清洗后的纯文本
- `metadata_accession-number` — SEC 档案编号
- `metadata_filing-date` — 申报日期（YYYYMMDD）
- `metadata_period` — 财政期间结束日期
- `metadata_filer` — JSON，包含公司名称、CIK、SIC、州
- `metadata_documents` — JSON，包含申报文件文档元数据

**损坏的分片:**

- `002137a1-6454-4dca-9582-93b9d177efde-90.parquet` — HuggingFace 上游数据损坏（大小 654 MB，但 parquet 无法读取）。已删除。

---

**已创建并推送的脚本:**

| 脚本 | 用途 | 提交 |
| ------ | ------ | ------ |
| `scripts/download/download_sec_edgar.py` | 按大小上限下载分片，跳过已有缓存，支持断点续传 | `378bcdb` |
| `scripts/download/view_sec_edgar.py` | 查看/列出/搜索 parquet 文件中的样本 | `93138ec` + `70f83b5` |
| `scripts/download/fix_corrupt_shard.sh` | 重新下载损坏的分片（现已无用） | `d153ec5` |

**查看器命令:**

```
python3.11 scripts/download/view_sec_edgar.py --list
python3.11 scripts/download/view_sec_edgar.py --sample
python3.11 scripts/download/view_sec_edgar.py --sample -n 3 --text-only --chars 500
python3.11 scripts/download/view_sec_edgar.py --search "risk factors"
python3.11 scripts/download/view_sec_edgar.py --file 10-K/<shard>.parquet --head 5
```

**获取更多数据:** 增加 `--target-gb` 参数（所有申报类型总计可用 274.8 GB）。
