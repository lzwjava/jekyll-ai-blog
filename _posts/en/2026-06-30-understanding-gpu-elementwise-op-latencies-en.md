---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding GPU Elementwise Op Latencies
translated: false
type: note
---

Question: Explain these elementwise/op latency numbers for a 1024×1024 FP16 tensor, and confirm the unit (is μs = 1×10⁻⁹ s?).

Answer:

First, the unit. No — μs is **microsecond = 1×10⁻⁶ s**. 1×10⁻⁹ s is a **nanosecond (ns)**. So:

```
1 s   = 1000 ms
1 ms  = 1000 μs   (10^-3 s)
1 μs  = 1000 ns   (10^-6 s)
1 ns  = 1000 ps   (10^-9 s)
```

Your ~4–7 μs ≈ 4000–7000 ns per op.

## What these numbers actually measure

A 1024×1024 FP16 tensor = 1M elements × 2 bytes = **2 MB**. The key insight: most of these ops are **memory-bandwidth-bound, not compute-bound**. The GPU isn't busy doing math — it's busy moving 2 MB in and out of HBM.

### Roofline check — why ~4 μs for add/mul/relu

An elementwise op like `add` does:

- Read 2 MB (input A) + 2 MB (input B) = 4 MB
- Write 2 MB (output)
- Total traffic ≈ 6 MB
- FLOPs = 1M (one add per element) → trivial

On an RTX 4070 (~480 GB/s) or MI300X (~5.3 TB/s), the floor is `bytes / bandwidth`:

```python
bytes_moved = 6e6          # 6 MB for a+b -> c
bw_4070     = 480e9        # B/s
bw_mi300x   = 5.3e12

print(bytes_moved / bw_4070  * 1e6, "μs")  # ~12.5 μs (theoretical floor)
print(bytes_moved / bw_mi300x * 1e6, "μs")  # ~1.1 μs
```

Your ~4 μs implies a high-bandwidth GPU (MI300X-class, or a fused kernel reading less). The point: **arithmetic intensity is ~0.17 FLOP/byte** — wildly memory-bound. A modern GPU does ~100+ FLOP/byte at the compute roofline, so you're using <1% of the ALUs. The op finishes the instant the bytes arrive.

### Why softmax (~7 μs) and layer_norm (~6 μs) cost more

These are **reductions** — they can't be done in a single streaming pass as naively as `add`:

- **softmax**: needs `max` over the row (numerical stability), then `exp`, then `sum`, then divide. That's logically 3 passes over the data (max, sum, normalize), though good kernels fuse it into ~2 reads. More traffic + sync = higher latency.
- **layer_norm**: needs mean and variance (two reductions) before normalizing. Again multi-pass.

```python
# softmax forward, the "safe" 3-pass logic fused kernels collapse
def softmax(x):           # x: [N, D], reduce over D
    m = x.max(-1, keepdim=True).values      # pass 1: max
    e = (x - m).exp()                        # pass 2: exp
    return e / e.sum(-1, keepdim=True)       # pass 3: sum + div
```

The extra ~50–75% latency vs `add` comes from the extra reads and the cross-lane reduction (warp shuffles + shared memory), not from `exp` being expensive.

### Why matmul is *only* ~6 μs — the surprise

Naively a 1024³ matmul is **2·N³ = 2.1 GFLOP**, vs 1M FLOP for `add` — 2000× more compute. Yet it's the same ballpark latency. Why?

Because matmul is the one op here that's **compute-bound and the hardware is built for it**:

```python
flops = 2 * 1024**3        # 2.1e9
# MI300X FP16 ~1300 TFLOP/s (with sparsity/tensor cores)
print(flops / 1.3e15 * 1e6, "μs")   # ~1.6 μs compute floor
```

Tensor cores (NVIDIA) / Matrix cores (CDNA on MI300X) chew through the MACs in ~1–2 μs; the rest is launch overhead and tiling. Arithmetic intensity for a square matmul is `N/3 ≈ 341 FLOP/byte` — firmly past the compute roofline, so the ALUs are actually the bottleneck (the good case).

## The mental model to keep

```
                 arithmetic       bottleneck        why latency ~equal
                 intensity
add/mul/relu     ~0.17 FLOP/B     memory bandwidth  2 MB in/out dominates
softmax          ~0.2  FLOP/B     memory + reduction  extra passes/syncs
layer_norm       ~0.2  FLOP/B     memory + reduction  mean+var passes
matmul           ~341  FLOP/B     compute (tensor cores)  N³ FLOPs but HW eats them
```

At these tiny sizes, a large fraction of every number is also **fixed kernel-launch overhead** (~2–5 μs on the host→device path). That's why nothing dips below ~4 μs no matter how trivial — you're hitting the launch floor, which is exactly why **kernel fusion** (FlashAttention fusing softmax+matmul, fused LayerNorm) matters so much: it amortizes that fixed cost and avoids round-tripping the 2 MB to HBM between ops.

## Verify it yourself

```python
import torch, torch.nn.functional as F
x = torch.randn(1024, 1024, dtype=torch.float16, device='cuda')

def bench(fn, iters=1000):
    fn()  # warmup + compile JIT
    torch.cuda.synchronize()
    start = torch.cuda.Event(True); end = torch.cuda.Event(True)
    start.record()
    for _ in range(iters): fn()
    end.record(); torch.cuda.synchronize()
    return start.elapsed_time(end) / iters * 1e3  # μs

print("add    ", bench(lambda: x + x))
print("relu   ", bench(lambda: F.relu(x)))
print("softmax", bench(lambda: F.softmax(x, -1)))
print("ln     ", bench(lambda: F.layer_norm(x, (1024,))))
print("matmul ", bench(lambda: x @ x))
```

Run that on your RTX 4070 and the MI300X — you'll see the elementwise ops scale almost purely with bandwidth ratio (~11×), while matmul scales with FP16 tensor throughput. That contrast *is* the roofline, measured.
