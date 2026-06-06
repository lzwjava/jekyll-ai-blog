---
audio: false
generated: true
image: false
lang: en
layout: post
title: China Telecom CGNAT Home Network Analysis
translated: false
type: note
---

Good, now you're on your HOME network. Here's the analysis:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOME NETWORK — China Telecom Fiber
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Local IP:   192.168.22.5
  Gateway:    192.168.22.1 (your home router)
  Subnet:     /24 (255.255.255.0)
  Public IP:  [REDACTED] (Shenzhen, AS4134 CHINANET)

  Ping to baidu:  avg 23ms, jitter 24ms ← good
  Ping to gateway: avg 16ms (first hop 69ms cold start, then 3ms)

  Download:  ~413 KB/s (~3.3 Mbps)
  Upload:    ~380 KB/s (~3.0 Mbps)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOUBLE NAT — YES, CONFIRMED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The traceroute proves it:

  Hop 1:  192.168.22.1     ← NAT #1: your home router
  Hop 2:  172.16.3.252     ← NAT #2: ISP CGNAT gateway
  Hop 3:  ** *            (hidden)
  Hop 4:  14.147.195.133   ← public backbone
  ...
  Hop 9:  14.29.117.178    ← near destination

  172.16.3.252 is a PRIVATE IP (172.16.0.0/12 range).
  That's China Telecom's CGNAT — your traffic goes through
  TWO NAT layers before hitting the public internet:

    You (192.168.22.5)
      → Home router (192.168.22.1) [NAT #1]
        → ISP CGNAT (172.16.3.252) [NAT #2]
          → Public IP [REDACTED]

  Why does China Telecom do this?

- IPv4 address exhaustion — not enough public IPs for everyone
- They share one public IP across many customers via CGNAT
- This is standard for Chinese residential broadband since ~2015

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT DOUBLE NAT MEANS FOR YOU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- No inbound connections: port forwarding on your home router
    won't work because CGNAT blocks it upstream anyway
- No self-hosting from home (web server, SSH, etc.)
- VPN hosting from home won't work
- P2P games/apps may have issues
- Normal browsing, LLM APIs, dev work: totally fine

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPARISON: HOME vs EARLIER HOTSPOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    Home (fiber)        Hotspot (4G/5G)
  ─────────────────────────────────────────────────────────
  Ping avg            23ms                215ms
  Ping jitter         24ms                341ms
  Packet loss         0%                  20%
  Download            3.3 Mbps            2.3 Mbps
  Upload              3.0 Mbps            0.5 Mbps
  NAT layers          2 (router+CGNAT)    3 (iPhone+router+CGNAT)
  Gateway ping        3ms                 N/A

  Home is clearly better — 10x lower latency, 6x less jitter,
  6x faster upload. But both go through CGNAT.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTE: Your home bandwidth (3.3 Mbps down) seems low for fiber.
Could be Wi-Fi negotiation at a low rate. If you connect via
Ethernet you'd likely see 100+ Mbps. The bottleneck is probably
your MacBook's Wi-Fi link speed, not the fiber itself.
