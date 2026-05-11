---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据迁移与FineWeb提取更新
translated: true
type: note
---

两个步骤均已完成。

**移动：** `~/projects/nanoGPT` → `/mnt/data/nanoGPT`（26G），原 `~/projects/nanoGPT` 现在是一个指向它的符号链接。主目录释放了约 26G 空间（占用从 92% 降至 89%，剩余 98G 可用）。

**脚本：** `/mnt/data/zz/scripts/extract/extract_fineweb_gpt3.py` 现在读取 `/mnt/data/zz/datasets/fineweb-edu/data__*.parquet`（即由 `plan_and_download_fineweb_gpt3.py` 下载的分片），并写入 `/mnt/data/nanoGPT/data/fineweb/train_fineweb.txt`。每行逻辑未变。

有一点需要注意：输出路径下现有的 16G `train_fineweb.txt` 会在你运行时被覆盖。如果想保留旧文件作为备份，请先重命名（`mv train_fineweb.txt train_fineweb.old.txt`）。

需要我现在启动提取吗？这会花费一些时间——大约有 200 个 parquet 分片（约 400 GB 压缩后的 parquet），而 `df.iterrows()` 速度较慢。如果我们要进行长时间运行，建议先做一个快速优化：从 `iterrows()` 切换到直接列迭代（速度提升约 5-10 倍）。你来决定。