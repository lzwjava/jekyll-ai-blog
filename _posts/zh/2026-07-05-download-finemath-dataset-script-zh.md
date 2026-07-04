---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载FineMath数据集脚本
translated: true
type: note
---

已创建 `/home/xiaoxin/projects/zz/finemath/download_finemath.py` — 目录和脚本已就绪。

**脚本：** `finemath/download_finemath.py`

从 **HuggingFaceTB/finemath**（包含 540 亿 token 的教育数学数据集）下载 parquet 分片。覆盖范围：

| 配置 | 分片数 | 大小 |
|---|---|---|
| `finemath-3plus` | 128 | 60.6 GB |
| `finemath-4plus` | 64 | 17.1 GB |
| `infiwebmath-3plus` | 64 | 43.6 GB |
| `infiwebmath-4plus` | 32 | 17.9 GB |
| **总计** | **288** | **139.2 GB** |

**使用示例：**
```bash
# 查看将要下载的内容（预演模式）
python3 finemath/download_finemath.py --plan

# 仅下载 K-12 数学子集（60 GB）
python3 finemath/download_finemath.py --config finemath-3plus

# 下载全部数据（约139 GB）
python3 finemath/download_finemath.py

# 使用 HF 镜像（从亚洲地区下载更快）
python3 finemath/download_finemath.py --mirror hf-mirror

# 仅下载 10 GB 用于测试
python3 finemath/download_finemath.py --target-gb 10 --plan
```

主要特性（继承自现有 `plan_and_download_fineweb.py` 的模式）：
- **可断点续传** — 使用 `wget -c`，跳过已下载的分片
- **镜像支持** — `--mirror hf-mirror` 可从亚洲地区加速下载
- **部分下载** — `--target-gb N` 可仅获取部分数据
- **进度显示** — 每个分片的统计信息、速率和预计完成时间