---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning Distributed Training Systems Reality
translated: false
type: note
---

**Question:** Extend the section on Option 2 — distributed training across my own machines as a way to learn the systems reality (rendezvous, NIC selection, allreduce over Ethernet, stragglers) that transfers to multi-node MI300X/H100 clusters.

**Answer:**

Option 2 teaches you the systems reality of distributed training — rendezvous, NIC selection, allreduce over Ethernet, and the straggler problem. This is the knowledge that transfers to multi-node MI300X/H100 clusters later. Here's the extended version of why, with the math and the code.

## 2.1 The bandwidth math — do this before launching anything

Every DDP step ends with an allreduce of the full gradient. For GPT-2 760M in bf16:

```
gradient size S = 760e6 params × 2 bytes ≈ 1.52 GB
```

Ring allreduce moves `2(N-1)/N × S` bytes through each node's NIC per step. For N=2 ranks that's ~1.52 GB in and ~1.52 GB out, per step.

```python
# comm_cost.py — know your step time before you burn a weekend
params = 760e6
bytes_per_param = 2            # bf16 grads
N = 2                          # ranks
S = params * bytes_per_param
traffic = 2 * (N - 1) / N * S  # bytes per rank per step

for name, gbps in [("1GbE", 1), ("2.5GbE", 2.5), ("10GbE", 10), ("RoCE 400G", 400)]:
    bw = gbps * 1e9 / 8 * 0.85          # ~85% effective
    print(f"{name:10s} allreduce ≈ {traffic / bw:6.2f} s/step")
```

Output: **~14 s/step on 1GbE, ~1.4 s on 10GbE, ~36 ms on 400G RoCE.** Your 4070's compute step on 760M is on the order of 1–2 s. So over a home 1GbE link you're 10× comm-bound — and that's the *entire lesson of clusters* compressed into one number. The ratio `T_comm / T_compute` is the same quantity people tune on H100 pods with NVLink + InfiniBand; only the constants change. Knowing how to compute it from first principles is the transferable skill.

The standard levers, in the order real clusters apply them:

1. **Gradient accumulation** — sync every K micro-steps, cutting comm by K×. The one-line fix for slow interconnects.
2. **Overlap** — DDP buckets gradients (`bucket_cap_mb`) and allreduces bucket *i* while backward computes bucket *i+1*. Free speedup if backward is long enough to hide comm.
3. **Compression** — `PowerSGD` or bf16→fp16 comm hooks (`ddp.register_comm_hook`).
4. **Better fabric** — which is why clusters buy InfiniBand instead of clever software.

## 2.2 Rendezvous and NIC selection — the part that actually breaks

`torchrun` uses a c10d rendezvous: rank 0 hosts a TCP store, everyone else dials in. On your LAN:

```bash
# On the workstation (rank 0, RTX 4070):
NCCL_SOCKET_IFNAME=enp5s0 GLOO_SOCKET_IFNAME=enp5s0 \
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
  --rdzv_backend=c10d --rdzv_endpoint=<WORKSTATION_IP>:29500 \
  train.py

# On the second machine (rank 1):
GLOO_SOCKET_IFNAME=en0 \
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=1 \
  --rdzv_backend=c10d --rdzv_endpoint=<WORKSTATION_IP>:29500 \
  train.py
```

The failure modes you'll hit here are *identical in kind* to cluster failures:

- **Wrong interface picked.** NCCL/Gloo auto-detect can grab `docker0`, a VPN tun, or Wi-Fi instead of the wired NIC. Hangs at init with no error. Fix: `NCCL_SOCKET_IFNAME` / `GLOO_SOCKET_IFNAME`, and `NCCL_DEBUG=INFO` to see what it chose. On MI300X clusters the same env var (RCCL honors it) plus `NCCL_IB_HCA` selects which RDMA rail you ride.
- **Firewall/port mismatch.** Rendezvous needs 29500 plus ephemeral ports. `ufw allow from 192.168.x.0/24` and move on.
- **Backend choice.** NCCL needs CUDA on both ends. Your M2 Air has no CUDA, so a Mac+workstation run must use `gloo` (CPU tensors, or copy grads to CPU). That's fine — the point is learning the choreography, not the throughput. RCCL on MI300X is API-identical to NCCL, so everything you learn transfers verbatim.

