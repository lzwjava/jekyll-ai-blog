---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Shadowrocket Supported Proxy Protocols Guide
translated: false
type: note
---

**Question:** What protocols does Shadowrocket support? VMess, Shadowsocks, etc.

**Answer:**

Shadowrocket is a powerful rule-based proxy utility primarily for iOS (available on the App Store), and it supports a wide range of proxy protocols commonly used for VPN-like proxy setups, bypassing restrictions, and privacy.

Here are the main protocols it supports (based on official updates, user guides, and reliable sources as of 2025–2026):

- **Shadowsocks** (including ShadowsocksR / SSR variants in many configurations)
- **VMess** (V2Ray's VMess protocol)
- **VLESS** (lightweight V2Ray protocol)
- **Trojan** (Trojan-GFW and variants)
- **SOCKS5** (and SOCKS in general)
- **HTTP / HTTPS** (standard HTTP proxy with optional TLS)
- **Hysteria** (including newer congestion control versions)
- **QUIC**-based protocols (with fixes and improvements in recent updates)
- **XTLS** (including XTLS-Vision variants)
- Other advanced ones like **WireGuard**, **OpenVPN**, and **IKEv2/IPSec** appear in some configurations or third-party integrations, but core focus is on proxy protocols rather than full VPN stacks.

It also supports many V2Ray-compatible plugins (kcptun, cloak, gost, etc.), custom TLS fingerprints, DNS-over-HTTPS/TLS/QUIC, and subscription imports (often in base64 or standard URI formats for VMess/VLESS/Trojan/Shadowsocks).

**Yes, it fully supports both VMess and Shadowsocks**, along with many modern anti-censorship protocols.

Note: The exact list can evolve with app updates (latest versions add/improve support for Hysteria, QUIC issues, XTLS, etc.). Always check the latest App Store release notes for the most current features.

**References:**

- [Shadowrocket on App Store](https://apps.apple.com/us/app/shadowrocket/id932747118)
- [RapidSeedbox Shadowrocket Guide](https://www.rapidseedbox.com/blog/shadowrocket-ultimate-guide)
- [Hiddify Shadowrocket Tutorial (GitHub)](https://github.com/hiddify/Hiddify-Manager/wiki/Tutorial-for-ShadowRocket-app)
- Various proxy setup guides mentioning VMess, VLESS, Trojan, Shadowsocks, etc. (2024–2026)