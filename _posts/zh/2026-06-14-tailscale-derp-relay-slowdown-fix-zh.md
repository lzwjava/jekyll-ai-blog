---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale DERP中继减速修复
translated: true
type: note
---

## Tailscale SSH 缓慢问题 — 完整诊断

### 网络拓扑
```
Mac (<IP_ADDRESS>)              →  (<IP_ADDRESS>) to
Parents' home, Guangzhou             Your home, Zengcheng
<IP_ADDRESS> (Wi-Fi)                 <IP_ADDRESS> (ethernet)
Public IP: <IP_ADDRESS>              Public IP: <IP_ADDRESS>
Router: TL-WR886N (UPnP ✓)          Router: <IP_ADDRESS> (OpenWrt/LuCI, UPnP ✗)
```

### 根本原因
Tailscale 使用的是 **DERP 中继** 而非直接连接：
```
Mac → DERP(sin) Singapore → to     ~500ms RTT → 5-6s SSH
Mac → DERP(lax) Los Angeles → to   ~350ms RTT → 5-6s SSH
```
两台机器都在 NAT 之后，但直接路径是可能的，因为：
- `to` 具有 **cone NAT**（`MappingVariesByDestIP: false`）— STUN 发现一个稳定的端点
- Mac 所在的父母家路由器具有 **UPnP** — Tailscale 可以打开一个端口

Tailscale 没有自行发现这条直接路径 — 它在完成对等探测之前就选择了 DERP。

### 应用修复
运行 `tailscale ping --until-direct` 强制 Tailscale 持续探测直到找到直接路径：
```
Before:  via DERP(sin/lax)   343-721ms per packet   SSH 5-6s
After:   via direct <IP_ADDRESS>:<PORT>   76ms        SSH 1.9s
```
当前状态：
```
<IP_ADDRESS>   to   active; direct <IP_ADDRESS>:<PORT>
```

### 为何无法直接连接

| 因素 | Mac (父母家) | to (你家) |
|--------|-------------------|----------------|
| NAT 类型 | UPnP 可用 | Cone NAT（稳定端口） |
| UPnP | ✓ (TL-WR886N) | ✗ (家庭路由器无 UPnP) |
| IPv6 | ✗ | ✗ (已禁用，无全局地址) |
| STUN 端点 | 已发现 | 稳定映射端口 |
| 入站可达 | 是 (通过 UPnP) | 否 (ICMP 被阻止，无端口转发) |

直接路径之所以有效，是因为 `to` 的 cone NAT 持续保持其端口映射，且 Mac 可以向其发送 UDP。Tailscale 的发现时机在找到该路径前就放弃了。

### SSH 配置说明
你的 SSH 配置中有 `lzw-to` 并设置了 `ProxyCommand none` — 正确。通配符 `Host !192.168.*.*` 通过 SOCKS5 代理（`localhost:7891` → hysteria2 → LA）路由。这不影响 Tailscale 流量（守护进程使用自己的隧道），但建议优先使用 `ssh lzw-to` 而不是 `ssh lzw@<IP_ADDRESS>` 以明确指定。

### 推荐的永久修复方案

1. **在家庭路由器上转发 UDP 41641**（LuCI → `<IP_ADDRESS>`）— 使 `to` 始终入站可达，直接连接立即建立，无需 DERP 回退。

2. **在 Mac 上定期重新探测** — 如果你不想改动路由器：
   ```bash
   */10 * * * * tailscale ping -c 1 --until-direct <TAILSCALE_IP> > /dev/null 2>&1
   ```

3. **在家庭路由器上启用 IPv6** — 如果中国电信提供公共 IPv6 前缀，Tailscale 可以直接进行 NAT 穿越，无需 STUN/UPnP。

**选项 1 最佳** — 一次性配置，永久修复。