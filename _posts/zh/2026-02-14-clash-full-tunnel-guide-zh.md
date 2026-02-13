---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Clash 全虚拟网卡模式配置指南
translated: true
type: note
---

问题：如何配置 Clash（使用提供的部分配置片段）以实现类似全隧道（full-tunnel）的行为或更好的 proxy routing？

回答：

你当前的部分 Clash 配置看起来已经是一个典型的 Clash/Clash Meta/Clash Verge 基础配置：

```yaml
port: 7890                # HTTP proxy port
socks-port: 7891          # SOCKS5 proxy port
allow-lan: true           # 允许局域网内的其他设备使用此代理
mode: Rule                # 基于规则的路由（对大多数用户而言，推荐优于 Global）
log-level: info
external-controller: 127.0.0.1:9090
proxies:                  # ← 这里放置你的 proxy nodes
```

要使其行为更接近 **full-tunnel mode**（所有流量都通过你的 VMess/Trojan 代理，类似于 VPN），以下是完成/配置它最常用且有效的方法。

### 推荐：使用 TUN Mode（真正的系统级全隧道，macOS 上的最佳选择）

TUN mode 最接近 Cisco AnyConnect 的全隧道行为。它通过 Clash 路由 **所有流量**（TCP + UDP），而无需应用程序遵循系统代理设置。

添加/启用这些行（需要 Clash Meta / Clash Premium core）：

```yaml
# 添加或修改这些
tun:
  enable: true
  stack: system          # 或 gvisor / mixed (system 在 macOS 上最快)
  dns-hijack:
    - any:53             # 劫持所有 DNS 查询 → 防止 DNS leaks
  auto-route: true       # 自动添加路由以将所有流量通过 TUN 发送
  auto-detect-interface: true
  mtu: 9000              # 可选：较高的 MTU 可以提高速度（测试 1400–9000）
```

**带有你的片段 + TUN 的完整最小工作示例：**

```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
external-controller: 127.0.0.1:9090

tun:
  enable: true
  stack: system
  dns-hijack:
    - any:53
  auto-route: true
  auto-detect-interface: true

proxies:
  # ← 你的 VMess / Trojan 节点放在这里，例如：
  - name: "🐟 漏网之鱼"
    type: vmess
    server: your.server.com
    port: 443
    uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    alterId: 0
    cipher: auto
    udp: true
    tls: true
    network: ws
    ws-opts:
      path: /yourpath
      headers:
        Host: your.host.com

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - "🐟 漏网之鱼"
      - DIRECT

rules:
  - MATCH,PROXY         # ← 这使所有流量都通过代理（全隧道行为）
```

**在 macOS 上激活 TUN 的步骤：**
1. 在 Clash Verge / Mihomo / 类似的 GUI 中 → Settings → TUN Mode → Enable（授予管理员权限，安装一次 helper）。
2. 重启 Clash。
3. 将 mode 设置为 **Rule**（如果你不想要任何例外，则设置为 Global）。
4. 测试：`curl ipinfo.io` 应该显示你的代理 IP，即使在 Terminal / 非浏览器应用中也是如此。

### 替代方案：保持 System Proxy 模式，但让它“感觉”更像全隧道

如果你不想使用 TUN（例如：避免管理员权限或内核扩展）：

```yaml
# 保留你原始设置，添加/增强：
mode: Global              # 而不是 Rule → 强制所有流量通过代理
# 或者保持 Rule 并添加强大的最终规则：
rules:
  - MATCH,PROXY         # 所有未匹配的流量都指向代理

# 可选：强制 DNS 通过代理以避免泄露
dns:
  enable: true
  ipv6: false           # 除非你的节点支持 IPv6，否则禁用它通常更安全
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 8.8.8.8
    - 1.1.1.1
  fallback:
    - https://1.1.1.1/dns-query
```

### 快速总结：选择哪种模式？

| 目标 | 推荐的配置更改 | 需要管理员权限？ | UDP 支持？ | 绕过大多数应用？ |
|-----------------------------------|------------------------------------|----------------------|--------------|----------------------|
| 真正的全隧道 (类似 AnyConnect) | 启用 TUN + `MATCH,PROXY` | 是 | 是 | 是 |
| 为大多数应用提供强代理 | `mode: Global` 或 `MATCH,PROXY` | 否 | 否 (仅 TCP) | 部分 |
| 智能路由 (中国直连，其余代理) | 保持 `mode: Rule` + 优秀的规则 | 否 | 否 | 部分 |

**2026 年大多数使用 VMess/Trojan 节点的各用户都使用 TUN mode** —— 它能提供最佳体验（用于游戏/语音的 UDP，无应用级代理问题，完整的 DNS 控制）。

如果你分享更多的配置（特别是 proxy-groups 和 rules），我可以给出更精确的建议。

References:  

- [Clash Meta TUN Mode Documentation](https://github.com/MetaCubeX/mihomo/wiki/TUN-device)
- [Clash Verge User Guide - TUN Setup](https://github.com/clash-verge-rev/clash-verge-rev/wiki)
- [Common Clash Configuration Examples](https://github.com/Loyalsoldier/clash-rules)