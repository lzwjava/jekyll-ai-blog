---
audio: false
generated: true
image: false
lang: en
layout: post
title: SPGISpeech Dataset Loaded and Explored
translated: false
type: note
---

Done. SPGISpeech dataset is loaded and explored. Here's what we found:

**Structure**

| Directory | Files | Train rows | Size |
| --- | --- | --- | --- |
| `S/` | 12 parquet | ~77k train + 39k val + 39k test | 45 GB |
| `M/` | 34 parquet | ~138k train + ... | 134 GB |
| `L/` | 146 parquet | ~633k train + ... | 580 GB |
| `dev/` | 3 parquet | validation split only | 11 GB |
| `test/` | 3 parquet | test split only | 11 GB |

**Schema** (`ParquetFile.schema_arrow`)

```
wav_filename: string       # e.g. "ed71da8f216a4f688c495b1be3050c5f/62.wav"
audio: struct<bytes: binary, path: string>  # raw WAV bytes in 'bytes', filename in 'path'
wav_filesize: int32
transcript: string         # formatted text with caps/punctuation/numbers
```

**Audio sample**: 1-channel, 16-bit, 16kHz WAV — 12.7s clip, fine with soundfile directly.

**The dataset library (datasets 5.x) issue**: it needs `torchcodec` for Audio decoding, which in turn needs CUDA torch. The pyarrow direct route (`pq.ParquetFile.read_row_group(…)` + `soundfile.read(BytesIO)`) works fine and avoids all that.

**Your setup**: `/mnt/data/zz/spgispeech/explore.py` ready to run:

```
cd /mnt/data/zz/spgispeech
source .venv/bin/activate
python3 explore.py S    # or M, L, dev, test
```
