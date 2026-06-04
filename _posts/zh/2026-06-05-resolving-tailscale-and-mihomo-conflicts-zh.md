---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决Tailscale与Mihomo冲突
translated: true
type: note
---

**问题：** 在中国使用 Tailscale 时，会与 mihomo + hysteria2 + DMIT 产生冲突吗？

**回答：**

是的，可能存在冲突，但通过**适当配置是可以管理的**。以下是具体情况：

---

## 冲突点

### 1. **虚拟网络接口冲突**

Tailscale 和 mihomo 都会创建虚拟网络接口：

- **Tailscale：** 创建 `utun0`（macOS）或 `tun0`（Linux）用于内核模式网络
- **Mihomo：** 创建用于流量拦截的虚拟接口（Linux 上使用 iptables，macOS 上使用 pf）

**结果：** 路由策略冲突、数据包循环或流量丢弃。

### 2. **DNS 冲突**

Mihomo 最近修复了 Tailscale 的 DNS 解析（提交信息：“use our internal DNS resolution logic for tailscale”），但仍存在：

- 两者都尝试重写 DNS 查询
- Tailscale 的 MagicDNS（如果启用）与 mihomo 的 DNS 拦截冲突
- DNS 服务器配置相互矛盾

### 3. **IP 地址范围冲突**

如果其他 VPN 使用了 Tailscale 所使用的 CGNAT 范围（100.64.0.0–100.127.255.255）内的 IP 地址，则会与 Tailscale 的 100.x.y.z 地址产生冲突。

### 4. **流量路由循环**

Mihomo 试图劫持 `100.x.x.x` 流量（Tailscale IP），但不知道如何路由 → 数据包循环或丢弃。

---

## 如何解决（3 种方法）

### **方法一：Tailscale 用户态模式（推荐在中国使用）**

使用 Tailscale 的用户态网络模式来避免与 Tailscale IP 地址的冲突。这样 Tailscale 会在本地（127.0.0.1）暴露一个 SOCKS5 代理，让你可以连接到 Tailscale 网络。

```bash
# 启用用户态网络
tailscale up --tun=userspace
```

然后配置 mihomo，将 Tailscale 流量通过本地 SOCKS5 端口转发：

```yaml
# mihomo config.yaml
port: 7890
socks-port: 7891
mixed-port: 7893
allow-lan: true

proxy-groups:
  - name: "tailscale-proxy"
    type: socks5
    server: 127.0.0.1
    port: 1099  # Tailscale 用户态 SOCKS5 端口

rules:
  # 将 100.x.x.x 流量路由到 Tailscale SOCKS5
  - IP-CIDR,100.64.0.0/10,tailscale-proxy
  - RULE-SET,tailscale,tailscale-proxy
```

**优点：** Tailscale 和 mihomo 不会争夺内核级网络资源。Hysteria2 通过 mihomo 正常传输。

---

### **方法二：混合模式（隧道顺序）**

显式地链式配置它们（针对中国使用场景）：

```
系统流量 → Mihomo (hysteria2 + DMIT) → 如果是 100.x.x.x → Tailscale 用户态 SOCKS5 → 实际目标
```

macOS `~/.config/mihomo/config.yaml`：

```yaml
proxies:
  - name: "hysteria2-dmit"
    type: hysteria2
    server: <dmit-server-ip>
    port: <port>
    auth_str: <password>
    obfs: salamander
    skip-cert-verify: true

proxy-groups:
  - name: "default"
    type: select
    proxies:
      - hysteria2-dmit
      - DIRECT

  - name: "tailscale"
    type: socks5
    server: 127.0.0.1
    port: 1099

rules:
  # Tailscale IP 走 Tailscale 的 SOCKS5
  - IP-CIDR,100.64.0.0/10,tailscale
  # 其他所有流量走 hysteria2
  - MATCH,default
```

---

### **方法三：分流隧道（仅限 Linux）**

如果在 Ubuntu 工作站上使用内核模式，可以用 iptables 将 Tailscale 排除在 mihomo 之外：

```bash
# 让 Tailscale 流量绕过 mihomo
iptables -t mangle -I INPUT -i tailscale0 -j RETURN
iptables -t mangle -I OUTPUT -o tailscale0 -j RETURN
```

这样 mihomo 只拦截非 Tailscale 的流量。

---

## 中国地区的特殊考量

**在中国使用 Tailscale：**

- 用户建议使用 Hysteria2 作为主要隧道来绕过 GFW，因为它专门设计用于规避中国防火墙检测。
- Tailscale + WireGuard 并未被明确封锁，但可能因 QoS 而被降级。
- **更好的方法：** 使用 hysteria2（主要）→ 在隧道内访问 Tailscale 网状网络

**推荐的中国设置：**

```
机器 → Mihomo (hysteria2 到 DMIT 服务器) → 隧道内部：访问 Tailscale 网状网络
```

这样：

1. **Hysteria2 处理 GFW 规避**（你的主要关注点）
2. **Tailscale 运行在 hysteria2 隧道内部**（无冲突）
3. **备用方案：** 如果 P2P Tailscale 失效，hysteria2 中继仍可工作

---

## 实际集成状态

Mihomo 已有针对 Tailscale 兼容性的明确修复（提交信息：“fix netlink permission denied on android for tailscale” 和 “use our internal DNS resolution logic for tailscale”），因此维护人员已经意识到并正在解决冲突。

在 Android 上使用用户态模式时，用户会利用 mihomo 将 Tailscale 的 100.x.x.x 流量路由到端口 1099 的本地代理。

---

## 总结

| 设置 | 冲突？ | 最适合 |
|-------|-----------|----------|
| Mihomo (hysteria2) + Tailscale 内核模式 | **高** | 不要组合使用 |
| Mihomo (hysteria2) + Tailscale 用户态模式 | **无** | 中国使用场景 ✓ |
| Hysteria2 隧道 → 内部使用 Tailscale | **无** | 最高可靠性 |

**针对你的中国设置：** 使用方法一（Tailscale 用户态模式）或先建立 hysteria2 隧道，再在内部运行 Tailscale。完全避免内核模式冲突。

---

**参考：**

- [Tailscale: 与其他 VPN 同时使用](https://tailscale.com/docs/reference/faq/other-vpns)
- [Mihomo Tailscale 修复](https://github.com/MetaCubeX/mihomo/releases)
- [Tailscale + Clash 集成指南](https://blog.l3zc.com/en/2025/04/tailscale-setup-recap/)
