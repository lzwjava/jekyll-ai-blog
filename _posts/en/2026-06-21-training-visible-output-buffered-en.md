---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Visible, Output Buffered
translated: false
type: note
---

Found it. The training IS running — the checkpoint file (1.49GB, updated at 22:41) proves it. But the log is dead because of **Python stdout buffering**.

When Python's stdout is piped through `tee`, it's not a TTY, so Python fully buffers output instead of line-buffering. The `print()` calls in train.py are sitting in a pipe buffer and never flushing to `/tmp/train.log`.

The log file's last modified time is 21:16 (only the initial warnings). The process is piped (`fd/1 -> pipe`), confirming the buffering issue.

**Training is fine, just invisible output.** To fix for future runs, either:

- Set `PYTHONUNBUFFERED=1` in the launch command
- Or add `-u` flag: `python3 -u train.py ...`

The checkpoint at `out-github-code-124m/ckpt.pt` (1.49GB) was saved moments ago, so it's actively training. You're just flying blind on loss/metrics. Want me to kill and restart with unbuffered output, or let it finish and check the checkpoint stats?
