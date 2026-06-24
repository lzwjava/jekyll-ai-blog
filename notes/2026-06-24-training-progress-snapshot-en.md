---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Snapshot
translated: false
type: note
---

Training is running smoothly in the `train` tmux session. Here's the snapshot:

  Iteration:  ~326,960
  Latest loss: 2.1948 (iter 326960)
  Step time:  ~621-622ms (very stable)
  MFU:        14.44% (plateaued)

The MFU (model FLOPs utilization) climbed from ~13.9% to ~14.44% early on and has been flat there for a while. Loss is fluctuating between ~1.5 and ~4.0, which is normal for per-step loss — the running average matters more. Step time is rock solid at 621-622ms, no slowdowns or stalls.
