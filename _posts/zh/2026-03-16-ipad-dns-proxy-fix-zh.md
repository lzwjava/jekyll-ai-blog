---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 iPad DNS 代理循环问题
translated: true
type: note
---

**问题：** 根据详细的调试日志，iPad 连接失败的确切根本原因是什麼，以及如何修复？

**答案：**

## 根本原因：已确认 — Hysteria2 Proxy Server DNS Loop

日志精确揭示了问题。这里是确切的失败链：

```
iPad → Clash TUN → tries to connect to Hysteria2 server
  → Clash DNS resolves Hysteria2 domain → returns 198.18.0.28 (FAKE IP!)
  → Clash tries to route 198.18.0.28 → TUN intercepts it again
  → sends BACK to Clash → infinite loop → connection hangs/fails
```

这是一个经典的 **"chicken-and-egg" DNS 问题** 在 fake-IP 模式下：Clash 需要联系代理服务器来转发流量，但其自身的 DNS 为代理服务器的域名返回 fake-IP，导致 Clash 试图将连接代理到它自己的代理服务器 — 无限循环。

---

## 修复方法：三部分

### 修复 1 — `proxy-server-nameserver` (最重要的)

这是 Clash Meta/Mihomo 的正确解决方案。为代理服务器域名添加专用的 DNS 解析器，绕过 fake-IP：

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16

  default-nameserver:
    - 223.5.5.5
    - 119.29.29.29

  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query

  # ↓↓↓ 这是关键修复 ↓↓↓
  # 使用真实 DNS（非 fake-IP）来解析您的代理服务器主机名
  proxy-server-nameserver:
    - https://doh.pub/dns-query
    - 223.5.5.5
```

`proxy-server-nameserver` 告诉 Clash：“使用这些 DNS 服务器解析代理节点主机名，并返回它们的 **真实 IP**，而非 fake IP。” 这打破了循环。

---

### 修复 2 — 将 Hysteria2 服务器域名添加到 `fake-ip-filter`

作为双重保障，还显式地将您的 Hysteria2 服务器域名从 fake-IP 中排除：

```yaml
dns:
  fake-ip-filter:
    - '*.lan'
    - 'localhost.ptlogin2.qq.com'
    - 'your-hysteria2-server.example.com'   # ← 在此处添加您的实际服务器域名
```

这强制 Clash 即使在 fake-IP 模式下，也为您的代理服务器域名返回 **真实 IP**。

---

### 修复 3 — 为 Hysteria2 服务器的真实 IP 添加 DIRECT 规则

一旦您知道 Hysteria2 服务器的真实 IP（使用 `dig your-hysteria2-domain @223.5.5.5` 获取），在 MATCH 规则 **之前** 添加为 DIRECT 规则：

```yaml
rules:
  - IP-CIDR,192.168.201.0/24,DIRECT
  - IP-CIDR,192.168.1.0/24,DIRECT
  - IP-CIDR,<YOUR_HYSTERIA2_SERVER_REAL_IP>/32,DIRECT  # ← 添加此规则
  # ... 其他规则 ...
  - MATCH,Hysteria2
```

这确保即使 DNS 某种情况下返回真实 IP，前往代理服务器的流量也会走 DIRECT（而非通过自身循环）。

---

## 如何应用修复

```bash
# 1. 编辑您的 Clash 配置
sudo nano /etc/clash/config.yaml
# （或您的配置所在位置 — 使用以下命令检查：ps aux | grep clash）

# 2. 如上所示添加 proxy-server-nameserver 和 fake-ip-filter

# 3. 重启 Clash
sudo systemctl restart clash
# 或
pkill clash && clash -d /etc/clash &

# 4. 验证代理服务器现在解析为真实 IP（非 198.18.x.x）
dig your-hysteria2-domain @192.168.201.1
# ✅ 现在应返回真实的公网 IP，而非 198.18.x.x

# 5. 从笔记本测试
curl https://api.ipify.org
# 应返回您的代理出口 IP
```

---

## 总结诊断表

| 观察到的症状 | 含义 |
|---|---|
| iPad 流量到达 TUN（Meta 上 `tcpdump` 已确认） | ✅ TUN 拦截正常 |
| Clash 日志中仅 UDP，TCP 被静默丢弃 | ✅ Clash 接收 TCP 但无法建立上游连接 |
| Hysteria2 解析为 `198.18.0.28` | ❌ **根本原因** — 代理服务器获得 fake-IP |
| 来自笔记本的代理测试也超时 | ✅ 确认是 Clash 级别的上游问题，而非路由问题 |
| 直接绕过 NAT 也失败 | 因为 Clash 通过 TUN 拦截所有流量，包括绕过尝试 |

`proxy-server-nameserver` 修复是针对此场景的标准方法，并在 Clash Meta/Mihomo 中有文档记录，专门解决“代理服务器域名获得 fake-IP”的问题。

- [Clash Meta DNS config (proxy-server-nameserver)](https://merlinkodo.github.io/Clash-Rev-Doc/config/dns/)
- [Clash fake-IP explanation](https://en.clash.wiki/configuration/dns.html)