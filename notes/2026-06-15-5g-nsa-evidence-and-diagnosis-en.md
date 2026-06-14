---
audio: false
generated: true
image: false
lang: en
layout: post
title: 5G NSA Evidence and Diagnosis
translated: false
type: note
---

Yes, almost certainly **5G NSA**. Here's the evidence from your diagnostics:

**Definitive proof:**

```
1. Same CGNAT IP on both:     14.31.170.218
   → Core network didn't change, only the radio layer did
   → SA would give you a different IP range and different routing

2. Same traceroute structure:  172.20.10.1 → 192.168.147.x → 192.168.242.x
   → Same private IP hops = same 4G EPC core
   → SA would show different gateway paths

3. Same NAT type:              Port-Restricted Cone
   → Determined by the core network, not the radio
   → Unchanged = same core = NSA

4. Worse latency + jitter:     89ms→136ms, ±3.6ms→±44ms
   → NSA adds 4G/5G coordination overhead
   → SA would show LOWER latency than 4G
```

You can also confirm on your iPhone directly:

```
Settings → Cellular → Cellular Data Options → Voice & Data
```

If it shows "5G Auto" or "5G" (not "5G SA" or "5G+ Standalone"), that's NSA. China Telecom's 5G rollout is predominantly NSA — SA is only available in select test cities and requires specific plan/SIM support.

**Bottom line:** Your 5G is running on a 4G core with 5G radio bolted on. The 2x speed boost is real (fatter pipe), but the latency penalty is the NSA tax. You'll only see true 5G latency (<10ms) when China Telecom deploys SA in your area — which is probably years away.
