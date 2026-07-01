---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SPGISpeech数据集加载并探索
translated: true
type: note
---

已完成。已加载并探索 SPGISpeech 数据集。以下是发现：

**结构**

| 目录 | 文件数 | 训练行数 | 大小 |
| --- | --- | --- | --- |
| `S/` | 12 个 parquet | 约 77k 训练 + 39k 验证 + 39k 测试 | 45 GB |
| `M/` | 34 个 parquet | 约 138k 训练 + ... | 134 GB |
| `L/` | 146 个 parquet | 约 633k 训练 + ... | 580 GB |
| `dev/` | 3 个 parquet | 仅验证集 | 11 GB |
| `test/` | 3 个 parquet | 仅测试集 | 11 GB |

**Schema** (`ParquetFile.schema_arrow`)

```
wav_filename: string       # 例如 "ed71da8f216a4f688c495b1be3050c5f/62.wav"
audio: struct<bytes: binary, path: string>  # 原始 WAV 字节在 'bytes' 中，文件名在 'path' 中
wav_filesize: int32
transcript: string         # 格式化文本，包含大写/标点/数字
```

**音频样本**: 单声道、16-bit、16kHz WAV — 12.7 秒片段，直接使用 soundfile 正常。

**数据集库 (datasets 5.x) 问题**: 它需要 `torchcodec` 进行音频解码，而 `torchcodec` 又需要 CUDA torch。直接使用 pyarrow 路径 (`pq.ParquetFile.read_row_group(…)` + `soundfile.read(BytesIO)`) 即可正常工作，避免了所有这些问题。

**你的设置**: `/mnt/data/zz/spgispeech/explore.py` 已准备好运行：

```
cd /mnt/data/zz/spgispeech
source .venv/bin/activate
python3 explore.py S    # 或 M, L, dev, test
```
