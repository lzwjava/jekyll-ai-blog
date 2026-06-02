---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Seeker Transparent Proxy Technical Overview
translated: false
type: note
---

Question: How does the Rust-based Seeker transparent proxy actually work under the hood?

Answer:
Seeker creates a **fully transparent system-wide proxy** by combining a **virtual TUN interface** with a **user-space routing + proxy engine** written in Rust. It works without requiring any application to be proxy-aware (no PAC, no SOCKS/HTTP settings in browsers or apps).

Here’s the detailed technical flow:

### 1. TUN Interface Creation
- Seeker creates a virtual network interface (usually `utun10` on macOS or `tun0` on Linux).
- It assigns an IP (default 198.18.0.1/24) and brings the interface up.
- It then **changes the system’s default route** so **all IP packets** (except those going to the real gateway or local networks) are routed into this TUN device.
- From the kernel’s perspective, every outgoing packet now arrives in user-space via the TUN file descriptor.

### 2. Packet Reading Loop (Rust async/tokio)
- The main loop continuously reads raw IP packets from the TUN fd.
- Packets are parsed using the `etherparse` crate:
  - IPv4/IPv6 → TCP/UDP/ICMP
- It extracts the **original destination IP + port** (this is critical for transparency).

### 3. Rule Matching (Clash-compatible)
- For every new TCP or UDP flow, Seeker looks up the destination domain/IP in its rule set:
  - First resolves domain if needed (via its own DNS server on 127.0.0.1:53)
  - Supports rules like `DOMAIN-SUFFIX,netflix.com,PROXY`, `GEOIP,CN,DIRECT`, etc.
  - Actions: **PROXY**, **DIRECT**, or **REJECT**

### 4. Connection Handling Paths

**A. DIRECT (bypass)**
- Packet is written straight back into the TUN with the original source IP preserved.
- Kernel routes it normally → goes out through your real gateway.

**B. REJECT**
- Sends TCP RST or ICMP unreachable back into the TUN.

**C. PROXY (the interesting case)**
- Seeker **establishes a new connection** to the selected proxy server (Shadowsocks, SOCKS5, or HTTP CONNECT).
- It then **shuttles data** bidirectionally between:
  - The original application ↔ Seeker (via TUN packets)
  - Seeker ↔ Remote proxy server (real TCP/UDP socket)
- For TCP: simple bidirectional copy using tokio async streams.
- For UDP: implements UDP NAT-like mapping (source port → proxy association) so replies can be routed back correctly.
- For ICMP ping: uses Fake-IP mode (like Clash) — maps real destination IPs to 198.19.0.0/16 range so pings work through TCP-based proxies.

### 5. DNS Hijacking
- Starts a local DNS server on 127.0.0.1:53 (takes over system DNS).
- For domains that should go through proxy, it can return **Fake-IPs** (so subsequent packets hit the TUN).
- Restores original DNS settings on clean exit.

### 6. Gateway / LAN Mode (optional)
- Binds DNS to 0.0.0.0:53 and expects other devices to point gateway/DNS to your machine.
- All traffic from the entire LAN flows through the same TUN + proxy logic.

### Core Rust Crates Used
- `tokio` + `async-std` – async runtime
- `etherparse` – IP/TCP/UDP/ICMP packet parsing & serialization
- `tun` / `smoltcp` style – TUN interface handling
- `shadowsocks-rust` style code – Shadowsocks encryption
- `yaml-rust` / `serde` – config parsing

In short: Seeker turns your machine into a **virtual VPN-like router** that intelligently redirects traffic through proxies based on domain/IP rules — entirely in safe, high-performance Rust.

*[GitHub - gfreezy/seeker](https://github.com/gfreezy/seeker)*
*[Main entry point (main.rs)](https://github.com/gfreezy/seeker/blob/master/src/main.rs)*
*[TUN handling module](https://github.com/gfreezy/seeker/blob/master/src/tun.rs)*
*[Rule engine](https://github.com/gfreezy/seeker/blob/master/src/rule/mod.rs)*
