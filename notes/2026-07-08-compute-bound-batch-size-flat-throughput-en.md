---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compute-Bound Batch Size Flat Throughput
translated: false
type: note
---

Question: I'm training a model at batch=48 on an H200 (135GB/144GB VRAM, GPU util 100%, MFU 66%). How should I think about choosing batch size, since bumping it up hasn't shortened wall-clock time much?

Answer:

Your intuition is right to be suspicious — and the GPU util reading (100%) already tells you why. You're **compute-bound, not launch-overhead-bound**. That changes what batch size can and can't do for you.

## The core identity

For a dense transformer, FLOPs per step scale linearly with batch:

```
FLOPs_per_step ≈ 6 * N * B * T
```

where `N` = params, `B` = batch, `T` = seq len (the standard 6ND approximation from Kaplan et al.). Your step_time is:

```
step_time ≈ FLOPs_per_step / (peak_FLOPs * MFU)
```

So `tokens/sec = B*T / step_time = peak_FLOPs * MFU / (6*N)` — **batch size cancels out**. Once you're compute-bound with util pinned at 100%, tok/sec is a function of your *hardware efficiency* (MFU), not your batch size. That's exactly why doubling batch just doubled step time and gave you roughly the same tok/sec — you verified this empirically already (136,700 tok/s at B=48).

Batch size only buys you wall-clock speed in the **overhead-bound regime**: when small batches leave the GPU idle between kernel launches, waiting on the dataloader, or paying fixed allreduce/sync latency in distributed training. In that regime, increasing B amortizes fixed cost over more useful work, and tok/sec climbs with B until you hit the compute-bound plateau — which you're already sitting on.

## What batch size actually controls (given you're compute-bound)

1. **Gradient noise, not throughput.** McCandlish et al.'s gradient noise scale framework measures the signal-to-noise ratio of gradients across training examples and predicts the largest efficient batch size for a task, and shows the noise scale increases as loss decreases over training and depends on model size mainly through model performance. Below the critical batch size (CBS), larger B reduces gradient variance and lets you take bigger, more reliable steps — same number of steps to converge, less noise per step. Above CBS, you're just burning compute for near-zero additional signal reduction (each extra example is nearly redundant with the ones already in the batch).

2. **A follow-up paper worth knowing about** found the noise-scale method itself is shaky in practice: a large batch size is necessary for fast training, but a batch size that is too large will harm token efficiency, and while McCandlish et al.'s gradient-noise-based CBS estimate has been used in practice (e.g. GPT-3), the assumptions behind it are strong and its reliability is unclear. Empirically, the gradient noise scale can underestimate the true critical batch size by several orders of magnitude, especially at larger model scale. Don't trust the noise-scale formula blindly — measure CBS empirically if you care about it.

3. **Total wall-clock time to a token budget** is roughly:

```
total_time ≈ total_tokens_needed / tokens_per_sec
```

Since `tokens_per_sec` is flat once compute-bound, your total training wall time for a fixed token budget is **basically fixed regardless of batch size** — the only lever left is raising MFU (better kernels, fewer recomputes, better overlap) or using less total compute (more efficient scaling / better data).

## Practically, for your run

Your MFU is 66% — solid but not maxed (H200 with good kernels + FA can often hit 50-60%+ for dense; for MoE with routing overhead 66% is actually quite good already). That's where your remaining wall-clock gains live, not batch size:

```python
# quick benchmark harness to find your actual overhead-bound -> compute-bound crossover
import time, torch

def bench(model, optimizer, batch_sizes, seq_len, steps=5):
    results = {}
    for B in batch_sizes:
        x = torch.randint(0, 32000, (B, seq_len), device="cuda")
        y = torch.randint(0, 32000, (B, seq_len), device="cuda")
        torch.cuda.synchronize()
        t0 = time.time()
        for _ in range(steps):
            optimizer.zero_grad(set_to_none=True)
            loss = model(x, labels=y).loss
            loss.backward()
            optimizer.step()
        torch.cuda.synchronize()
        dt = (time.time() - t0) / steps
        toks_per_sec = B * seq_len / dt
        results[B] = toks_per_sec
        print(f"B={B:4d}  step_time={dt*1000:7.1f}ms  tok/s={toks_per_sec:,.0f}")
    return results

# sweep and look for where tok/s stops increasing — that's your compute-bound floor
bench(model, optimizer, batch_sizes=[8, 16, 24, 32, 48, 64], seq_len=2048)
```

If tok/s is already flat by B=24-32 in that sweep, you've confirmed B=48 is pure gradient-quality choice, not throughput choice — and you could actually drop to a smaller B (freeing VRAM for longer context or bigger MoE expert capacity) with no wall-clock cost, as long as you stay above your empirical CBS.

## MoE-specific wrinkle (relevant to your DeepSeek v4 work)

For MoE, batch size also determines **tokens-per-expert per step**. With `E` experts and top-`k` routing, expected tokens routed to a given expert per step is roughly `B*T*k/E`. Too small a batch → high variance in expert load → some experts starved, capacity-factor drops kick in, dropped tokens hurt quality independent of the noise-scale argument above. This is a second, MoE-specific reason to keep batch above some floor, separate from the gradient-noise argument — worth checking your router's dropped-token rate at different B, not just tok/s.

## Bottom line

- Batch size stopped helping wall-clock because you're compute-bound (100% util) — that's expected and correct, not a bug.
- Tune batch size for **gradient noise / MoE load balance**, not throughput.
- Chase wall-clock gains through **MFU** (kernel fusion, FA3/FA2 tuning, activation checkpointing trade-offs, sequence packing) instead — that's the only lever left once util is pinned.

References:

- [An Empirical Model of Large-Batch Training (McCandlish et al., 2018)](https://arxiv.org/abs/1812.06162)
- [Critical Batch Size Revisited (2025)](https://arxiv.org/abs/2505.23971)
