---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Shadowrocket 支持的代理协议指南
translated: true
type: note
---

**Question:** Shadowrocket 支持哪些协议？VMess, Shadowsocks 等。

**Answer:**

Shadowrocket 是一款强大的基于规则的 proxy 实用工具，主要用于 iOS（可在 App Store 购买），它支持广泛的 proxy protocols，常用于类似 VPN 的 proxy 设置、绕过限制以及隐私保护。

以下是它支持的主要协议（基于 2025–2026 年的官方更新、用户指南和可靠来源）：

- **Shadowsocks**（包括许多配置中的 ShadowsocksR / SSR 变体）
- **VMess**（V2Ray 的 VMess 协议）
- **VLESS**（轻量级 V2Ray 协议）
- **Trojan**（Trojan-GFW 及其变体）
- **SOCKS5**（以及通用的 SOCKS）
- **HTTP / HTTPS**（带可选 TLS 的标准 HTTP proxy）
- **Hysteria**（包括较新的拥塞控制版本）
- 基于 **QUIC** 的协议（在最近的更新中进行了修复和改进）
- **XTLS**（包括 XTLS-Vision 变体）
- 其他高级协议如 **WireGuard**、**OpenVPN** 和 **IKEv2/IPSec** 出现在某些配置或第三方集成中，但其核心重点是 proxy protocols 而非完整的 VPN 堆栈。

它还支持许多 V2Ray 兼容的 plugins（kcptun, cloak, gost 等）、自定义 TLS fingerprints、DNS-over-HTTPS/TLS/QUIC 以及订阅导入（通常为 VMess/VLESS/Trojan/Shadowsocks 的 base64 或标准 URI 格式）。

**是的，它完全支持 VMess 和 Shadowsocks**，以及许多现代抗封锁协议。

注意：准确的列表可能会随 App 更新而演变（最新版本增加/改进了对 Hysteria、QUIC 问题、XTLS 等的支持）。请务必查看最新的 App Store 发布说明以获取最新功能。

**References:**

- [Shadowrocket on App Store](https://apps.apple.com/us/app/shadowrocket/id932747118)
- [RapidSeedbox Shadowrocket Guide](https://www.rapidseedbox.com/blog/shadowrocket-ultimate-guide)
- [Hiddify Shadowrocket Tutorial (GitHub)](https://github.com/hiddify/Hiddify-Manager/wiki/Tutorial-for-ShadowRocket-app)
- 提及 VMess, VLESS, Trojan, Shadowsocks 等的各种 proxy 设置指南 (2024–2026)
