---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compute-Bound vs Attention-Bound Scaling
translated: false
type: note
---

Question: Is a 5-6 machine AI studio setup worth it? Agents don't benefit much (should be 2-3 max, session bandwidth is the bottleneck), but embedded/mobile dev (Arduino compile, Android/iOS + device tethering) clearly benefits, and GPU/CPU-heavy research (kernel hacking, long benchmarks) clearly benefits too. For a serious AI researcher, is 2 local GPU boxes the baseline, since pretrain/SFT runs (data download + training) eat 30min-several hours?

Answer:

Your reasoning is basically correct, and it maps to a simple axis: **is the task human-attention-bound or compute-bound?**

**Agent work is attention-bound, not machine-bound.** You are the scheduler. Running 5-6 parallel Claude Code / agent sessions doesn't scale because you can only meaningfully review/steer 2-3 concurrent diffs before context-switching cost eats the gain. This is the same reason human engineering managers cap direct reports — not a tooling limit, a working-memory limit. So 2-3 machines (or just 2-3 tmux panes on one machine) is the real ceiling regardless of how much hardware you own.

```bash
# this is the actual bottleneck pattern — not more machines, better multiplexing
tmux new-session -d -s agent1 'zz run task1.md'
tmux new-session -d -s agent2 'zz run task2.md'
tmux new-session -d -s agent3 'zz run task3.md'
tmux ls   # you're the scheduler polling 3 panes, not 6
```

**Notification-on-completion is a solved problem, don't let it block the decision:**

```bash
# wrap any long agent/training job
task_cmd; curl -d "done: $?" ntfy.sh/<YOUR_TOPIC>
```

or a webhook to Bark/ntfy/Slack. This isn't a reason to reduce to fewer machines — it's a 5-line fix regardless of machine count.

**GPU/CPU research is compute-bound, and here more machines genuinely help — but only if:**

1. You're running independent experiments (hparam sweeps, ablations) — trivially parallel across boxes, no interconnect needed.
2. You're NOT trying multi-node distributed training across cheap desktop GPUs — without NVLink/InfiniBand, NCCL all-reduce over gigabit/10GbE ethernet will bottleneck you badly before you get any benefit from the second box. Multi-node only pays off with real interconnect (RDMA/IB) or if you're doing data-parallel with infrequent sync (federated-style, not tight DDP).

For your case — GPT-2 760M on MI300X, ~2B tokens/mo — you don't need multi-node. You need:

- 1-2 boxes with the biggest single-GPU memory you can afford (MI300X 192GB already solves most of this)
- A second box mainly for **overlap**: while box A trains, box B does data prep / eval / a different ablation. That's the actual justification for "2 local GPUs is baseline" — not distributed training, but pipeline overlap so the 30min-few-hour data download + preprocessing isn't dead GPU-idle time on your only machine.

```python
# the real pattern that justifies box #2 — overlap, not distributed training
# box A: training
torchrun --nproc_per_node=8 train.py --resume_from ckpt

# box B (in parallel): next shard prep + eval of previous ckpt
python prepare_shard.py --shard next
python eval.py --ckpt ckpt_prev
```

So: 2 boxes = compute overlap, justified. 5-6 boxes = mostly idle unless you're running independent ablation sweeps or doing embedded/mobile toolchain work that genuinely needs separate OS/arch targets (Android NDK, Xcode, Ardupilot build). Your instinct to cut back to 2-3 is right — the extra machines were solving a scheduling problem (your attention) with hardware, which doesn't work.

I don't recognize what tool you mean by "龙虾" (lobster) here — if you mean a specific session/task orchestrator, tell me the name and I'll look at whether it's actually a better fit than tmux+zz for this.

References:

- [NCCL and multi-node scaling limits](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)
- [ntfy.sh — simple pub/sub notifications for long-running jobs](https://ntfy.sh/)
- [tmux manual](https://github.com/tmux/tmux/wiki)
