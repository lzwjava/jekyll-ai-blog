---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 国内DNS劫持跳转伪造IP
translated: true
type: note
---

Question: 为什么在这种情况下（使用 doh.pub 和 AliDNS 等国内 DoH/DoT 服务器）我们不需要配置 enhanced-mode: fake-ip 和 fake-ip-range？

Answer:

当使用**纯国内 DNS 服务器**时，你**并不严格需要** `enhanced-mode: fake-ip`（以及对应的 `fake-ip-range`），例如：

- `https://doh.pub/dns-query`
- `https://dns.alidns.com/dns-query`
- `tls://223.5.5.5:853` (AliDNS DoT)

这是因为在这些配置下，对于大多数用户关注的域名，这些服务器通常**不会遭受严重的 DNS 污染（DNS poisoning）**。

### 为什么通常推荐 fake-ip（以及为什么这里往往不需要）

| 场景 | DNS 污染 / 劫持风险 | 是否需要 fake-ip？ | 原因 |
|------------------------------------|--------------------------------|---------------|--------|
| 直接使用国外 DoH/DoT (1.1.1.1, 8.8.8.8 等) | 高（特别是 Google, Twitter, YouTube, OpenAI 等） | 强烈推荐 | Fake-ip 防止本地 ISP/GFW 看到真实查询并返回伪造/错误的 IP |
| 使用国内 DoH/DoT (doh.pub, AliDNS, 360 等) | 低到中（通常仅污染极敏感的国外域名） | 通常**不要求** | 这些 resolver 在中国境内运行 → 它们为国内网站返回基本干净的结果，为国际网站提供相对准确的结果（或至少不是离谱的虚假 IP） |
| 你处于 TUN mode 并追求极致隐私 / 防泄漏 | 始终有用 | 仍然推荐 | Fake-ip 对 App 和内核隐藏了真实的 destination IPs |
| 你只关心基础连接性 + 速度 | 低优先级 | 可以跳过 | 国内 DoH 速度快且很少完全失效 |

### 针对你的特定案例（你展示的配置）

```yaml
dns:
  enable: true
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - tls://223.5.5.5:853
```

- 所有列出的服务器都是**国内**的 → 在常见的代理/测试域名上发生严重污染的概率较低。
- 尤其是 doh.pub，在国际解析方面以相对干净著称（许多中国的 Clash 用户将其作为首选）。
- AliDNS (223.5.5.5) 在国内通常可靠且快速。
- 未使用国外 upstream DNS → 无需通过 fake-ip 技巧来向 GFW 隐藏查询。

因此，在这种配置下：

- DNS 解析已经足够可信。
- 你避免了 fake-ip 模式带来的轻微额外开销或复杂性。
- 大多数 App 都能获得正确的 IP → 代理工作正常。
- 你仍然可以正常浏览、通过代理使用 ChatGPT 等，不会有明显的 DNS 相关故障。

### 即使使用国内 DNS，什么时候**应该**添加 fake-ip

如果你注意到以下症状，请将其加回：

- 某些国外域名解析到了错误的/中国的 IP（例如 google.com → 某个随机的内地服务器）
- 你频繁访问度极高敏感/受严格审查的域名
- 你对 DNS leaks 有强迫症或想要最大程度的隔离
- 你配合 TUN mode 使用，并希望 App 永远看不到真实的 destination IPs

在这种情况下，只需添加：

```yaml
dns:
  enable: true
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - tls://223.5.5.5:853
```

大多数中国的 Clash Verge / Mihomo 用户在坚持使用国内 DoH/DoT 时，都会在**不开启 fake-ip** 的情况下运行——这对于日常代理使用来说效果非常好。

结论：
在当前的配置下 → **你可以为了简单和速度安全地跳过 fake-ip**。
如果你以后切换回 Cloudflare/Google DoH 或者发现任何奇怪的解析问题 → 届时再添加 fake-ip。

References:

- [MetaCubeX mihomo DNS enhanced-mode explanation](https://wiki.metacubex.one/en/config/dns)
- [Clash fake-ip vs redir-host discussion (Chinese community)](https://github.com/MetaCubeX/mihomo/discussions/456)
- [Common China Clash DNS setups without fake-ip](https://github.com/Loyalsoldier/clash-rules)
