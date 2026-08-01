---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Tensor Parallelism: Five Linear Classes"
translated: false
type: note
---

There are 5 linear classes, and they all exist for one reason: **Tensor Parallelism** — splitting one big matmul across multiple GPUs. The only things that differ between them are:

1. **which weight dimension gets sharded** (rows or columns)
2. **how a full checkpoint weight is loaded/resharded into each GPU's local slice** (`weight_loader`)
3. **whether the forward pass needs a `dist.all_reduce`** to combine partial results

Here's the breakdown:

---

## `LinearBase` — the shared scaffold

Holds `weight` (+ optional `bias`), records `tp_rank`/`tp_size`, and attaches a `weight_loader` hook to each parameter. It does **no real math** — `forward` raises `NotImplementedError`. Everything else inherits from it.

## `ReplicatedLinear` — no sharding

The simplest case: every GPU has the **full** weight. `weight_loader` just copies the whole checkpoint tensor; `forward` is a plain `F.linear`. Used for things like embeddings/output heads or small projections that aren't worth splitting.

## `ColumnParallelLinear` — column-parallel

Splits the **output** dimension: each GPU holds `output_size / tp_size` columns, so `weight` is `[out/tp, in]`.

- `weight_loader`: slices out `rank * shard_size : (rank+1) * shard_size` of the output dim from the full checkpoint weight.
- `forward`: no communication needed — each GPU computes its own columns and they're concatenated later.

## `MergedColumnParallelLinear` — two column-parallels fused

A "fused" column-parallel used for **gate_up_proj** in the MLP: one weight matrix containing two logical projections (`gate` + `up`, each of size `intermediate_size`) that get sharded *and* merged into a single local tensor.

- `weight_loader(param, loaded_weight, loaded_shard_id)` takes an extra `loaded_shard_id` (0 or 1) so it knows which half of the merged local weight this checkpoint slice belongs to, and where the TP shard offset lands inside it.

## `QKVParallelLinear` — the special fused one

Column-parallel but for **Q/K/V with GQA head-sharding**. The local output is `(q_heads + 2*kv_heads) * head_dim` — note: **Q heads are split across GPUs, but KV heads are replicated** when `total_num_kv_heads < total_num_heads` (GQA). This only works because `total_num_kv_heads` is required to divide evenly by `tp_size`.

- `weight_loader(param, loaded_weight, loaded_shard_id)` with `loaded_shard_id ∈ {"q", "k", "v"}`: Q, K, V checkpoint slices each map to different offsets inside the single merged local weight.
- It's also a plain column-parallel in the forward sense — no all-reduce.

## `RowParallelLinear` — row-parallel

Splits the **input** dimension: each GPU holds `[out, in/tp]` and computes a partial output.

- `weight_loader`: slices the *input* dim (dim 1).
- `forward`: **this is the one that needs `dist.all_reduce(y)`** to sum the partial products from all ranks. Also, bias is only added on `tp_rank == 0` (and the all-reduce then sums it correctly).

---

## How they fit together in the model

In `nanovllm/models/qwen3.py`, the pattern is the standard Megatron-style TP setup:

| Model component | Class | Why |
| --- | --- | --- |
| `qkv_proj` | `QKVParallelLinear` | one fused Q/K/V matmul, heads split across GPUs |
| `o_proj` | `RowParallelLinear` | attention output must be summed across GPUs → row-parallel + all-reduce |
| `gate_up_proj` | `MergedColumnParallelLinear` | fused gate+up matmul, column-parallel |
| `down_proj` | `RowParallelLinear` | MLP output, row-parallel + all-reduce |

So the pair `ColumnParallel` (no comm) → `RowParallel` (all-reduce) is the canonical Megatron-LM `f`/`g` pairing: column-parallel produces shards, row-parallel consumes them, and each row-parallel layer does one all-reduce, which gives communication-efficient TP for free. `ReplicatedLinear` is the escape hatch for layers you don't want to shard.

If you want to see the whole thing in action, run `python3.12 experiments/04_scheduler_watch.py` — though note the TP code paths only activate when `tp_size > 1`; on a single GPU every rank is rank 0 and the all-reduces become no-ops.
