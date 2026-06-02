---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU Time Versus Network Latency
translated: false
type: note
---

Question: Does 54ms or 10ms represent an enormous amount of time from a CPU instruction execution perspective in the context of quantitative trading latency?

Answer:

## Yes — Absolutely Enormous. Here's the Scale

The gap between **network latency** and **CPU execution speed** is one of the most staggering mismatches in all of computing.

---

## The Numbers: A Scale Comparison

| Operation | Typical Time | Relative Scale |
|---|---|---|
| **CPU clock cycle** (modern 3–4 GHz) | ~0.3 nanoseconds | 1x (baseline) |
| **L1 cache hit** | ~1 nanosecond | ~3 cycles |
| **L2 cache hit** | ~5 nanoseconds | ~15 cycles |
| **L3 cache hit** | ~40 nanoseconds | ~120 cycles |
| **RAM access** | ~100 nanoseconds | ~300 cycles |
| **SSD read** | ~100 microseconds | ~300,000 cycles |
| **Network (local LAN)** | ~0.1 milliseconds | ~300,000 cycles |
| **Binance Tokyo (colocated)** | **~10 ms** | **~30,000,000 cycles** |
| **NY → Tokyo (no colocation)** | **~54 ms** | **~162,000,000 cycles** |

---

## What Can a CPU Do in 10ms?

At 3 GHz, in **10 milliseconds** a single CPU core executes approximately:

> **30,000,000 clock cycles**

In practical terms, a modern CPU can execute:

- A **simple instruction** (add, compare, branch) in 1 cycle
- A **complex algorithm** (sorting 1 million numbers) in a few milliseconds
- An **entire trading strategy calculation** — signal detection, risk check, order sizing — in **under 1 microsecond** on optimized code

So while your **network round-trip takes 10ms**, your **entire trading logic** might take **0.001ms (1 microsecond)**. The CPU is sitting idle waiting for the wire **99.99% of the time**.

---

## The Fundamental Insight: The Bottleneck is NOT the CPU

This is the core principle of modern HFT infrastructure:

```
Total latency = CPU processing time + Network transit time + Exchange processing time

~10ms total  =    ~0.001ms        +      ~8ms           +      ~2ms
```

The CPU is essentially **instant** relative to the network. This is why:

1. **Colocation** (saving 40–50ms of wire time) matters **far more** than buying a faster CPU
2. HFT firms obsess over **fiber routes**, **microwave towers**, and **laser links** between exchanges — shaving 1ms of wire time is worth millions
3. The famous **Spread Networks** project spent $300 million to lay a straighter fiber cable between Chicago and New York — just to save **3 milliseconds**

---

## The Memory Hierarchy Makes It Worse

Even **RAM access** at ~100ns is:

- 100x slower than L1 cache
- But still **100,000x faster** than a 10ms network hop

This is why HFT systems:

- Keep all critical data in **L1/L2 cache** (pre-loaded, never touching disk)
- Use **kernel bypass networking** (DPDK, RDMA) to cut OS overhead from ~50 microseconds to ~1 microsecond
- Use **FPGA hardware** to process market data in nanoseconds, bypassing the CPU entirely

---

## Practical Implication for Quant Trading

The 54ms vs 10ms difference (NY→Tokyo vs colocated Tokyo) represents:

> **~132,000,000 CPU cycles wasted per order round-trip**

A competitor colocated in Tokyo who is 44ms faster than you has already:

- Received the fill confirmation
- Updated their risk model
- Potentially sent a **second order** to hedge or follow up

...all **before your first order even reaches the exchange**.

This is why the industry saying is:

> *"Latency is not a software problem. It's a physics problem."*

The speed of light in fiber (~200,000 km/s) is a hard ceiling no amount of faster CPUs can overcome. **Geography beats processing power** — every time.
