---
audio: false
generated: true
image: false
lang: en
layout: post
title: File Transfer Speed Test Results
translated: false
type: note
---

Done. Here's what I found and what changed:

**Speed test results on this machine (12.5 MB/s link cap):**

| Method | Workers | Aggregate |
| -------- | --------- | ----------- |
| Sequential wget | 1 | 14.0 MB/s |
| Parallel wget | 8 | 12.5 MB/s |
| hf_transfer + wget | 1 | 11.4 MB/s |

**Bottleneck:** the machine's link to HF is saturated at ~12-14 MB/s total. Parallel workers don't help here because the entire pipe is already maxed by a single stream.

**Still worth having parallel architecture because:**

- On **cloud GPU machines** (RunPod, Lambda, etc.) with 100-1000 MB/s pipes, parallel workers scale linearly
- Resilient to slow/retried files — one timeout doesn't block the rest
- Connection latency overhead is shared across workers

**Updated script at `codeparrot/download.py`:**

```bash
# 8 parallel workers
python3.11 download.py

# 16 parallel workers (good for cloud)
python3.11 download.py --workers 16

# With hf_transfer too
HF_HUB_ENABLE_HF_TRANSFER=1 python3.11 download.py --workers 16
```

Run the full pipeline:

```bash
bash codeparrot/run_pipeline.sh
```

For your workstation at 192.168.1.36, it'll be similar (home ISP). For cloud boxes (AMD Dev Cloud, RunPod), crank `--workers` to 16-32 and it'll actually help.