Minimal `train.py` skeleton:

```python
import os, torch, torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group(backend="gloo")  # "nccl"/"rccl" when both ends have GPUs
rank, world = dist.get_rank(), dist.get_world_size()

device = "cuda" if torch.cuda.is_available() else "cpu"
model = DDP(build_gpt2_760m().to(device))

# sanity probe: measure real allreduce bandwidth before training
x = torch.randn(64 * 1024 * 1024 // 4, device=device)  # 64 MB
torch.cuda.synchronize() if device == "cuda" else None
import time; t0 = time.time()
dist.all_reduce(x)
dt = time.time() - t0
print(f"rank {rank}: allreduce 64MB in {dt*1e3:.1f} ms → {64/1024/dt:.2f} GB/s effective")
```

Run that probe first. Comparing it against raw `iperf3 -c <WORKSTATION_IP>` tells you how much the collective stack costs versus the wire — the same methodology as running `nccl-tests` (`all_reduce_perf`) on a new cluster before trusting it.

## 2.3 The straggler problem — synchronous SGD's tax

DDP is bulk-synchronous: every step, all ranks meet at the allreduce. Step time = max over ranks. Pair a 4070 with an M2 (or with the MI300X over WAN) and the fast rank idles 80–95% of the time.

This is not a toy problem — it's *the* scaling problem. On a 1,024-GPU job, one GPU thermal-throttling, one flaky NIC, or one slow DataLoader worker gates the whole cluster. The mitigations you'd learn here are the production ones:

- **Balance work, not ranks**: give the slow rank a smaller micro-batch (DDP allreduces *averaged* gradients, so reweight by sample count yourself), or give the fast rank more gradient-accumulation steps between syncs.
- **Find stragglers with the profiler**: `torch.profiler` shows allreduce wait time per rank; on clusters this is the first chart anyone looks at.
- **Timeouts as canaries**: `init_process_group(timeout=timedelta(seconds=120))` — a hang at a collective means a dead/slow rank, and elastic rendezvous (`--max-restarts`) is how torchrun recovers. This is the mechanism underneath fault-tolerant training at scale.

## 2.4 What maps directly to MI300X/H100 clusters

| Home-lab concept | Cluster equivalent |
|---|---|
| `GLOO/NCCL_SOCKET_IFNAME` on 1GbE | `NCCL_IB_HCA`, rail-optimized RoCE/IB (8×400G per node) |
| c10d rendezvous on your LAN | Same c10d under Slurm/Kubernetes; `MASTER_ADDR` from the scheduler |
| Ring allreduce cost model | Identical formula; intra-node goes over xGMI/NVLink (~448 GB/s on MI300X) instead of the NIC |
| Gradient accumulation to hide slow links | Same lever, plus overlap and pipeline parallelism |
| Straggler gating your 2 ranks | Straggler gating 1,024 ranks; same detection, bigger blast radius |
| DDP (model fits per-GPU) | FSDP/ZeRO when it doesn't — sharding adds allgather/reduce-scatter, and your cost model extends to those collectives the same way |

The honest framing: as a *speedup*, two heterogeneous home machines over Ethernet is a bad deal. As a **$0 cluster simulator**, it's excellent — you'll debug rendezvous hangs, read `NCCL_DEBUG` output, measure collectives, and internalize the comm/compute ratio. Then when you spin up 2× MI300X droplets on AMD Dev Cloud and run the same `torchrun` command with RCCL, nothing will surprise you.

**References:**

- [PyTorch DDP internals (bucketing, overlap)](https://pytorch.org/docs/stable/notes/ddp.html)
- [torchrun / elastic rendezvous](https://pytorch.org/docs/stable/elastic/run.html)
- [NCCL environment variables](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)
- [nccl-tests (allreduce benchmarking)](https://github.com/NVIDIA/nccl-tests)
- [DDP communication hooks (PowerSGD, fp16)](https://pytorch.org/docs/stable/ddp_comm_hooks.html)
