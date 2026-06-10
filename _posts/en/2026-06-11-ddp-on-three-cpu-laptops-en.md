---
audio: false
generated: true
image: false
lang: en
layout: post
title: DDP on Three CPU Laptops
translated: false
type: note
---

**Question:** What about three CPU-only Ubuntu laptops?

**Answer:**

Same story as two, slightly better throughput, slightly worse everything else. Nothing about the code changes except `--nnodes=3` — DDP doesn't care about node count or powers of two. The interesting part is what happens to the math.

**Communication cost grows sublinearly — the ring all-reduce formula:**

Ring all-reduce moves `2(N-1)/N × D` bytes per rank, where `D` = gradient size:

| N | Payload factor | GPT-2 124M (496 MB grads) over GbE |
|---|---------------|-------------------------------------|
| 2 | 1.00× | ~4.5 s |
| 3 | 1.33× | ~6.0 s |
| ∞ | 2.00× (asymptote) | ~9 s ceiling |

CPU backward is still ~15–30 s, so comm stays hidden. Expected scaling: **~2.6–2.8× over one laptop**. The all-reduce cost converging to a constant 2× payload regardless of N is *why* data parallelism scales to thousands of GPUs — you're seeing the same asymptote at toy scale.

One topology note: all three into the same gigabit **switch** (your router's LAN ports count). Each ring link is a separate full-duplex port-to-port path, so the switch doesn't bottleneck. Don't daisy-chain or mix WiFi in.

**Launch — same script, three commands:**

```bash
# Laptop A (rank 0, master)
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=3 --node_rank=0 --nproc_per_node=1 \
  --master_addr=<LAPTOP_A_LAN_IP> --master_port=29500 dist_train.py
# Laptop B
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=3 --node_rank=1 ... # same flags
# Laptop C
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=3 --node_rank=2 ... # same flags
```

**Three things that start to bite at N=3 that didn't at N=2:**

1. **Straggler tail statistics.** Each step waits for `max(t_1, t_2, t_3)`. With identical hardware, per-step time is the *maximum of N samples* from your step-time distribution — and that max grows with N. One laptop thermal-throttling under sustained AVX (very laptop-like behavior) caps the whole job. Mitigate: `cpupower frequency-set -g performance`, laptops elevated/cooled, watch `watch -n1 'grep MHz /proc/cpuinfo'` on each node.

2. **Fault tolerance is now a real concern.** Lid closes, WiFi power-save kicks in, one rank dies → the other two hang forever at the next all-reduce (gloo has no heartbeat by default). Two fixes:

```bash
# (a) timeout so hangs become errors
torchrun ... --rdzv_backend=c10d --rdzv_endpoint=<LAPTOP_A_LAN_IP>:29500
# in code: dist.init_process_group("gloo", timeout=datetime.timedelta(seconds=120))

# (b) elastic training — survives node loss, rescales world_size
torchrun --nnodes=1:3 --max_restarts=3 \
  --rdzv_backend=c10d --rdzv_endpoint=<LAPTOP_A_LAN_IP>:29500 dist_train.py
```

   Elastic (`--nnodes=min:max`) is worth trying once on this rig — it's the mechanism behind fault-tolerant cluster jobs, and checkpoint/resume logic you write for it transfers directly to real training runs.

3. **Global batch size and the LR scaling rule.** With per-rank batch 32, your global batch went 32 → 64 → 96 across these experiments. Same hyperparameters ≠ same training dynamics. The standard recipe (Goyal et al., "Accurate, Large Minibatch SGD"): scale LR linearly with global batch and warm up:

```python
base_lr = 3e-4          # tuned at global batch 32
lr = base_lr * (dist.get_world_size() * per_rank_bs) / 32
# + linear warmup over first ~200-500 steps
```

   At N=3 with a tiny model you'd barely notice, but this is the knob people forget when a run that converged on 1 node mysteriously diverges on 8.

**Diminishing-returns check:** 1 laptop = 1.0×, 2 = ~1.9×, 3 = ~2.7×, and each added laptop also adds a straggler lottery ticket and a failure point. Meanwhile the 4070 is still ~15–20× the whole trio. So the honest framing stays the same as before: this is a **distributed-systems lab, not a compute strategy** — and a genuinely good one. A 3-node elastic gloo cluster exercises rendezvous, ring collectives, stragglers, fault recovery, and batch-size scaling — the exact failure modes of a 512-GPU job, at zero cost. Run nanoGPT shakespeare-char on it, kill a node mid-run, watch elastic recover, then go rent the MI300X for the real thing.
