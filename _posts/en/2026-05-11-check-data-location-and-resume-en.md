---
audio: false
generated: true
image: false
lang: en
layout: post
title: Check Data Location and Resume
translated: false
type: note
---

The harness is hard-pinned to `~/projects/zz` as cwd and refuses to spawn any bash at all now that the path is gone. I need to know whether the `mv` actually completed or got cancelled before it ran.

Could you check from your own terminal:

```bash
ls /mnt/data/
ls ~/projects/ | grep zz
df -h /
```

Two possible states:

1. **`mv` ran and the data is on `/mnt/data/zz`** — most likely, given `/dev/sda1` is on the same controller and a 72 GB intra-disk-no, *cross-disk* move of 72 GB would take a few minutes, not instantaneous, so probably it **did not run** and was rejected the same way as my retry.
2. **`mv` was rejected** — the simpler case. The data is still on the NVMe at `/home/lzw/projects/zz` (the error message implies the harness thinks it doesn't exist, but that's about *my* tool's cwd check, not the actual filesystem).

After you confirm where the data lives, please also `cd` to a different directory (e.g. `cd ~`) in **the terminal Claude Code is running in** if you can — then I can take over again. Or just run the move yourself:

```bash
cd ~
mv ~/projects/zz /mnt/data/zz
cd /mnt/data/zz
```

72 GB across two physical disks at HDD write speed (~150 MB/s) ≈ **8 minutes**. After it finishes, update your shell to start new sessions in `/mnt/data/zz` and the FineWeb script will just work from there (its paths inside `progress.json` are relative to `--output-dir`).
