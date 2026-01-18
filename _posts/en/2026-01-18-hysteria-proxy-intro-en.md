---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Introduction to Hysteria Proxy Protocol
translated: false
type: note
---

**Question:** What is an introduction to the Hysteria protocol for proxy use?

**Answer:**

Hysteria (especially **Hysteria 2**, the current version) is a high-performance, censorship-resistant proxy protocol/tool designed to provide fast and stable connections over poor, lossy, or heavily censored networks (such as satellite links, congested Wi-Fi, or regions with strict internet filtering like China).

### Core Features
- **Underlying Technology** — Built on **QUIC** (the transport protocol that powers HTTP/3), which runs over UDP instead of TCP. This gives it advantages in lossy networks where TCP often slows down dramatically due to packet loss.
- **Masquerading** — The protocol is designed to look exactly like standard **HTTP/3** traffic to outside observers (censors, DPI systems, ISPs). Without valid authentication credentials, a Hysteria server behaves just like a normal HTTP/3 web server (e.g., returning 404, serving files, or acting as a reverse proxy). This makes blocking it very difficult without also blocking large amounts of legitimate web traffic.
- **Congestion Control** — Uses a custom algorithm called **Brutal** (in Hysteria 2), which tries to maintain a user-specified bandwidth (e.g., 100 Mbps down) even when there is significant packet loss — very useful in unstable networks. (It can also fall back to BBR.)
- **Performance Focus** — Optimized for maximum throughput rather than minimal loss, making it faster than many traditional proxies (Shadowsocks, V2Ray/Vmess, Trojan) in bad network conditions.

### Proxy Modes and Usage
Hysteria itself is not a traditional VPN; it is primarily a proxy protocol with multiple output modes:
- **SOCKS5** proxy (most common)
- **HTTP** proxy
- **TCP/UDP port forwarding**
- **Linux TProxy** (transparent proxy)
- **TUN mode** (virtual network interface for system-wide proxying on Windows, macOS, Linux — handles TCP + UDP only)

You typically run a Hysteria **server** on a VPS/cloud host (with a domain and TLS certificate), then connect using the official client or third-party apps (Nekobox, sing-box, Shadowrocket, etc.) that support Hysteria 2.

### Typical Use Cases
- Bypassing censorship (GFW, etc.) where UDP is not heavily blocked
- Getting stable high speed on mobile networks, international flights, or satellite internet
- Scenarios where traditional TCP-based proxies become very slow due to packet loss

### Quick Comparison
- Vs Shadowsocks/Trojan → Much better performance on lossy links, harder to detect
- Vs WireGuard/OpenVPN → More stealthy (looks like HTTPS), usually faster in bad conditions, but not a full L3 VPN (no ICMP/ping by default in TUN mode)
- Vs Reality/VLESS → Different masquerading approach (HTTP/3 vs TLS-in-TLS); Hysteria often wins on unstable links

Official project: https://github.com/apernet/hysteria  
Documentation (Hysteria 2): https://v2.hysteria.network/

**References:**

- [Hysteria 2 Official Site](https://v2.hysteria.network/)
- [Protocol Documentation](https://v2.hysteria.network/docs/developers/Protocol)
- [GitHub Repository](https://github.com/apernet/hysteria)
- [Sing-box Hysteria2 Integration](https://sing-box.sagernet.org/manual/proxy-protocol/hysteria2)