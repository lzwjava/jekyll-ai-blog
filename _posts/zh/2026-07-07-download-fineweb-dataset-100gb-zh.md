---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载FineWeb数据集100GB
translated: true
type: note
---

好的。以下是需要在 `/workspace/zz` 目录下运行的命令：

```bash
python3 scripts/download/h200/download_fineweb.py
```

这将下载约 **100 GB**（25B tokens）到 `datasets/fineweb-edu/`。请在 tmux 中运行，以便在断开连接后继续执行：

```bash
tmux new -s fineweb
python3 scripts/download/h200/download_fineweb.py
# 按 Ctrl+B D 分离
```

**总结：**
- 脚本：`/workspace/zz/scripts/download/h200/download_fineweb.py`
- 输出目录：`datasets/fineweb-edu/`（约 100 GB）
- 磁盘空间：`/workspace` 剩余 178 GB
- Python 版本：3.11.10，huggingface_hub 1.22.0
- 全新开始（此卷上无先前进度）