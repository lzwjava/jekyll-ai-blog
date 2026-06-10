---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two CPU Laptops Speed Up Training
translated: false
type: note
---

**Question:** What about two Ubuntu laptops with no dedicated GPU at all — both CPU-only?

**Answer:**

Funny enough, this is the **only one of your three configurations where distributed training actually delivers a real speedup**. Here's why: DDP scaling dies when ranks are heterogeneous (straggler stalls) or when communication can't hide under compute. Two CPU laptops are homogeneous, and CPU compute is so slow per step that the network has plenty of time to hide the all-reduce. Slow compute is, paradoxically, great for scaling efficiency.

**The scaling math:**

DDP overlaps gradient all-reduce with the backward pass (bucketed, ~25 MB buckets by default). Scaling is near-linear when `t_comm < t_backward`.

GPT-2 124M, fp32: ~496 MB of gradients per step.

- Gigabit Ethernet: ~4.5 s to all-reduce
- CPU backward (8-core mobile chip): ~15–30 s

Comm fully hides under backward → **~1.8–1.9× effective speedup** from the second laptop. Compare the 4070+CPU pair from the last answer, where the same math gave you a *slowdown*. For nanoGPT's shakespeare-char (10.65M params, ~43 MB grads, ~0.4 s comm), it's even more comfortably hidden.

**Setup — same script as before, both ranks on CPU, stock DDP:**

```python
# dist_train.py
import os, torch, torch.nn as nn, torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.data.distributed import DistributedSampler

def main():
    dist.init_process_group(backend="gloo")
    rank, ws = dist.get_rank(), dist.get_world_size()
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "8")))

    model = DDP(nn.Sequential(nn.Linear(768, 3072), nn.GELU(), nn.Linear(3072, 768)))
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

    # DistributedSampler gives each rank a disjoint shard — this is where the 2x comes from
    ds = TensorDataset(torch.randn(4096, 768))
    dl = DataLoader(ds, batch_size=32, sampler=DistributedSampler(ds))

    for epoch in range(3):
        dl.sampler.set_epoch(epoch)
        for (x,) in dl:
            loss = model(x).pow(2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        if rank == 0:
            print(f"epoch {epoch} loss {loss.item():.4f}")

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
```

```bash
# Laptop A (rank 0)
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=2 --node_rank=0 --nproc_per_node=1 \
  --master_addr=<LAPTOP_A_LAN_IP> --master_port=29500 dist_train.py

# Laptop B (rank 1)
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=2 --node_rank=1 --nproc_per_node=1 \
  --master_addr=<LAPTOP_A_LAN_IP> --master_port=29500 dist_train.py
```

**CPU-specific tuning that actually matters:**

1. **One process per node, all threads to it.** PyTorch CPU ops parallelize internally via OpenMP (intra-op parallelism). `nproc_per_node=2+` with split threads usually loses to one fat process — measure, but start with 1×`nproc` threads.
2. **Pin `OMP_NUM_THREADS` to *physical* cores**, not hyperthreads. GEMM-bound workloads degrade with SMT oversubscription: `lscpu | grep -E 'Core|Socket'`.
3. **bf16 autocast if your CPU has AVX-512/AMX** (recent Intel) — `torch.autocast("cpu", dtype=torch.bfloat16)` can give 2–4× on matmuls. Check: `lscpu | grep -o 'avx512_bf16\|amx_bf16'`.
4. **`torch.compile(model)`** — the inductor CPU backend fuses ops and often gives 1.3–2× on transformer blocks, and it stacks with DDP.
5. **Ethernet cable, not WiFi.** WiFi latency jitter punches holes in the comm/compute overlap. A $5 cable between the laptops (or both into the router) keeps the all-reduce deterministic.
6. **Power profile:** `sudo cpupower frequency-set -g performance` — laptop governors throttle sustained AVX loads hard, and a thermally-throttled rank becomes a straggler against its identical twin.

**Absolute-terms reality check:** two laptops × ~25 s/step on GPT-2 124M ≈ effective ~13 s/step. Your 4070 does ~0.25 s/step — one GPU ≈ **50 of these laptop pairs**. So the honest sizing is:

- **shakespeare-char / 1–10M param nanoGPT**: genuinely trains fine on this rig, minutes-to-hours, and the 2× is real. Good vibe-coding loop.
- **GPT-2 124M+**: technically converges, practically a space heater. Use the 4070 or the MI300X.

The interesting takeaway across all three of your configs: distributed efficiency is governed by two ratios — **rank homogeneity** and **t_backward / t_comm**. Two weak identical nodes scale beautifully; one strong + one weak node scales worse than the strong node alone. That intuition is exactly what bites people later at cluster scale (one slow NIC or thermally-throttled GPU drags 511 others), so this toy rig teaches the right lesson.
