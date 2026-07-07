---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb-Edu 下载设置
translated: true
type: note
---

已完成。以下是设置内容：

**脚本：** `~/zz/scripts/download/h200/download_fineweb.py`
- 在 AMD MI300X 上为 GPT-3 消融实验下载 FineWeb-Edu
- 默认：约 250 亿 tokens（约 100 GB）
- 可通过 `datasets/fineweb-edu/progress.json` 断点续传
- 在 `~/zz` 目录下运行：`python3 scripts/download/h200/download_fineweb.py`

**tmux：** 已安装（3.2a）

**初步检查：** 通过 — 已连接到 HuggingFace，列出分片，下载速度约 68 MB/s。准备好正式下载后，请在 tmux 会话中运行，这样断开连接后仍会继续：

```bash
cd ~/zz
tmux new -s fineweb
python3 scripts/download/h200/download_fineweb.py
# 按 Ctrl+B D 分离会话，使用 tmux attach -t fineweb 重新连接
```

可用参数：`--tokens <N>` 自定义数量，`--refresh-plan` 重新列出分片，`--output-dir <path>` 更改目标路径。