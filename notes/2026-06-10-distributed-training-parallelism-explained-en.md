---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed Training Parallelism Explained
translated: false
type: note
---

**Question:** How does distributed training work under the hood, and would it actually help the nanochat 760M run on MI300X?

**Answer:**

## Start with what one training step actually is

Every training step is the same three phases regardless of how many GPUs you have:

```python
loss = model(x, y)        # forward:  activations
loss.backward()           # backward: gradients
optimizer.step()          # update:   weights -= f(grad)
```

Distributed training is just the answer to one question: **which of these three phases do you split, and across what dimension?** There are exactly three dimensions to split along — the batch, the weights, and the layers — giving the three parallelism families.

---

## 1. Data Parallelism (DP/DDP) — split the batch

Every GPU holds a **complete replica** of the model. You split the batch.

The key insight is mathematical: the gradient of a mean loss over a batch is the mean of per-example gradients:

```
∇L(batch) = (1/B) Σᵢ ∇L(xᵢ)
          = (1/N) Σₖ [ (1/(B/N)) Σᵢ∈GPUₖ ∇L(xᵢ) ]
            ─────   ──────────────────────────────
            average      local gradient on GPU k
```

So each GPU computes gradients on its shard, then you **average gradients across GPUs** — and every replica takes the identical optimizer step. The replicas stay bit-identical forever (same init via broadcast at step 0, same averaged gradient every step).

Minimal implementation, no framework magic:

```python
import torch, torch.distributed as dist

dist.init_process_group("nccl")  # RCCL on ROCm, same API
rank, world = dist.get_rank(), dist.get_world_size()
torch.cuda.set_device(rank)

model = GPT(config).cuda()
# step 0: make all replicas identical
for p in model.parameters():
    dist.broadcast(p.data, src=0)

for step in range(num_steps):
    x, y = get_batch(rank)            # each rank gets DIFFERENT data
    loss = model(x, y)
    loss.backward()
    for p in model.parameters():      # average grads across ranks
        dist.all_reduce(p.grad, op=dist.ReduceOp.AVG)
    optimizer.step()
    optimizer.zero_grad()
```

That's all DDP fundamentally is. `torch.nn.parallel.DistributedDataParallel` adds two optimizations on top:

**a) Bucketing + overlap.** Instead of one AllReduce per tensor at the end, DDP registers autograd hooks. As soon as a gradient is ready during `backward()`, it goes into a ~25MB bucket; full buckets AllReduce **asynchronously while backward is still computing earlier layers**. Since backward runs last-layer-first, communication of layer 24's grads overlaps with computation of layer 1's. On a transformer, this hides most of the comm cost.

**b) `no_sync()` for gradient accumulation.** You only AllReduce on the last micro-batch:

```python
for i in range(grad_accum_steps):
    ctx = model.no_sync() if i < grad_accum_steps - 1 else nullcontext()
    with ctx:
        loss = model(x_i, y_i) / grad_accum_steps
        loss.backward()
optimizer.step()
```

nanochat already does exactly this — look at `base_train.py`, it reads `RANK`/`WORLD_SIZE` from torchrun and divides `total_batch_size` by world size.

### What AllReduce actually costs

Ring AllReduce moves `2 × (N-1)/N × bytes` per GPU regardless of GPU count — for your 760M trainable matrices in bf16, that's roughly **~1.5 GB per step** over the interconnect. On MI300X nodes with Infinity Fabric (~hundreds of GB/s), this is tens of milliseconds — and it's overlapped with backward anyway. DP scales almost linearly for models this size.

---

## 2. Tensor Parallelism — split the weights

Each matmul is sharded. For `Y = XW` with `W [1536, 6144]` split column-wise across 4 GPUs, each GPU computes `X @ W[:, shard]` and you concatenate. Megatron-style TP does column-split on the up-projection, row-split on the down-projection, so you need only **one AllReduce per MLP and one per attention block** — but that's per *layer*, per *forward and backward*, on the critical path. It can't be hidden like DDP comm.

You use TP when **one layer's weights/activations don't fit** or when you need to scale batch=1 latency. A 760M model on a 192 GB GPU is ~2 orders of magnitude away from needing this.

## 3. Pipeline Parallelism — split the layers

