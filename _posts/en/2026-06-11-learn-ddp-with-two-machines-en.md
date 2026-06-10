---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learn DDP with Two Machines
translated: false
type: note
---

**Question:** Given my two machines (i9-13900KF + RTX 4070 box, and a CUDA-less i5-12450H laptop), which of the three nanochat DDP options should I pick to actually *learn* distributed training?

**Answer:**

Do **1 → 2 in sequence as a learning exercise (one evening), then use Option 3 for any real training**. They answer different questions:

- Option 1 teaches you the DDP *mechanics* (process groups, ranks, gradient allreduce) with zero networking variables.
- Option 2 teaches you the *systems* reality of distributed training — rendezvous, NIC selection, allreduce over Ethernet, and the straggler problem. This is the knowledge that transfers to multi-node MI300X/H100 clusters later.
- Option 3 teaches you nothing new (`--nproc_per_node=1` means DDP wraps a single process; allreduce is a no-op). It's just the correct way to train for real.

### Step 1: The Gloo patch (needed for both 1 and 2)

In `nanochat/common.py`, `compute_init()` gates DDP on CUDA. Change the backend selection instead:

```python
# before
if is_ddp_requested and device_type == "cuda":
    init_process_group(backend="nccl")
    ...

# after
if is_ddp_requested:
    backend = "nccl" if device_type == "cuda" else "gloo"
    init_process_group(backend=backend)
    if device_type == "cuda":
        torch.cuda.set_device(ddp_local_rank)
```

Gloo is PyTorch's CPU-capable collective backend — ring allreduce over TCP instead of NVLink/IB. Also make sure any `torch.compile` or bf16 autocast paths don't assume CUDA when `device_type == "cpu"`.

### Step 2: Option 1 — local 4-process CPU DDP on the i9 box

```bash
torchrun --nproc_per_node=4 --standalone \
    -m scripts.base_train --device-type=cpu --depth=4 --max-seq-len=512 \
    --device-batch-size=1 --total-batch-size=512 --num-iterations=20
```

Verify it's actually doing DDP: print `dist.get_world_size()` and confirm loss is identical across ranks after step 1 (gradients synced → identical weights). Then benchmark `--nproc_per_node=1` vs `2` vs `4` tokens/sec. You'll likely see sublinear scaling because the 12450H... wait, this is the i9 — you'll see decent scaling up to physical cores, then it flattens. That curve *is* the lesson.

### Step 3: Option 2 — multi-node across the LAN

First, **match torch versions** — Gloo across 2.12.0 and 2.9.1 is asking for serialization/protocol mismatches. Pin the laptop to the same version as the workstation:

```bash
# on the i5 laptop
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu
```

Then, on the i9 box (master):

```bash
export GLOO_SOCKET_IFNAME=<your_ethernet_iface>   # check with: ip route get <IP_ADDRESS>
torchrun --nnodes=2 --node_rank=0 --nproc_per_node=2 \
    --master_addr=<MASTER_IP> --master_port=29500 \
    -m scripts.base_train --device-type=cpu --depth=4 ...
```

On the i5 laptop:

```bash
export GLOO_SOCKET_IFNAME=<your_ethernet_iface>
torchrun --nnodes=2 --node_rank=1 --nproc_per_node=2 \
    --master_addr=<MASTER_IP> --master_port=29500 \
    -m scripts.base_train --device-type=cpu --depth=4 ...
```

Two things you'll observe, both worth internalizing:

1. **Stragglers.** DDP is synchronous — every step blocks on the slowest rank's allreduce. The i5 will drag the i9 down to its pace. This is exactly why production clusters use homogeneous nodes, and why heterogeneous setups need pipeline parallelism or async schemes instead of vanilla DDP.
2. **Comm cost.** A depth-4 nanochat model has tens of millions of params; allreduce moves ~2×P×4 bytes per step over (probably) 1 GbE ≈ 125 MB/s. Compute the expected comm time per step, then measure it. When measured ≫ computed, you've found bucketing/latency overhead — the same analysis you'd do sizing interconnect on a real cluster.

### Then: Option 3 for actual training

The RTX 4070 will outrun both CPU setups combined by 1–2 orders of magnitude for transformer training (tensor cores + bf16). Once the learning exercise is done, `run_rtx4070.sh` is the right tool — and your mental model from steps 1–2 maps directly onto `--nproc_per_node=8` NCCL runs when you next rent an 8×MI300X node.

One concrete artifact to produce from this: a table of tokens/sec for {1-proc CPU, 4-proc CPU, 2-node CPU, single 4070}, plus measured allreduce time per step. That's a blog-post-worthy benchmark for your notes and forces you to instrument the code rather than just run it.
