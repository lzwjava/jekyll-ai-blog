---
audio: false
generated: true
image: false
lang: en
layout: post
title: Process Killed, Machine Recovered
translated: false
type: note
---

Process killed, machine recovered (51GB available again). Here's the full picture:

## What happened (half an hour ago)

**The machine didn't crash from a bug — it ran out of RAM and froze.** The journal shows the sequence:

| Time | Event |
|---|---|
| ~18:58 | `mixed_sample_2gb.txt` (2 GB) created; you launched `train_tokenizer.py` on it (`tok_train_sample.log` created 19:00) |
| 19:01:28 | `systemd-journald[747]: Under memory pressure, flushing caches` ← RAM exhausted |
| 19:02:17 | **Last log of the boot — no clean shutdown.** System hung/froze |
| 19:04:38 | Machine rebooted (boot list confirms: boot `-1` ended 19:02:17, boot `0` started 19:04:38) |

There's no OOM-killer or panic line because the machine froze from memory thrashing before the kernel could act (or you force-rebooted).

## Reproduction just now — confirmed

I re-ran exactly that command on the 2 GB sample with a memory monitor:

- **RSS climbed to ~35 GB within 8 minutes** (581% CPU, multithreaded Rust BPE)
- System available memory fell **54 GB → 13.5 GB in ~90 seconds** (~600 MB/s and accelerating)
- I killed it at that point — extrapolating, it would have eaten all 62 GB RAM **+ 33 GB swap**, then hung the box exactly like before

## Root cause

`ByteLevelBPETokenizer.train()` holds the **entire corpus in memory in the Rust trainer** — unique words + pair-count maps for a 65k vocab. The multiplier is roughly **15–20× the file size**:

- 2 GB sample → ~35+ GB (hangs your 62 GB box)
- full `mixed.txt` (11.5 GB) → ~180 GB+ — impossible on this machine

Training never even finished (no vocab.json/merges.txt written — the `tok_mixed/` outputs are from Aug 13 01:28, a different earlier run).

## Fix options

1. **Subsample the corpus** (recommended) — train on ~100–200 MB randomly sampled from `mixed.txt`. For a 65k vocab this is standard practice and plenty representative; memory drops to ~3 GB.
2. **Chunked/sampled lines** — stream lines and keep only a capped number of lines (same effect as #1, simpler).
3. Change `--vocab-size` won't help — memory is dominated by unique-word counts, not vocab size.

Want me to patch `scripts/train_tokenizer.py` to subsample/stream (e.g., a `--max-bytes` or `--sample-lines` option), then run the test on the 2 GB file safely?