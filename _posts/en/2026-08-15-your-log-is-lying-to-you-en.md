---
audio: false
generated: true
image: false
lang: en
layout: post
title: Your log is lying to you
translated: false
type: note
---

Here's the full picture:

## Training is fine — your log is lying to you

**The process is not stuck.** It's actively computing right now (confirmed via `py-spy`: it's inside a Triton kernel at `train.py:331`, GPU at 100%, 8.7 GB VRAM, 202 W).

**Real progress is way past iter 1900.** The checkpoint in `out-bilingual/ckpt.pt` contains `iter_num = 4500`, and that file was last written at **17:12:56** — about 3 minutes ago when I checked. The math checks out perfectly: from iter 1900 (04:16) to iter 4500 (17:12) is 2600 iters in 12.9 h = **17.9 s/iter**, exactly matching the ~17.8 s/iter in the logs.

**Why the log/terminal froze at "iter 1900":** `train.py` uses plain `print()` (no `flush=True`), and stdout through `| tee` is block-buffered — the log and tmux pane only show the last ~8 KB flush (which happened at 04:16). The buffered lines since then (~130 lines) will dump all at once when the process exits. To see live progress next time: `python3.12 -u train.py ...` or `PYTHONUNBUFFERED=1`.

## ETA: finish ~19:40–19:45 HKT today (Aug 15)

- `max_iters = 5000`, currently at ~iter 4520 (4500 saved at 17:12:56)
- ~500 iterations left × 17.9 s ≈ **2.5 hours** (final eval + checkpoint save at 5000 included)
- So from now (~17:16): done around **19:40–19:45**, roughly 2.5 h away

You'll know it finished when the tmux pane shows `step 5000: ...` + `saving checkpoint to out-bilingual`, then the shell prompt with `EXIT_CODE=0`. The real-time way to verify progress meanwhile: `python3.12 -c` won't be needed — just check `out-bilingual/ckpt.pt`'s mtime; it updates every 250 iters (~74 min apart: next at ~18:27 for 4750, final at ~19:42 for 5000).