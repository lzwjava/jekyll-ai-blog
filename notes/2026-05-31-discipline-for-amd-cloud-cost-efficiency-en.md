---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discipline for AMD Cloud Cost Efficiency
translated: false
type: note
---

**Question:** How to save money on AMD Dev Cloud ($1.99/hr) by clearing distractions — stop Warp/agent sessions, parallel tasks, and focus only on training?

**Answer:**

Yes, exactly right. The AMD MI300X is a compute resource, not a dev environment. Every minute you're paying for it should be GPUs doing work, not your terminal sitting idle in a Warp session.

Here's the discipline:

## Before Starting the Instance

1. **Prep everything locally first** — training script finalized, config tuned, dataset staged, dependencies listed
2. **No debugging on the paid instance** — debug on your MacBook or workstation first
3. **Write a single launch script** — one command should kick off the full training run

## On the Instance: Minimize Idle Time

```bash
# Don't use interactive Warp sessions — use tmux + detach immediately
tmux new -s train
python train.py --config config.yaml
# Ctrl+B, D  ← detach, instance keeps running, you don't need to watch it

# Or just nohup it and disconnect entirely
nohup python train.py > train.log 2>&1 &
echo $! > train.pid
```

## Kill Everything That Isn't Training

```bash
# Check what's running
ps aux | grep python

# Kill any lingering agent/tool sessions
pkill -f "warp"
pkill -f "claude"
pkill -f "cursor"

# Minimal env — no editors, no agents, no extra terminals
```

## Auto-Shutdown When Done (most important)

```bash
# Append to your train script or run after
python train.py && sudo shutdown -h now

# Or with a trap for errors too
python train.py; EXIT_CODE=$?; sudo shutdown -h now; exit $EXIT_CODE
```

This way the instance dies the moment training finishes, even if you're asleep.

## Checkpoint Aggressively

```bash
# Save every N steps so a crash doesn't waste a full run
# In your training loop:
if step % 500 == 0:
    torch.save(model.state_dict(), f"ckpt_{step}.pt")
```

## Cost Math

At $1.99/hr, 1 idle hour = ~$2 wasted. A 10-hour run left running 2 extra hours because you forgot to kill it = $4 gone. Auto-shutdown pays for itself immediately.

**Summary of the discipline:**
- Local: write, debug, test on CPU/small batch
- AMD: launch training, detach, auto-shutdown
- No agents, no Warp sessions, no parallel exploration on the paid box
