---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rendezvous in Distributed LLM Training
translated: false
type: note
---

**Question:** What does "rendezvous" mean in computing, and specifically in distributed LLM training?

**Answer:**

## Core concept

"Rendezvous" (French for "meeting point") in computing means: **multiple independent processes agreeing to meet, synchronize, and exchange information before proceeding together.** No process moves forward until all expected participants have shown up.

## In distributed LLM training (the meaning you care about)

When you launch multi-GPU/multi-node training with `torchrun`, the **rendezvous** is the bootstrap phase where all workers:

1. **Discover each other** — every process contacts a known endpoint (the rendezvous backend, usually a TCP store on the master node)
2. **Agree on membership** — confirm that exactly `world_size` workers exist
3. **Assign ranks** — each process gets a unique `rank` (0..N-1) and `local_rank`
4. **Establish the communication group** — after rendezvous, NCCL/Gloo process groups are created so `all_reduce`, `all_gather` etc. can run

This is why every distributed PyTorch script starts with:

```python
import torch.distributed as dist

# This call BLOCKS until all world_size processes have rendezvoused
dist.init_process_group(
    backend="nccl",
    init_method="env://",   # reads MASTER_ADDR, MASTER_PORT, RANK, WORLD_SIZE
)
rank = dist.get_rank()
world_size = dist.get_world_size()
```

And the launcher side, where rendezvous flags are explicit:

```bash
# Node 0 (master)
torchrun \
  --nnodes=2 --nproc_per_node=8 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=<IP_ADDRESS>:29500 \
  --rdzv_id=my_job_42 \
  train.py

# Node 1 — identical command, same rdzv_endpoint
```

- `--rdzv_backend=c10d`: PyTorch's built-in TCPStore-based rendezvous (no etcd needed)
- `--rdzv_endpoint`: the meeting point — host:port everyone connects to
- `--rdzv_id`: a job ID so two jobs on the same cluster don't accidentally join each other

## How it works under the hood (c10d backend)

The master node runs a `TCPStore`. Each worker does roughly:

```python
# Simplified mental model of what happens inside init_process_group
store = TCPStore(master_addr, master_port, world_size, is_master=(rank == 0))
store.set(f"worker_{rank}", my_nccl_info)      # announce yourself
store.wait([f"worker_{r}" for r in range(world_size)])  # block until everyone arrives
# rank 0 generates the NCCL unique ID, others read it from the store
# → NCCL communicators are built, training can start
```

That blocking `wait` **is** the rendezvous. If one node is slow to boot, everyone waits. If it never arrives, you get the classic `timeout in rendezvous` error after `--rdzv_timeout` (default 600s).

## Elastic rendezvous

`torchrun` (TorchElastic) extends this: rendezvous can **re-run** when workers die or join. With `--nnodes=2:4` (min:max), if a node crashes, surviving workers re-rendezvous, re-assign ranks, reload from checkpoint, and continue. The rendezvous is no longer a one-time bootstrap — it's a recurring consensus round. This is how fault-tolerant large-scale training (and DeepSeek-style multi-thousand-GPU runs) survives hardware failures without restarting the whole job.

## Other places the word appears

- **Rendezvous hashing (HRW)**: consistent-hashing alternative — each node scores `hash(key, node)`, highest score wins. Used for sharding KV caches and distributing requests in inference clusters.
- **Ada/CSP rendezvous**: synchronous message passing where sender and receiver must both arrive before data transfers (vs. async queues).
- **Kubernetes/Slurm ML jobs**: the rendezvous endpoint is what your job spec's headless service or `MASTER_ADDR` env points at.

## Quick experiment for your RTX 4070 box

Single machine, 1 GPU, but you can still watch rendezvous happen with 2 CPU processes:

```bash
torchrun --nproc_per_node=2 --rdzv_backend=c10d \
  --rdzv_endpoint=localhost:29500 - <<'EOF'
import os, torch.distributed as dist
dist.init_process_group("gloo")
print(f"rank {dist.get_rank()}/{dist.get_world_size()} rendezvoused, pid={os.getpid()}")
dist.barrier()  # another mini-rendezvous: all ranks meet here
dist.destroy_process_group()
EOF
```

Kill one process mid-run and you'll see the rendezvous/timeout machinery fire — useful intuition before you scale nanoGPT to multi-node on the MI300X cloud.

**References:**

- [PyTorch Elastic Rendezvous docs](https://pytorch.org/docs/stable/elastic/rendezvous.html)
- [torchrun documentation](https://pytorch.org/docs/stable/elastic/run.html)
- [Rendezvous hashing (Wikipedia)](https://en.wikipedia.org/wiki/Rendezvous_hashing)
