---
audio: false
generated: true
image: false
lang: en
layout: post
title: PPTP VPN Protocol Explained
translated: false
type: note
---

Question: What is PPTP in a VPN?

Answer: **PPTP (Point-to-Point Tunneling Protocol)** is an old VPN protocol that creates a tunnel between your device and a VPN server.

At a high level:

```text
Your device
    │
    │  PPTP tunnel
    ▼
VPN server
    │
    ▼
Internet
```

### How it works

PPTP essentially combines:

1. **PPP** — carries your network traffic.
2. **GRE** — encapsulates the PPP packets.
3. **MPPE** — encrypts the PPP payload.

Historically, PPTP commonly uses:

```text
TCP 1723  → control connection
GRE       → carries the tunneled data
```

The important detail is that **GRE is not TCP or UDP**; it's IP protocol number 47.

### Why you should not use PPTP today

PPTP's authentication/encryption design is fundamentally broken. In particular, **MS-CHAPv2**, commonly used with PPTP, has practical cryptographic weaknesses that make captured VPN traffic susceptible to offline password attacks.

So:

```text
PPTP
 ├── easy to implement
 ├── fast
 ├── widely supported historically
 └── ❌ cryptographically obsolete
```

Modern VPNs generally use **WireGuard**, **IKEv2/IPsec**, or **OpenVPN** instead.

If you're looking at PPTP because you're debugging a legacy VPN, I can also walk through the **actual packet flow (`TCP 1723 → GRE → PPP → MS-CHAPv2`) with tcpdump/Wireshark commands**.