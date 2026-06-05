---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mobile Hotspot vs Home Network Comparison
translated: false
type: note
---

Here's the full picture of your mobile hotspot network vs your home network:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MOBILE HOTSPOT (China Telecom 4G/5G) — Current Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Network Path:
  MacBook (172.20.10.3) → iPhone hotspot (172.20.10.1)
    → China Telecom CGNAT → Internet

  Real public IP:  183.42.160.71 (Shenzhen, Guangdong)
  Carrier:         AS4134 CHINANET BACKBONE
  NAT layers:      Double NAT (iPhone + CGNAT)
  Subnet:          /28 — only 14 usable IPs
  MTU:             1500 (OK)
  IPv6:            Native (240e:47e:1490:dbb0::/64)
  Proxy:           127.0.0.1:7890 (Clash → DMIT LA)

Performance (raw, no proxy):
  Ping to baidu:   15–1157ms, avg 215ms, jitter 341ms ← TERRIBLE
  8.8.8.8:         275–625ms, 20% packet loss
  114.114.114.114: 100% packet loss (ICMP blocked or carrier filtered)
  Direct IP ping:  100% loss (carrier blocks inbound ICMP on mobile)

Performance (via proxy — DMIT LA):
  Baidu:   229ms TTFB (proxy accelerates!)
  GitHub:  600ms TTFB
  Google:  478ms TTFB

Bandwidth:
  Download: ~291 KB/s (~2.3 Mbps) — slow
  Upload:   ~68 KB/s (~0.5 Mbps) — very slow

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY DIFFERENCES vs YOUR HOME NETWORK (expected):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    Mobile Hotspot      Home (China Telecom fiber)
  ─────────────────────────────────────────────────────────────────
  NAT layers        Double NAT          Single NAT
  Ping jitter       341ms (wild)        ~2-5ms (stable)
  Ping avg          215ms to baidu      ~5-15ms to baidu
  Download          ~2 Mbps             ~100-300 Mbps typical
  Upload            ~0.5 Mbps           ~30-50 Mbps typical
  Packet loss       20% to 8.8.8.8      0%
  ICMP inbound      Blocked (CGNAT)     Usually works
  IPv6              Native ✓            Native ✓
  DNS               Via phone gateway   Direct to 100.100.100.100
  Latency stability High variance       Low variance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. JITTER IS THE BIG PROBLEM — 341ms stddev means your connection
   is wildly inconsistent. Some pings hit 15ms, others 1157ms.
   This makes SSH, video calls, and real-time tools painful.
   Cause: cellular radio congestion, signal handoff between towers.

2. DOUBLE NAT — iPhone hotspot adds an extra NAT layer on top of
   China Telecom's CGNAT. This means:
   - No inbound connections possible (no port forwarding)
   - Extra latency hop
   - Some protocols break (VPN, FTP, SIP)

3. UPLOAD IS TRAGIC — 68 KB/s means git push, file uploads, and
   Claude Code conversations with large contexts will crawl.

4. PROXY ACTUALLY HELPS — Your Clash proxy (DMIT LA) gives
   faster TTFB to international sites than direct connection.
   The proxy route through LA has better peering than China
   Telecom's direct international links. Surprising but real.

5. ICMP FILTERING — China Telecom mobile blocks most inbound ICMP.
   114.114.114.114 and your own IP unreachable. This is normal
   for mobile networks.

BOTTOM LINE:
  Mobile hotspot is usable for light browsing and LLM API calls
  (small payloads), but terrible for anything latency-sensitive
  or bandwidth-heavy. Your home fiber connection is ~50-100x
  faster and far more stable. Use the hotspot as emergency
  backup only — the jitter alone will drive you crazy for
  development work.
