---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hysteria 2 GFW Bypass Status 2026
translated: false
type: note
---

Question: Is Hysteria 2 good at bypassing the GFW ban?

Answer:

**Hysteria 2 remains reasonably effective against the Great Firewall (GFW) in early 2026, but it is no longer one of the absolute strongest or most reliable options.**

Here is the current situation based on technical papers, developer discussions, and user reports:

- **Strengths of Hysteria 2 for GFW circumvention**
  - Uses QUIC (UDP-based, very similar to HTTP/3 traffic), which helps it blend in with normal web browsing/video streaming.
  - Brutal congestion control gives excellent performance on high-loss or unstable connections (common on Chinese mobile/poor international lines).
  - Many users still report stable daily usage, especially with good configuration (proper camouflage domain, consistent SNI, password auth, port hopping when available).
  - In low-to-moderate traffic scenarios it often works better than older TCP-based protocols (VMess WS, Shadowsocks plain, etc.).

- **Weaknesses and real-world problems in 2025–2026**
  - Since mid-2024 the GFW has deployed **selective QUIC/SNI censorship** (decrypts QUIC Initial packets and blocks on SNI). Many QUIC-based tools (including base Hysteria 2) became easier to target.
  - After the 2025 USENIX Security paper exposed weaknesses, communities added **SNI slicing / ECH-like defenses** to quic-go, Hysteria, sing-box, etc. → newer Hysteria 2 + sing-box / updated clients became harder to block again.
  - Still classified as **"partially blocked"** by some proxy services (region/provider/server-dependent). Some Chinese operators (e.g., certain联通/电信 areas) actively disrupt QUIC/UDP more aggressively than others.
  - Self-hosted servers are frequently blocked after days/weeks if: using non-443 ports without hopping, weak camouflage, high traffic patterns, or just bad luck with the IP being flagged.

- **Comparison with current top-tier GFW-resistant protocols (early 2026)**

  | Protocol              | GFW Resistance (2026) | Speed / Lossy Lines | Detection Risk | Notes                              |
  |-----------------------|------------------------|----------------------|----------------|------------------------------------|
  | VLESS + Reality       | ★★★★★                 | Good                 | Very low       | Currently considered #1 by most    |
  | VLESS + gRPC + uTLS   | ★★★★☆                 | Medium               | Low            | Still strong with good fingerprint |
  | Hysteria 2            | ★★★☆☆                 | Excellent            | Medium         | Fast but more variable stability   |
  | TUIC v5               | ★★★☆☆                 | Very good            | Medium         | Similar QUIC family                |
  | WireGuard / AmneziaWG | ★★☆☆☆                 | Good                 | High           | Easily fingerprinted nowadays      |

**Bottom line**
Hysteria 2 is **still good** (especially if you value speed on bad lines and use modern clients + proper camouflage), but it is **not the most bullet-proof choice** anymore. Many experienced users now treat **Reality-based flows** as primary and keep Hysteria 2 / TUIC as fast backup protocols. Stability heavily depends on:

- your ISP + region
- server provider / IP reputation
- exact client + server version
- whether you use port hopping / frequently change config

If your current Hysteria 2 node dies quickly, try switching to Reality first.

References:

- [Exposing and Circumventing SNI-based QUIC Censorship of the Great Firewall of China (USENIX Security 2025)](https://gfw.report/publications/usenixsecurity25/en)
- [Hysteria 2 official documentation and discussions](https://github.com/apernet/hysteria/discussions)
- [Community reports on partial blocking (Xeovo Hub)](https://hub.xeovo.com/posts/115-hysteria-20-launch-new-way-to-bypass-censorship)
