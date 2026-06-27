---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alias Breaks Python venv, Use Full Path
translated: false
type: note
---

Found it. Your `.bashrc` has:

```
alias python=python3.13
```

But `python3.13` doesn't exist on this machine. That alias overrides the venv. Two options:

**Option 1** — just use the full path (no alias issue):
```
/home/lzw/sglang-venv/bin/python -m sglang.launch_server --model Qwen/Qwen2.5-3B-Instruct --port 30000 --host 0.0.0.0
```

**Option 2** — unalias first, then activate:
```
unalias python && source /home/lzw/sglang-venv/bin/activate && python -m sglang.launch_server --model Qwen/Qwen2.5-3B-Instruct --port 30000 --host 0.0.0.0
```

Option 1 is simplest. Just run that in tmux.
