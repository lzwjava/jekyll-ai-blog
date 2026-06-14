---
audio: false
generated: true
image: false
lang: en
layout: post
title: Redact DMIT Proxy IP Output
translated: false
type: note
---

**Question:** Redact the DMIT proxy IP from the comparison output and re-display it.

**Answer:**

```
═══════════════════════════════════════════════════════════════
  4G vs 5G HOTSPOT COMPARISON
═══════════════════════════════════════════════════════════════
                        4G              5G           Change
──────────────────────────────────────────────────────────────
SPEED
  Download             11.6 Mbps       21.3 Mbps     +84%  ↑↑
  Upload               7.7 Mbps        14.7 Mbps     +91%  ↑↑
LATENCY (avg)
  1.1.1.8              89ms            136ms         +53%  ↓
  Jitter (1.1.1.8)     ±3.6ms          ±44.1ms       way worse ↓↓
  8.8.8.8              235ms           346ms         +47%  ↓
  Jitter (8.8.8.8)     ±36.5ms         ±183.0ms      way worse ↓↓
CONNECTIVITY
  Public IP (STUN)     14.31.170.218   14.31.170.218  SAME (same carrier CGNAT)
  HTTP exit IP         <IP_ADDRESS>    <IP_ADDRESS>   SAME (DMIT proxy)
  NAT Type             Port-Restr Cone Port-Restr Cone SAME
  Double NAT           Yes             Yes            SAME
  Local IP             172.20.10.3     172.20.10.3    SAME
TRACEROUTE (hop 3 & 5)
  Hop 3                39-24ms         22-82ms        more variation
  Hop 5                116ms           15-20ms        faster!
═══════════════════════════════════════════════════════════════
  VERDICT
═══════════════════════════════════════════════════════════════
  ✅ 5G is ~2x FASTER for both download and upload
  ❌ 5G has WORSE latency and much higher jitter
  🔄 Same carrier CGNAT IP, same NAT type, same double NAT
  The 5G radio gives more bandwidth but the signal
  fluctuates more (typical for 5G in non-ideal coverage).
  The double NAT and CGNAT are unchanged — switching
  4G↔5G doesn't change your carrier's network topology,
  only the radio layer speed.
  For stable latency tasks (SSH, video calls, gaming):
      4G wins — jitter ±3.6ms is excellent
  For bulk transfers (downloads, streaming):
      5G wins — 2x throughput
═══════════════════════════════════════════════════════════════
```

DMIT exit IP redacted to `<IP_ADDRESS>`. The carrier STUN IP (`14.31.170.218`) and local IP (`172.20.10.3`) are left as-is since those appeared in your original data — redact those too if needed.
