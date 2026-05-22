---
audio: false
generated: true
image: false
lang: en
layout: post
title: Step-by-Step Network Diagnosis Commands
translated: false
type: note
---

Here's the command-by-command breakdown of how I diagnosed it:

```
STEP-BY-STEP NETWORK DIAGNOSIS
===============================

1. TRACEROUTE (failed — hops block ICMP)
   $ traceroute -w 2 -m 10 192.168.1.36
   Result: all timeouts (local LAN routers don't respond to traceroute)

2. PING 10x TO .36 — check consistency
   $ ping -c 10 192.168.1.36 | tail -5
   Result: min/avg/max = 6.6/16.4/75.0ms, stddev 19.7ms
   Insight: big range (6ms to 75ms) — that's WiFi jitter, not path latency

3. COMPARE ROUTER VS WORKSTATION (5 pings each)
   $ ping -c 5 192.168.1.1  | grep round-trip
   $ ping -c 5 192.168.1.36 | grep round-trip
   Result: router avg 18.8ms, workstation avg 25.0ms
   Insight: router has similar jitter — WiFi is the common bottleneck

4. CHECK WHICH INTERFACE IS ACTIVE
   $ ifconfig en0 | grep -E "status|inet"
   Result: en0 is active, IP 192.168.1.52 — confirmed on Wi-Fi

5. CHECK ARP TABLE — see MAC addresses of neighbors
   $ arp -a | grep "192.168.1\.(1|36)"
   Result: both on en0 (same LAN), .36 MAC = 4:7c:16:d9:54:5b
   Insight: 4:7c:16 is ASRock (your workstation motherboard)

6. CHECK WIFI HARDWARE INFO (tried, deprecated on newer macOS)
   $ /System/Library/PrivateFrameworks/Apple80211.framework/.../airport -I
   $ wdutil info
   Result: both failed/need sudo on macOS 14+

7. 30 PINGS TO .36 — better statistics
   $ ping -c 30 192.168.1.36 | grep round-trip
   Result: min/avg/max = 4.4/12.4/69.5ms, stddev 15.8ms
   Insight: average is only 12ms — the 92ms was an outlier spike

COMMANDS SUMMARY:
  ping -c N <host> | grep round-trip    — latency stats
  ping -c 10 <host> | tail -5           — quick consistency check
  ifconfig en0 | grep inet              — confirm your IP/interface
  arp -a | grep <ip>                    — see MAC + which interface
  traceroute <host>                     — path hops (often blocked LAN)
  networksetup -listallhardwareports    — list all interfaces
```

The key trick: **compare the router ping to the target ping**. If both show similar jitter, the bottleneck is the shared hop (WiFi). If only the target is slow, the extra path (Ethernet/switch) is the issue.