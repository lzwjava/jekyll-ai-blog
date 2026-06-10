---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PyTorch DDP: Data Parallelism Explained"
translated: false
type: note
---

**Question:** In PyTorch distributed training, does data parallelism mean splitting the training data across two GPUs, where each GPU holds the same model and they synchronize parameter updates?

**Answer:**

Yes — what you're describing is **data parallelism (DDP)**, the most common form. But your mental model needs one correction: GPUs don't "share" the model update — they each compute their own gradients, then **average gradients via all-reduce** before each one applies the identical update locally. Let's walk through it precisely.

## DDP mechanics, step by step

With 2 GPUs and per-GPU batch size 32:

1. **Replicate**: Each GPU holds a full copy of the model, initialized identically (rank 0 broadcasts weights at startup).
2. **Shard the data**: `DistributedSampler` partitions the dataset so each rank sees a disjoint slice. Effective global batch = 32 × 2 = 64.
3. **Forward + backward independently**: Each GPU computes loss on its own micro-batch and runs backward. At this point gradients *differ* between GPUs (different data!).
4. **All-reduce gradients**: NCCL averages gradients across ranks. This is the key sync point: `g = (g_0 + g_1) / 2`. After this, every rank holds *identical* gradients.
5. **Optimizer step locally**: Each rank runs `optimizer.step()` on its own copy. Since weights, gradients, and optimizer state are identical, the models stay in lockstep forever — no parameter broadcast needed after step 1.

The math: averaging gradients over shards is equivalent to computing the gradient of the mean loss over the full batch of 64 (assuming mean reduction in your loss). So DDP with N GPUs ≈ single-GPU training with N× batch size — which is why you often scale LR accordingly.

## Minimal DDP (this is exactly what nanoGPT does)

```python
# torchrun --nproc_per_node=2 train.py
import os, torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

dist.init_process_group(backend="nccl")
rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(rank)

model = MyModel().cuda(rank)
model = DDP(model, device_ids=[rank])

sampler = DistributedSampler(train_ds)          # disjoint shards per rank
loader = DataLoader(train_ds, batch_size=32, sampler=sampler)

opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

for epoch in range(epochs):
    sampler.set_epoch(epoch)                    # reshuffle shards each epoch
    for x, y in loader:
        x, y = x.cuda(rank), y.cuda(rank)
        loss = model(x, y)
        loss.backward()                          # all-reduce happens HERE,
        opt.step()                               # overlapped with backward
        opt.zero_grad()

dist.destroy_process_group()
```

Two non-obvious details worth knowing:

- **Gradient all-reduce overlaps with backward.** DDP registers autograd hooks and buckets gradients (default 25MB). As soon as a bucket's gradients are ready, NCCL all-reduce fires asynchronously while backward continues computing earlier layers. This is why DDP scales well — communication hides behind compute.
- **`set_epoch` matters.** Without it, every epoch sees the same shard ordering.

Since you've trained GPT-2 760M on the MI300X — check nanoGPT's `train.py`: it adds gradient accumulation on top, only syncing on the last micro-step via `model.require_backward_grad_sync = (micro_step == grad_accum_steps - 1)` to avoid wasteful all-reduces.

## Where your model breaks down: when the model doesn't fit

DDP requires the *full model + grads + optimizer state* on every GPU. AdamW costs ~16 bytes/param in mixed precision (2 weights + 2 grads + 4+4 optimizer moments + 4 master weights), so a 7B model needs ~112GB — dead on a 12GB 4070. That's where the other parallelism axes come in:

- **FSDP / ZeRO**: still data parallelism, but shards params/grads/optimizer state across GPUs, all-gathering layers just-in-time during forward/backward. Trades communication for memory.
- **Tensor parallelism**: splits individual matmuls across GPUs (e.g., attention heads split across devices). Needs fast interconnect (NVLink).
- **Pipeline parallelism**: splits layers across GPUs, micro-batches flow through stages.
- **Expert parallelism**: for MoE (relevant to your DeepSeek v4 interest) — different experts live on different GPUs, tokens get routed via all-to-all.

Frontier training (DeepSeek-V3 tech report is the best public reference) composes all of these: DP × PP × EP simultaneously.

So your summary is right for DDP specifically: same model everywhere, data split, synchronized updates — with the precision that synchronization happens at the *gradient* level via all-reduce, not by sharing the update itself.
