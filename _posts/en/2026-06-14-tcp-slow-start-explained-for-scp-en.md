---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Slow Start Explained for scp
translated: false
type: note
---

**Question:** Why does `scp` start slow (~300 KB/s) then ramp up to full speed (~5 MB/s)?

**Answer:**

This is TCP slow start — a congestion control mechanism baked into the kernel.

## TCP Slow Start

TCP doesn't blast data at full speed immediately. It probes the network:

```
cwnd (congestion window) starts at ~10 segments (~14 KB)
Each ACK received → cwnd doubles (exponential growth)
Until cwnd hits ssthresh (slow start threshold) → switches to linear growth
```

Timeline for your transfer:
```
t=0s:   cwnd=14KB   → ~300 KB/s visible
t=0.5s: cwnd=112KB  → ~2 MB/s
t=1s:   cwnd=896KB  → ~5 MB/s (hits link capacity)
t=2s+:  steady state at ~6 MB/s (your LAN ceiling)
```

The "ramp" you see is literally the exponential doubling phase.

## Why LAN Still Has Slow Start

Even on `192.168.x.x`, TCP doesn't know it's on LAN until it probes. The kernel uses the same congestion control (cubic/bbr) regardless of interface.

```bash
# Check your CC algorithm on the workstation
sysctl net.ipv4.tcp_congestion_control
# probably: cubic
```

BBR ramps faster than CUBIC on low-latency links because it models bandwidth directly rather than waiting for loss.

## Why scp Specifically

`scp` uses SSH → TCP. The SSH layer adds ~cipher overhead per packet but doesn't change the TCP behavior. The slow start is purely kernel-level.

## Fix: Skip the Ramp

For large files on LAN, use `rsync` over SSH with bigger buffers, or just accept it — 27 MB at 5 MB/s is 4s, the ramp only costs ~1-2s.

```bash
# Or use netcat for raw speed (no encryption):
# sender:
nc -l 9999 < junhong.m4a
# receiver:
nc 192.168.x.x 9999 > junhong.m4a
```

Or tune SSH socket buffer:
```bash
scp -o "IPQoS=throughput" ~/Downloads/junhong.m4a lzw@192.168.x.x:~/
```

The ramp is physics — TCP is being polite to a network it doesn't know yet.
