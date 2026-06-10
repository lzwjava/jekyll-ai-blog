---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two-Node DDP Hang Debugging
translated: false
type: note
---

**Question:** Explain what's happening in this transcript — an agent (Hermes) debugging a stuck 2-node distributed nanochat CPU training run.

**Answer:**

This is a classic DDP hang-debugging session. Your agent is running nanochat's `base_train` across two machines (master `.36` on ethernet, worker `.47` on WiFi) using `torchrun` with the **gloo** backend (CPU-only collectives), and the run froze. Here's the play-by-play:

**1. Diagnosing the hang: 0% CPU = blocked in a collective**

```bash
top -b -n1 -p 603 | tail -3   # master PID
top -b -n1 -p 52262 | tail -3 # worker PID
```

Both processes alive but at 0% CPU. That's the signature of a process blocked on a network `recv()` inside a collective op (`all_reduce`, `broadcast`) — not computing, not crashed, just waiting forever for a peer that never arrives. If it were merely *slow compute*, you'd see ~100% CPU. The `strace -e trace=network` attempt was the right instinct (you'd see it parked in `recvfrom`/`poll`), though the shell syntax with `&;` was botched.

**2. First hypothesis: data shard mismatch**

Master had 201 parquet files (`base_data_climbmix`), worker had 4 (`base_data_small`). In DDP this is a real deadlock source: each rank's dataloader iterates independently, and gradients sync via `all_reduce` *per step*. If rank 0 thinks there are more batches than rank 1, rank 1 exits its loop while rank 0 blocks in `all_reduce` waiting for a partner — permanent hang, no error. Hence the agent pinning both to `NANOCHAT_DATA_DIR=.../base_data_small` (though notably it only exported that on the master in the restart — worth checking the worker resolves the same shards).

**3. The actual finding: bf16 auto-detection on a CPU run**

The log showed `COMPUTE_DTYPE: torch.bfloat16 (auto-detected: CUDA SM 89)`. The dtype-selection logic checked `torch.cuda.is_available()` — true on `.36` because the RTX 4070 (SM 8.9 = Ada) is physically present — even though training was launched with `--device-type cpu`. So it picked bf16 for a CPU run. PyTorch's CPU bf16 kernels are dramatically slower than fp32 on chips without AMX/AVX512-BF16 (lots of up/down conversion, fewer fused paths). Fix: `export NANOCHAT_DTYPE=float32`.

Small nuance the agent glossed over: bf16-slow and collective-deadlock are *different* symptoms (high CPU vs 0% CPU). Likely both were in play — e.g., one rank crawling through bf16 init/eval while the other sat blocked at the first sync point, looking like a deadlock. The restart fixed both candidate causes at once, which is pragmatic but doesn't isolate which one actually killed it.

**4. The restart command, decoded**

```bash
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
  --master_addr=<MASTER_IP> --master_port=29500 \
  -m scripts.base_train -- --device-type cpu --depth 4 \
  --aspect-ratio 64 --head-dim 64 --max-seq-len 512 \
  --device-batch-size 2 --total-batch-size 2048 ...
```

- `GLOO_SOCKET_IFNAME=enp4s0` / `wlp3s0` — pins gloo to the right NIC. Without this, gloo can bind to a docker bridge or virtual interface and ranks never find each other (another silent-hang source). Smart inclusion.
- `NANOCHAT_FORCE_SDPA=1` — skip FlashAttention (CUDA-only), use PyTorch SDPA.
- Model math: `depth=4`, `aspect_ratio=64` → d_model = 256; `head_dim=64` → 4 heads. A toy ~3-5M param model, appropriate for a CPU connectivity test.
- Batch math: 2 ranks × batch 2 × seq 512 = 2048 tokens = `total_batch_size`, so **exactly 1 micro-step per optimizer step, zero gradient accumulation** — every step does one all-reduce.

**One thing to watch:** the worker syncs gradients over WiFi (`wlp3s0`). Even for this tiny model, each step ships full gradients both ways; over WiFi latency that all-reduce will dominate step time. Fine for a 10-iteration smoke test, but for anything real, get `.47` on ethernet — gloo ring all-reduce over WiFi is the bottleneck, not the CPUs.
