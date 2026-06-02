---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Clash DNS 配置指南
translated: true
type: note
---

我可以帮你修复你的 Clash DNS 配置。问题可能出在 `fallback` URL 的格式或你的整体 DNS 设置上。这里有一个修正后的配置，用于使用全局 DNS：

```yaml
dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 8.8.8.8
    - 1.1.1.1
  fallback:
    - 1.0.0.1
    - 8.8.4.4
```

**关键修改：**

1. **移除 fallback 中的 HTTPS URL** — `fallback` 部分应该只包含 DNS server（IP 地址或 Clash 实际支持的 DNS-over-HTTPS URL），而不是任意的 HTTP 路径。你写的 `192.168.0.1/dns-query` 无法正常工作。

2. **使用标准公共 DNS server** — 对于全局 DNS，请坚持使用经过验证的服务商，例如：
   - `8.8.8.8` 和 `8.8.4.4` (Google)
   - `1.1.1.1` 和 `1.0.0.1` (Cloudflare)
   - `208.67.222.222` 和 `208.67.220.220` (OpenDNS)

**如果你想使用 DNS-over-HTTPS (DoH)**，请改用以下格式：

```yaml
dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - https://dns.google/dns-query
    - https://1.1.1.1/dns-query
  fallback:
    - 8.8.4.4
    - 1.0.0.1
```

你目前遇到了什么具体的错误或问题？这将有助于我为你提供更精确的修复方案。
