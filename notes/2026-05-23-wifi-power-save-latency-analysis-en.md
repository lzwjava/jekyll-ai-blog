---
audio: false
generated: true
image: false
lang: en
layout: post
title: WiFi Power Save Latency Analysis
translated: false
type: note
---

Here's the breakdown:

```
ANALYSIS: .52 and .29 OUTLIERS
==============================

192.168.1.52 — avg 0.6 ms
─────────────────────────
  ARP flag: "permanent" — this is YOUR AIR (lzw-mac.local)
  MAC: b2:e2:c6:39:f3:dd (locally administered = Apple private WiFi address)
  Why 0.6ms: pinging yourself = loopback, never leaves the NIC.
  Not special — it's just the local machine.

192.168.1.29 — avg 446.7 ms
───────────────────────────
  MAC: 86:c5:c7:ef:f6:5f (locally administered = randomized/private MAC)
  Likely: an Apple device (iPhone/iPad) using private WiFi address
  Per-ping breakdown:
    icmp_seq=0  324 ms
    icmp_seq=1  298 ms
    icmp_seq=2  196 ms
    icmp_seq=3  1045 ms  ← spike!
    icmp_seq=4  45 ms
    icmp_seq=5  849 ms
    icmp_seq=6  701 ms
    icmp_seq=7  860 ms
    icmp_seq=8  641 ms
    icmp_seq=9  693 ms
    stddev = 312 ms  ← enormous jitter

  WHY: This device is in WiFi power-save mode (802.11 PSM).
    - Radio sleeps to save battery
    - Wakes up periodically to check for buffered frames
    - Each ping has to wait for the next wake window
    - That's why latency ranges 45ms to 1045ms randomly
    - 0% packet loss = it IS reachable, just sleeping between checks

  Other slow devices:
    .14 (Xiaomi, 86ms) — phone in power-save, less aggressive
    .49 (Apple, 97ms) — Apple device, moderate power-save
```

The pattern: **battery-powered devices** (phones, tablets) use 802.11 power-save mode. They batch buffered frames and wake on a schedule. The more aggressive the power-save, the higher the ping latency. .29 is the worst offender — likely an iPhone/iPad with aggressive battery optimization. Wired devices (.36, .18) and always-on devices (.1 router) stay low.
