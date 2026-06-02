---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-haiku-4.5
title: Clash 全球模式浅析
translated: true
type: note
---

这是一个非常好的问题！Clash 中的 "Global mode"（全局模式）意味着所有的流量都会经过 Proxy。其工作原理如下：

**Global Mode 流程：**

1. **DNS Resolution** — 当你的设备请求一个域名（例如 `google.com`）时，Clash 会拦截该请求，并使用其配置的 DNS servers 将其解析为 IP 地址。

2. **Routing Decision** — 随后 Clash 决定流量的去向：
   - 在 **global mode** 下，所有的流量（不仅仅是特定的域名或 IP）都会通过你的 Proxy/VPN 进行路由。
   - 这与 **Rule mode** 不同，在 Rule mode 下，只有匹配你规则的特定流量才会经过 Proxy。

3. **Proxy Forwarding** — 解析后的流量将通过你配置的 Proxy server 发送到目的地。

**为什么要使用 global mode？**

- 所有内容都经过加密并由 Proxy 路由（更高的隐私性）
- 绕过所有层面的 Geo-blocking 或限制
- 当你需要完全的匿名性时非常有用

**DNS configuration 的作用：**

```yaml
nameserver:
    - 8.8.8.8
    - 1.1.1.1
```

这些配置将域名解析为 IP。当 Clash 收到 DNS query 时，它会使用这些 servers。`fallback` servers 是在 primary servers 失败时的备用方案。

**Fake-IP mode 的优势：**

```yaml
fake-ip-range: 198.18.0.1/16
```

Clash 不会等待真实的 DNS resolution，而是立即分配临时的 Fake IP 并在后台进行解析——这带来了更快的响应速度。

**常见问题：** 如果你在 global mode 下遇到 DNS 错误，通常意味着 nameservers 无法访问，或者与系统的 DNS 设置存在冲突。在启用 global mode 之前，请先确保你的 Proxy 连接正常工作。

你在开启 global mode 后遇到连接困难了吗？
