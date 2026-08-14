---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU OOM from constant folding
translated: false
type: note
---

The traceback is fully explained by the source. Here's the chain of events:

## What's actually failing

The OOM at `aten.scalar_tensor(0, dtype=torch.int64, device=cuda:0)` is **not** because that op is large — it's an 8-byte 0-dim tensor. It's the *first allocation to fail* because the GPU is completely full. And the allocation happens inside Inductor's **joint-graph constant folding**, which executes ops on the real CUDA device during compilation.

## Source trace

**1. `model.py:196`** — `F.cross_entropy(..., ignore_index=-1)` is the origin. Under `torch.compile`, this is decomposed via `torch/_decomp/decompositions.py` in `_nll_loss_forward` (line ~4760):

```python
safe_target = torch.where(target != ignore_index, target, 0)
result = torch.where(target != ignore_index, result, 0)
```

Since `targets` is int64 on CUDA, the literal `0` is traced as `aten.scalar_tensor(0, dtype=torch.int64, device=cuda:0)` — exactly the node in the error (the `target != ignore_index` comparison also creates one for `-1`).

**2. `joint_graph.py:410`** — `constant_fold_uniform_value()` runs as a joint-graph pass during Inductor compilation (gated by `torch._inductor.config.joint_graph_constant_folding = True`, `config.py:900`). It's purely an optimization: find nodes whose output is a uniform constant and rewrite them to `aten.full(shape, value)` so Inductor emits a cheap fill instead of a kernel.

**3. `joint_graph.py:385` / `constant_folding.py:251`** — the `UniformValueConstantFolder._deduce_value` determines constness by *actually running the op* on the recorded device:

```python
# pointwise ops
if isinstance(node.target, torch._ops.OpOverload) and (
    torch.Tag.pointwise in node.target.tags
    or node.target is torch.ops.aten.scalar_tensor.default
):
    args, kwargs = self.fetch_args_kwargs_from_env(node)
    ...
    return node.target(*args, **kwargs)   # <-- real CUDA allocation at compile time
```

No faketensor, no CPU offload, no OOM `try/except` around this call — it only bails out on `SymInt` inputs and strips `memory_format`.

**4. The OOM itself** — during training, compile happens while the GPU is already saturated (weights + Adam state + current batch's activations/gradients). The caching allocator can't satisfy even an 8-byte `scalar_tensor` allocation (`cudaMalloc` fails), so it raises `AcceleratorError: CUDA error: out of memory`, which Inductor surfaces as `BackendCompilerFailed`.

## Why the pass "has issues"

- It performs **real on-device allocations at compile time**, on top of an already-full GPU. This is fine at inference/compile time with memory headroom, but during training it's an extra spike that can trip OOM even though the folded tensors are tiny.
- The only guard it has is the SymInt check — nothing protects against a saturated allocator, and `scalar_tensor(0)` doesn't even need device execution to know its value (it's constant by construction).

## Fixes

- **Targeted:** disable the pass — it's only an optimization:

  ```python
  torch._inductor.config.joint_graph_constant_folding = False
  ```

  Correctness is unaffected; you lose uniform-constant folding and the `+0`/`*1` no-op removal.
- **Real fix:** your GPU has *zero* headroom. Reduce batch size / sequence length or use gradient checkpointing — the compile-time spike will keep failing otherwise.
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` helps with fragmentation but not when memory is genuinely exhausted.

If this is a repro for a bug report, the interesting bug is: constant folding executes ops on-device at compile time with no memory-pressure fallback, so an OOM during training surfaces as a spurious `BackendCompilerFailed` at a trivial `scalar_tensor` node.
