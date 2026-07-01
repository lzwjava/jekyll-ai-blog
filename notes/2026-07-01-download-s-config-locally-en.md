---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download S Config Locally
translated: false
type: note
---

No, nothing is downloaded yet — all the reads above are streaming over HF Hub's remote filesystem (`HfFileSystem`). The `spgispeech/` dir is only 5.2 GB, and that's just the Python virtualenv (torch 2.6+cu124 is ~5 GB by itself).

**Disk**: 845 GB available on `/mnt/data`.

We've got plenty of room. To download the actual parquet files locally so reads are instant, you'd want:

- **S config**: ~45 GB (train + val + test) — fast
- **M config**: ~134 GB (train only) — moderate
- **L config**: ~580 GB (train only) — big but fits

Want to download one? I'd suggest **S** (45 GB, fits easily, ~77k clips, good enough for fine-tuning experiments). If you want the full SPGISpeech paper benchmark setup, you'll also need **dev** (11 GB) and **test** (11 GB).

The command would be:

```bash
huggingface-cli download kensho/spgispeech --include "S/*" --local-dir /mnt/data/zz/spgispeech/data
```

Or use `hf download` (the new CLI).
