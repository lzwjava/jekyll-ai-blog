---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 别名破坏Python虚拟环境，请使用完整路径
translated: true
type: note
---

找到了。你的 `.bashrc` 中有：

```
alias python=python3.13
```

但此机器上没有 `python3.13`。这个别名会覆盖虚拟环境。有两个选项：

**选项1** — 直接使用完整路径（无别名问题）：

```
/home/lzw/sglang-venv/bin/python -m sglang.launch_server --model Qwen/Qwen2.5-3B-Instruct --port 30000 --host 0.0.0.0
```

**选项2** — 先取消别名，再激活环境：

```
unalias python && source /home/lzw/sglang-venv/bin/activate && python -m sglang.launch_server --model Qwen/Qwen2.5-3B-Instruct --port 30000 --host 0.0.0.0
```

选项1最简单。直接在 tmux 中运行即可。
