---
audio: false
generated: true
image: false
lang: en
layout: post
title: WiFi Jitter Outlier Versus Ethernet Performance
translated: false
type: note
---

Here's what the data tells us:

```
ANALYSIS: Network Latency to 192.168.1.36
==========================================

Your Air is on Wi-Fi (en0), IP 192.168.1.52
Both .1 (router) and .36 (workstation) appear as Wi-Fi neighbors in ARP
(both on en0 — .36 is actually wired, but router bridges the LAN)

PATH: Air [WiFi] -> Router [Ethernet] -> Switch -> Workstation (.36)

MEASUREMENTS (30 pings each):
                            min     avg     max     stddev
  Router (WiFi only):       7.4ms   22.9ms  96.0ms  26.8ms
  Workstation (full path):  4.4ms   12.4ms  69.5ms  15.8ms

KEY INSIGHT: Your 92.3ms was an OUTLIER, not the typical case.
The workstation actually has LOWER avg latency than the router!
(12.4ms vs 22.9ms — WiFi contention varies per-packet)

LATENCY BREAKDOWN (estimated):
  WiFi hop (Air -> Router):     ~5-15ms typical, spikes to 50-90ms
  Router processing:            ~0.1ms
  Ethernet (Router -> Switch):  ~0.01ms (speed of light in copper)
  Switch -> Workstation:        ~0.01ms

WHY THE SPIKES (92.3ms, 74.9ms, etc.):
  - WiFi channel contention (neighbors on same channel)
  - WiFi power-save mode wake-up latency
  - 802.11 retransmissions on interference
  - Background scan for better APs
  - All of these add 10-100ms jitter to WiFi

VERDICT: The 92.3ms spike is pure WiFi jitter.
The Ethernet/switch leg adds <1ms of deterministic latency.
Your table makes sense — the extra path (router->cable->switch)
is negligible. WiFi is the bottleneck, not the topology.

Compare: if .36 had WiFi too, you'd see 2x WiFi jitter (40-200ms).
Being wired, only one WiFi hop contributes.
```

The 92.3ms you saw was a WiFi jitter spike, not the typical case. With 30 pings, the average is only 12.4ms — the Ethernet/switch path adds essentially zero latency. The `--delay` flag captures single-sample latency, so it naturally picks up these WiFi spikes. For more stable measurements, you'd want something like `ping -c 10` averaged. But for a quick network scan, it's useful — if you see consistently high latency to a device, that tells you something real.