---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mapping Tmux to PID and Process Validation
translated: false
type: note
---

## Review of my approach

**What worked**
- Parallelized independent reads (both `capture-pane`, then config + ls).
- Cross-referenced the running PID with the tmux output to confirm which config was active.

**Weaknesses**
1. **Captured both tmux panes blindly.** I ran `capture-pane -t 0` and `-t 1` in parallel before checking whether they were different views. They were identical (same training, two attached clients). Better: one capture first, or `tmux list-panes -a -F '#{session_name} #{pane_tty} #{pane_pid}'` to map sessions to the actual `train.py` PID.

2. **Used a stale snapshot.** `capture-pane` returned the visible scrollback. The last iter shown was 6800, but the process has been running for ~18 hours (1089 CPU-min, started Apr 29) and the checkpoint timestamp (06:42) is from step 6500 — current iter is almost certainly past 7000 by now. I should have noted the snapshot's freshness, or grabbed more scrollback (`-S -500`), or watched a few seconds of live output to confirm it's still advancing.

3. **No liveness check.** I never verified the GPU is actually doing work right now. A `nvidia-smi` would confirm training isn't hung; `ps` only shows the process exists.

4. **ETA was rough.** I averaged 9.34s/iter and added a small fudge for checkpoint saves, but ignored that every 500th iter does a val pass. The eval log line at step 5000 also shows ~29s for that iter — that overhead repeats every 500 iters, not every 1000. Real ETA is probably ~20–30 min longer than I quoted.

5. **Didn't sanity-check disk.** Checkpoint is 1.4 GB and rewrites in place, so it's bounded — but I should have glanced at `df` since OOD writes would silently kill training.

**What I'd do differently next time:** map tmux→PID first, then one fresh capture of the correct pane plus `nvidia-smi` and `df -h .` — fewer redundant calls, stronger answer.