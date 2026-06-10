---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attention Build in Progress
translated: false
type: note
---

Build is actively compiling — 3 nvcc/cc1plus processes running. Disk holding steady at 34GB free.

Status:
- tmux session: `flash-build` on lzw@192.168.1.36
- Target arch: sm_89 (RTX 4070 only — much faster than multi-arch)
- Log: `/tmp/flash-attn-build.log`
- ETA: ~30-60 min for full CUDA kernel compilation

You can check anytime with:
```
ssh lzw@192.168.1.36 "tmux capture-pane -t flash-build -p | tail -10"
```

Or watch the log:
```
ssh lzw@192.168.1.36 "tail -f /tmp/flash-attn-build.log"
```
