---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iOS双重VPN代理设置指南
translated: true
type: note
---

**问题：** 在 iOS 的 VPN 限制和中国网络环境下，如何同时配置 Tailscale 和 Shadowsocks？

**回答：**

iOS 限制**同时只能有一个 VPN 活动**，因此需要路由策略。以下按可靠性排序的实用解决方案：

## 1. **Shadowsocks 代理模式（推荐）**

最清晰的方法：将 Shadowsocks 作为 **SOCKS5/HTTP 代理**（非 VPN 模式），然后 Tailscale 作为 VPN。

**iOS 设置：**
- 安装 **Shadowrocket**（付费，最灵活）或 **Quantumult X**（功能更强）
- 将 Shadowsocks 服务器配置为代理规则（SOCKS5），而非 VPN
- 独立启用 Tailscale VPN
- 在 Shadowrocket 中设置：
  ```
  [Proxy]
  ProxyName = SOCKS5, <SS_SERVER_IP>, <SS_PORT>, chacha20-poly1305, <PASSWORD>

  [Rule]
  # 将中国流量通过 Shadowsocks 路由
  GEOIP,CN,ProxyName
  FINAL,DIRECT
  ```

此方案可行是因为代理规则作用于应用层，而非系统 VPN。Tailscale 处理 VPN 隧道，Shadowrocket 处理特定域名/区域的代理路由。

---

## 2. **路由 Tailscale 流量，代理其余所有内容**

如果需要两者全局工作：

```bash
# 在同时运行两个服务的 Mac/Linux 网关上：
# 配置 Shadowsocks 监听 0.0.0.0:1080
# 正常配置 Tailscale

# 在 iOS 上：
# - 连接到 Tailscale VPN
# - 通过 Tailscale IP 将应用/浏览器指向 Shadowsocks 网关
```

**Shadowrocket 中的 iOS 配置：**
```
[Proxy]
Gateway = <TAILSCALE_IP_OF_SS_GATEWAY>, 1080

[Rule]
# 不在 Tailscale 网络上的任何内容都使用 Shadowsocks 代理
GEOIP,CN,Gateway
FINAL,DIRECT
```

---

## 3. **选择性 VPN，以 Shadowsocks 为主**

如果 Shadowsocks 更重要（在中国很可能如此）：

- **主要：** Shadowrocket 中的 Shadowsocks 作为 VPN
- **次要：** 通过 **Shadowsocks 路由的 HTTP 代理** → Tailscale 控制服务器访问 Tailscale

这需要将 Tailscale 配置为使用 SOCKS5 代理：
```bash
# Tailscale CLI 不直接支持代理，但你可以：
# 1. 通过 Shadowsocks 代理 SSH 进入 Tailscale 对端
# 2. 或者在 macOS/Linux 端使用 ProxyChains
```

---

## 4. **硬件网关（最稳定）**

如果你有持续的 VPN 需求，可以在 Ubuntu 机器上同时运行两者：

```bash
# 安装 ss-server（或使用 sslocal 客户端模式）
apt install shadowsocks-libev

# 启动 Shadowsocks
ss-server -c /etc/shadowsocks-libev/config.json -u

# 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# 现在 iOS 连接：
# 1. Tailscale VPN 连接到你的 Ubuntu 机器
# 2. Shadowsocks 流量通过同一机器的代理路由
```

iOS Shadowrocket 配置：
```
[Proxy]
ShadowsocksGW = SOCKS5, 100.x.x.x (Tailscale IP), 1080

[Rule]
GEOIP,CN,ShadowsocksGW
FINAL,Tailscale
```

---

## 为何可行

- **代理 ≠ VPN**：iOS 允许多个代理，但只允许一个 VPN
- **Shadowsocks 作为代理** 在应用层处理流量拦截
- **Tailscale VPN** 处理到你的机器的安全隧道
- 无冲突，因为它们运行于不同层次（第 7 层代理 vs 第 3 层 VPN）

---

## iOS 应用推荐

| 应用 | 代理 | VPN | 费用 | 备注 |
|-----|-------|-----|------|-------|
| **Shadowrocket** | ✓ | ✓ | $3-5 | 最灵活，国内支持最佳 |
| **Quantumult X** | ✓ | ✓ | $8 | 规则引擎更强大 |
| **Surge** | ✓ | ✓ | $10 | 除非需要日志记录，否则功能过剩 |
| **Tailscale iOS** | — | ✓ | 免费 | 仅用于 Tailscale |

使用 **Shadowrocket 进行路由**，**Tailscale 应用独立作为 VPN**。

---

**关键点：** 别再想“两个 VPN”——要思考“一个 VPN + 一个代理”。Shadowsocks 擅长作为代理层，Tailscale 作为 VPN 层。它们为不同的工作而设计。