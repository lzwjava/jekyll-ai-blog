---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attention 构建中
translated: true
type: note
---

构建正在进行中 — 3个nvcc/cc1plus进程正在运行。磁盘剩余空间稳定在34GB。

状态：

- tmux会话：`flash-build` 位于 lzw@192.168.1.36
- 目标架构：sm_89（仅限RTX 4070 — 比多架构编译快得多）
- 日志：`/tmp/flash-attn-build.log`
- 预计完成时间：完整CUDA内核编译约需30-60分钟

随时可通过以下命令检查：

```
ssh lzw@192.168.1.36 "tmux capture-pane -t flash-build -p | tail -10"
```

或查看日志：

```
ssh lzw@192.168.1.36 "tail -f /tmp/flash-attn-build.log"
```