GPU 0 holds layers 0–11, GPU 1 holds 12–23. Activations flow forward, gradients flow back. Naive PP leaves GPUs idle (the "bubble"); GPipe/1F1B scheduling shrinks the bubble to `(stages-1)/(microbatches+stages-1)`. Only relevant when the model doesn't fit even with ZeRO. Not your problem.

## 4. ZeRO/FSDP — DP without the memory redundancy

Plain DDP wastes memory: N copies of weights + grads + optimizer state. For 760M with your Muon/Adam mix that's maybe ~10 GB of state replicated per GPU. ZeRO-1/2/3 shards optimizer state → grads → params, reconstructing via AllGather on the fly. The trade: more communication for less memory. You're at 105/192 GB on a single GPU — **memory is not your constraint**, so ZeRO buys you nothing here.

---

## Now apply it to your run

Your numbers from the summary: 1× MI300X, 7.7 s/step, 8 grad-accum micro-batches per step, 27.5% MFU, 29K steps ≈ 62 hours. Two separate inefficiencies, and it matters which you attack first:

**Inefficiency 1: per-FLOP efficiency (MFU=27%).** This is a *kernel* problem — SDPA math fallback instead of fused flash attention, plus full `L` attention instead of `SSSL` sliding window. **DP does not fix this.** Four GPUs at 27% MFU is four GPUs each wasting 73% of their compute. You'd pay 4× $/hr for 4× of a bad baseline.

**Inefficiency 2: wall-clock serialization.** Your 8 grad-accum micro-batches run sequentially. This is exactly what DP parallelizes — with 8 GPUs, grad accum drops to 1 and the 8 micro-batches run simultaneously on different devices:

```
1 GPU:  step = 8 × (fwd+bwd) + opt           ≈ 7.7 s
8 GPUs: step = 1 × (fwd+bwd) + allreduce + opt ≈ 1.1–1.3 s
```

Same `total_batch_size=524288`, same loss curve, ~6–7× wall-clock speedup (comm + per-micro-batch fixed overheads eat a bit). The command is trivial because nanochat is already DDP-ready:

```bash
torchrun --standalone --nproc_per_node=8 -m scripts.base_train \
  --depth=24 --window-pattern=L --total-batch-size=524288
```

Nothing else changes — hyperparameters, LR, token budget all stay identical because the *effective batch* is unchanged. That's the beauty of DP done right: it's mathematically invisible to the optimization.

### The decision table

| Config | MFU | Wall clock | $ @ ~$2/hr/GPU |
|---|---|---|---|
| 1× MI300X, SDPA (now) | 27% | ~62 h | ~$124 |
| 1× + ROCm flash-attn, SSSL | ~45–50% | ~33 h | ~$66 |
| 8× MI300X, SDPA | 27% | ~10 h | ~$160 |
| 8× + flash-attn | ~45% | ~5–6 h | ~$90 |

So: **distributed training would absolutely help your wall-clock time, near-linearly, with a one-line command change** — nanochat's DDP path is already wired. But it doesn't touch your cost-efficiency problem, which is the SDPA kernel. Order of operations:

1. **First try ROCm flash-attn** (`pip install flash-attn --no-build-isolation` on the droplet; AMD maintains a ROCm fork at `ROCm/flash-attention` if upstream fails to build for gfx942). This halves both time *and* cost.
2. **Then** add GPUs if you want it done in hours instead of days — and only then, because every extra GPU multiplies whatever per-GPU efficiency you've locked in.

One caveat worth knowing for when you scale further: at very large world sizes, DP forces either huge global batches (which eventually hurt convergence — see the critical batch size idea in McCandlish et al., "An Empirical Model of Large-Batch Training") or tiny per-GPU batches (which tank MFU). That's the point where TP/PP/ZeRO stop being academic. At 760M and ≤8 GPUs, you're nowhere near it — pure DP is the correct and complete answer.

**References:**

- [PyTorch DDP design notes (bucketing, overlap)](https://pytorch.org/docs/stable/notes/ddp.html)
- [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054)
- [Megatron-LM: tensor parallelism](https://arxiv.org/abs/1909.08053)
- [ROCm flash-attention fork](https://github.com/ROCm/flash-attention)
- [An Empirical Model of Large-Batch Training](https://arxiv.org/abs/1812.06162)
