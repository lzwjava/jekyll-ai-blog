---
audio: false
generated: true
image: false
lang: en
layout: post
title: Introduction to TCP Congestion Control
translated: false
type: note
---

Question: What is an introduction to TCP congestion control algorithms?

Answer:

## Overview

TCP congestion control is the mechanism by which TCP senders regulate the rate at which they inject data into the network, preventing congestion collapse. The core idea: the sender maintains a **congestion window (cwnd)** that limits how many unacknowledged bytes can be in flight at once.

```
Flight size = min(cwnd, receiver's advertised window)
```

---

## Core Concepts

### AIMD — The Fundamental Principle
All classic algorithms follow **Additive Increase, Multiplicative Decrease**:
- **Increase**: grow cwnd slowly (additive) during normal operation
- **Decrease**: shrink cwnd sharply (multiplicative) on congestion signal

### Congestion Signals

| Signal | What it means |
|--------|--------------|
| Triple duplicate ACK | Packet lost, but network still delivering ACKs |
| Timeout (RTO) | Severe congestion or route failure |

---

## Phase Machines

### 1. Slow Start
- Start with cwnd = 1 MSS (or ~10 MSS in modern stacks)
- **Double cwnd each RTT** (exponential growth)
- Stop when cwnd reaches `ssthresh` (slow-start threshold)

```
Each ACK → cwnd += 1 MSS
```

### 2. Congestion Avoidance
- cwnd grows **linearly** (one MSS per RTT)
- Probes for available bandwidth without flooding

```
Each ACK → cwnd += MSS × (MSS / cwnd)
```

### 3. Fast Retransmit
- On **3 duplicate ACKs**: retransmit the missing segment immediately — don't wait for RTO

### 4. Fast Recovery
- After fast retransmit: stay in a "reduced but not collapsed" state
- Avoids going back to Slow Start for non-severe losses

---

## Key Algorithm Timeline

### TCP Tahoe (1988)
The original. On **any** loss event (timeout or 3 dup-ACK):
```
ssthresh = cwnd / 2
cwnd = 1 MSS        ← always resets to Slow Start
```

### TCP Reno (1990)
Distinguishes loss types. On **3 dup-ACKs**:
```
ssthresh = cwnd / 2
cwnd = ssthresh     ← Fast Recovery instead of Slow Start
```
On **timeout** → same as Tahoe (reset to 1 MSS).

### TCP NewReno (RFC 6582)
Fixes Reno's weakness when **multiple packets are lost** in one window:
- Stays in Fast Recovery until all lost segments are recovered (tracks "partial ACKs")

### TCP SACK (Selective ACKs)
Not an algorithm per se, but a critical extension — receivers report exactly which bytes arrived, allowing senders to retransmit only the gaps.

### TCP CUBIC (RFC 9438) — Default in Linux since 2.6.19
Uses a **cubic function** of time since last congestion event for window growth, independent of RTT:
```
W(t) = C(t − K)³ + Wmax
```
- Grows fast when far from previous max, cautiously near it
- Friendly to long-fat networks (high bandwidth × delay)
- Default in Linux, macOS, Android

### BBR (Bottleneck Bandwidth and RTT) — Google, 2016
Fundamentally different: **model-based, not loss-based**.
- Continuously estimates **bottleneck bandwidth (BtlBw)** and **min RTT**
- Targets the optimal operating point: fill the pipe without bloating buffers
- Ignores packet loss as the primary signal (loss ≠ congestion in lossy WiFi)
- Used by Google, YouTube, QUIC; BBRv3 is the current iteration

```
pacing_rate = BtlBw × pacing_gain
cwnd        = BtlBw × RTprop × cwnd_gain
```

---

## Comparison at a Glance

| Algorithm | Loss Signal | Growth | RTT-Fair | Notes |
|-----------|-------------|--------|----------|-------|
| Tahoe | Timeout + dup-ACK | Slow Start after any loss | Yes | Historical baseline |
| Reno | Distinguishes events | Fast Recovery on dup-ACK | Yes | Simple, widely studied |
| NewReno | Same as Reno | Better multi-loss recovery | Yes | RFC 6582 |
| CUBIC | Dup-ACK / Timeout | Cubic in time | Better | Linux default |
| BBR | BW + RTT model | Pacing-based | Partial | YouTube/GCP scale |

---

## State Diagram (Reno/CUBIC)

```
             ┌─────────────────────────────────────────┐
             │              SLOW START                  │
             │  cwnd doubles each RTT                   │
             └──────────────┬──────────────────────────┘
                            │ cwnd ≥ ssthresh
                            ▼
             ┌─────────────────────────────────────────┐
             │          CONGESTION AVOIDANCE            │
             │  cwnd += 1 MSS per RTT                   │
             └──────────┬──────────────┬───────────────┘
                        │ 3 dup-ACKs   │ Timeout
                        ▼              ▼
             ┌──────────────┐   ssthresh = cwnd/2
             │ FAST RECOVERY│   cwnd = 1 MSS
             │ ssthresh=cwnd/2   → back to SLOW START
             │ cwnd=ssthresh│
             └──────────────┘
```

---

## What's Next (Modern Directions)

- **QUIC** (HTTP/3) — implements its own congestion control at the application layer, defaults to CUBIC or BBR
- **Copa / PCC Vivace** — delay-gradient algorithms for latency-sensitive workloads
- **Swift** — Google datacenter variant optimized for μs-scale RTTs
- **ML-based CC** — Aurora, Orca use reinforcement learning to tune CC online

References:
- [RFC 5681 – TCP Congestion Control](https://datatracker.ietf.org/doc/html/rfc5681)
- [RFC 9438 – CUBIC for Fast Long-Distance Networks](https://datatracker.ietf.org/doc/html/rfc9438)
- [RFC 6582 – The NewReno Modification to TCP's Fast Recovery](https://datatracker.ietf.org/doc/html/rfc6582)
- [BBR: Congestion-Based Congestion Control (ACM Queue, 2016)](https://queue.acm.org/detail.cfm?id=3022184)
- [Computer Networks: A Systems Approach – Peterson & Davie, Chapter 6](https://book.systemsapproach.org/congestion/tcpcc.html)
