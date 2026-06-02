---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Monitoring GPU Usage with nvidia-smi
translated: false
type: note
---

To watch GPU usage change over time with `nvidia-smi`, you only need the loop flag:

**Basic live refresh**

```
nvidia-smi -l 1
```

This updates every 1 second. You can replace `1` with any interval in seconds.

**If you want more detailed stats (per-process usage)**

```
nvidia-smi pmon -s um -d 1
```

This shows per-process GPU utilization (`u`) and memory (`m`) every second.

**If you want full GPU statistics repeatedly**

```
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv -l 1
```

This prints a compact line each second with utilization and memory.

Let me know if you want the output logged to a file or need a custom format.
