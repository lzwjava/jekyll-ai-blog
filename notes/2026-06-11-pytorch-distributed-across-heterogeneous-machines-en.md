---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch Distributed Across Heterogeneous Machines
translated: false
type: note
---

**Question:** Can PyTorch distributed training run across two heterogeneous machines — a macOS machine (Apple silicon) and an Ubuntu machine with an RTX 4070?

**Answer:**

Yes, it runs — but only with the **gloo** backend, and with real caveats that make it a learning exercise rather than a speedup. Three hard constraints first:

1. **NCCL is out.** NCCL requires CUDA on every rank. Your Mac has no CUDA, so the whole job must use `gloo` (TCP-based, CPU collectives). This means even the 4070's gradients get staged through CPU RAM for the all-reduce.
2. **MPS ≠ Neural Engine, and gloo doesn't speak MPS.** PyTorch's `mps` backend runs on the M2's *Metal GPU* — the Apple Neural Engine (ANE) is not usable for PyTorch training at all (it's only reachable via Core ML, inference-only). And `gloo` collectives only accept CPU (and CUDA) tensors, so the Mac rank either trains on CPU, or trains on MPS with a manual grad copy MPS→CPU→all-reduce→MPS.
3. **DDP is synchronous.** The slowest rank gates every step. Your M2 is maybe 5–10× slower than the 4070 on a GPT-2-class forward/backward, so the 4070 mostly idles.

Minimal working setup, manual all-reduce so MPS works on the Mac:

```python
# dist_train.py — same file on both machines
import os, torch, torch.distributed as dist
import torch.nn as nn

def pick_device():
    if torch.cuda.is_available(): return "cuda"
    if torch.backends.mps.is_available(): return "mps"
    return "cpu"

def allreduce_grads(model, world_size, device):
    # gloo only handles CPU tensors -> stage grads through CPU
    for p in model.parameters():
        if p.grad is None: continue
        g = p.grad.detach().to("cpu")
        dist.all_reduce(g, op=dist.ReduceOp.SUM)
        p.grad.copy_((g / world_size).to(device))

def main():
    dist.init_process_group(backend="gloo")  # NCCL impossible here
    rank, ws = dist.get_rank(), dist.get_world_size()
    device = pick_device()
    torch.manual_seed(42)  # identical init on all ranks (or broadcast rank0's weights)

    model = nn.Sequential(nn.Linear(768, 3072), nn.GELU(), nn.Linear(3072, 768)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

    for step in range(100):
        x = torch.randn(32, 768, device=device)
        loss = model(x).pow(2).mean()
        opt.zero_grad(); loss.backward()
        allreduce_grads(model, ws, device)
        opt.step()
        if rank == 0 and step % 10 == 0:
            print(f"step {step} loss {loss.item():.4f} [{device}]")

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
```

Launch (Ubuntu box is rank 0 / rendezvous master):

```bash
# Ubuntu + 4070
torchrun --nnodes=2 --node_rank=0 --nproc_per_node=1 \
  --master_addr=<UBUNTU_LAN_IP> --master_port=29500 dist_train.py

# MacBook Air M2
torchrun --nnodes=2 --node_rank=1 --nproc_per_node=1 \
  --master_addr=<UBUNTU_LAN_IP> --master_port=29500 dist_train.py
```

If both ranks run on CPU, you can use stock `DistributedDataParallel(model)` directly — DDP+gloo+CPU is fully supported and overlaps the all-reduce with backward via bucketing. DDP does *not* support MPS modules, which is why the manual version above exists.

**Why it won't be faster than the 4070 alone — the bandwidth math:**

For GPT-2 124M in fp32, gradients are ~496 MB per step. Ring all-reduce moves `2(N-1)/N ≈ 1×` the payload per rank, so ~500 MB over your LAN per step. Gigabit Ethernet ≈ 117 MB/s real throughput → **~4–5 s of pure communication per step**, before the M2 straggler penalty and the MPS↔CPU copies. The 4070 alone does a 124M-param step in well under a second. WiFi makes it comically worse.

**Mitigations if you do it anyway (worth doing once to internalize the mechanics):**

- **Uneven batch sizes per rank** — e.g. 4070 takes batch 48, M2 takes 16, and you weight the gradient sum by sample count instead of dividing by `world_size`. This is the classic heterogeneous-DDP trick.
- **bf16 gradient compression** before the all-reduce halves the wire traffic (`g.to(torch.bfloat16)` → all_reduce → upcast).
- **Bucket the copies** — flatten all grads into one contiguous CPU tensor (`torch._utils._flatten_dense_tensors`) and do a single all-reduce instead of per-parameter calls; per-tensor gloo calls have brutal latency overhead.

**Practical verdict for your setup:** use this two-node rig to learn `torchrun`, rendezvous, ranks, and collective semantics — it's the same mental model as multi-node NCCL on the MI300X box, just slower. For actual training throughput, the 4070 solo beats the pair, and the MI300X at ~$2/hr beats everything else you own per dollar of wall-clock. The real payoff of the exercise is that when you move to 8×MI300X with RCCL, nothing about the code changes except `backend="nccl"` and `--nproc_per_node=8`.
