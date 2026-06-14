---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Misled by Proxy Location
translated: false
type: note
---

**Question:** Summarize the network diagnosis, redacting all IP addresses, and focus especially on the key discovery at the bottom.

**Answer:**

## Network Diagnosis Summary

### Setup

- **Mac** (parents' home, Guangzhou District A) connects via hysteria2 proxy (LA) for general traffic
- **`to` workstation** (your home, Guangzhou District B / Zengcheng) sits behind China Telecom NAT on its local subnet

### The Routing Problem

Current Tailscale path:

```
Mac (GZ District A) → hysteria2 proxy (LA, USA) → DERP relay (Singapore) → to workstation (GZ District B)
```

Latency: ~500ms average, sometimes up to 900ms.

### Key Discovery (the bottom part)

**The real issue isn't network topology — it's that Tailscale is confused about Mac's location.**

Because Mac routes all traffic through the hysteria2 proxy in LA, **Tailscale sees Mac as being in the US**, so it picks Singapore as the nearest DERP relay. The actual physical path is:

```
Guangzhou → USA → Singapore → Guangzhou
```

A completely unnecessary intercontinental round trip between two machines that are in the **same city**.

If Tailscale saw Mac's real IP (China Telecom, Guangzhou), it would pick a much closer relay — likely Hong Kong — cutting latency dramatically, possibly 5–10x.

### Root Fix

**Exclude Tailscale traffic from the hysteria2 proxy on Mac.** Let Tailscale use the real local IP for its coordination and DERP selection, while other traffic still routes through the proxy.
