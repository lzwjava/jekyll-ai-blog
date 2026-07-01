---
audio: false
generated: true
image: false
lang: en
layout: post
title: 5G NSA Latency and Jitter Issues
translated: false
type: note
---

**Question:** Why does 5G have worse latency and much higher jitter compared to 4G despite faster throughput? Is this common or specific to my case?**Answer:**

Your results are **completely normal and well-documented**. Here's the technical breakdown of why:

---

## Root Cause: You're Almost Certainly on 5G NSA (Non-Standalone)

This is the key. There are two 5G architectures:

| | **NSA (Non-Standalone)** | **SA (Standalone)** |
| --- | --- | --- |
| Radio | 5G NR | 5G NR |
| Core network | 4G LTE EPC | True 5G core |
| Control plane | Routed through 4G | Native 5G |
| Latency | Worse than 4G | <10ms (theoretical) |
| Deployment | ~95% of current 5G | Rare, expensive |

In NSA, the initial call/session is still set up with the 4G network. New 5G radios capture the 5G spectrum, but packets still route back to the 4G core — so customers won't experience the full 5G package with ultra-low latency.

In NSA deployments, control plane signaling lives in the LTE Evolved Packet Core (EPC), while user plane data is transmitted over 5G. This hybrid operation introduces additional signaling steps and interfaces between LTE and 5G, which **increase end-to-end latency and jitter**, particularly for uplink communication.

---

## Why Jitter is So Much Worse (±3.6ms → ±44ms)

Three compounding reasons:

**1. Radio physics** — 5G sub-6GHz and mmWave signals are shorter range and more sensitive to obstruction. Your hotspot is mobile, so signal fluctuates constantly → variable radio retransmissions → jitter spikes.

**2. Dual-stack handoffs** — NSA devices can hop between 4G anchor and 5G NR mid-session. Each handoff adds variable delay.

**3. Scheduler behavior** — 5G performance varies by signal quality and tower load; latency/jitter can spike at peak hours. Signal quality, tower load, and interference can push latency higher and make jitter spiky — two users on the same plan in different locations can see very different results.

---

## Is This Common?

**Yes, extremely common.** Ultra-low latency, a hallmark of 5G, isn't enabled by NSA networks. And NSA is what most people actually have. The marketing claims of "sub-10ms 5G latency" refer to SA networks which are incredibly rare around the world — only a handful of telecom companies have deployed this infrastructure, as it's prohibitively expensive.

Real-world forum users confirm this too — people explicitly lock their hotspot routers to LTE-only because 5G NSA makes both speed and latency poor.

---

## Your Specific Numbers in Context

| Metric | Your 4G | Your 5G | Typical 4G | Typical 5G NSA |
| --- | --- | --- | --- | --- |
| Download | 11.6 Mbps | 21.3 Mbps | 10–30 Mbps | 20–100 Mbps |
| Latency | 89ms | 136ms | 30–80ms | 50–150ms |
| Jitter | ±3.6ms | ±44ms | ±10–30ms | ±20–80ms |

Your 4G latency is slightly high (89ms vs typical 30–50ms) — that's likely the double NAT + CGNAT overhead adding ~40ms on top of the radio latency. But the jitter is **excellent** at ±3.6ms.

---

## Practical Recommendation for Your Use Case

Given you're SSH-ing into `192.168.x.x` (workstation) and AMD cloud:

- **SSH / interactive work** → stick to 4G. Jitter ±3.6ms means keystrokes feel instant.
- **Pulling large model checkpoints / uploading datasets** → switch to 5G for the 2x throughput.
- You could even script a hotspot toggle based on task type if your carrier's APN supports it.

References:

- [5G NSA vs SA — Informa TechTarget](https://www.techtarget.com/searchnetworking/feature/5G-NSA-vs-SA-How-does-each-deployment-mode-differ)
- [Performance Benchmarking of 5G SA and NSA Networks — MDPI](https://www.mdpi.com/2224-2708/15/1/18)
- [5G Home Internet vs Cable: Latency, Jitter, and Real-World Tests](https://theispinfo.com/5g-home-internet-vs-cable-latency-jitter-and-real-world-tests/)
