---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenWrt Hysteria2 路由器设置指南
translated: true
type: note
---

**您当前使用旧笔记本电脑运行 Linux Mint 作为网关的实验在技术上是正确的，但操作上很复杂**。您遇到的这些问题（DHCP、DNS 拦截、路由循环、防火墙转发）说明了为什么**通用 Linux 机器作为家用路由器更难维护**。

从系统设计角度来看，您本质上构建了这个架构：

```
iPad
  ↓ USB LAN
Linux Laptop (dnsmasq + NAT + Clash + TUN)
  ↓
WAN
  ↓
Hysteria2 Server (Los Angeles)
  ↓
Global Internet
```

该设计可行，但引入了多项操作难题：

* Linux 防火墙规则（UFW / iptables / nftables）
* DNS 劫持和 fake-IP 处理
* LAN 和 WAN 之间的路由循环
* DHCP 配置
* 设备特定的连接问题（iPad 缓存 DNS）

这些是**路由器问题**，而非应用问题。专用的路由器操作系统如 OpenWrt 正是为此专门构建的。

因此，对于您的目标，最稳定的架构是：

```
Home Devices (iPad / Phone / Laptop)
        ↓ WiFi / LAN
OpenWrt Router
        ↓
Hysteria2 Client (sing-box / PassWall2)
        ↓
Hysteria2 Server (Los Angeles)
        ↓
Global Internet
```

此架构有诸多优势。

---

# 1. 为什么 OpenWrt 通常是更好的解决方案

像 **OpenWrt** 这样的路由器操作系统已经内置：

* DHCP 服务器（dnsmasq）
* DNS 转发
* NAT
* 防火墙区域管理
* LAN/WAN 路由

无需在 Linux 上手动配置所有这些组件，OpenWrt 通过 **LuCI web UI** 提供它们。

主要优势：

### 稳定性

路由器可运行数月无需维护。

### 更简单的网络管理

OpenWrt 自动处理：

* LAN → WAN 转发
* DHCP 租约
* DNS 传播

### 更易集成的代理功能

像 **PassWall2** 或 **OpenClash** 这样的插件集成了代理路由规则。

---

# 2. OpenWrt 中的 Hysteria2 支持

Hysteria2 通常通过 **sing-box** 实现，该引擎受多个 OpenWrt 插件支持。

常见解决方案：

| Plugin              | Engine     | Hysteria2 Support | Notes                |
| ------------------- | ---------- | ----------------- | -------------------- |
| PassWall2           | sing-box   | Yes               | 在中国非常常见 |
| OpenClash           | Clash Meta | Yes               | 强大的规则系统 |
| sing-box standalone | sing-box   | Yes               | 手动配置 |

其中，最直接的方法是：

**PassWall2 + sing-box**

因为它为 Hysteria2 节点提供了直接的 GUI 配置。

---

# 3. 为什么您的笔记本网关设置困难

您的调试总结显示了典型的精确问题：

### 问题 1：DHCP 失败

```
iPad → APIPA 169.254.x.x
```

原因：防火墙阻塞了 DHCP 端口。

路由器通常自动管理 DHCP。

---

### 问题 2：DNS 绕过

您的 iPad 使用了：

```
8.8.8.8
```

而非：

```
Clash DNS
```

这会破坏代理路由。

路由器通常强制执行 DNS 重定向。

---

### 问题 3：路由循环

```
192.168.1.x network
```

在接口之间循环。

路由器实现了正确的**区域隔离**：

```
LAN → WAN
WAN → blocked
```

---

### 问题 4：复杂的防火墙规则

您必须配置：

```
ufw default allow routed
NAT
forward rules
interface rules
```

OpenWrt 使用**防火墙区域**在内部处理这些。

---

# 4. 硬件考虑因素

您的 **2013 Lenovo 笔记本** 性能足够但效率低下：

| Device         | Power Usage |
| -------------- | ----------- |
| Laptop router  | ~20–40W     |
| OpenWrt router | ~5–10W      |

24/7 运行时，笔记本会浪费电力。

---

# 5. 推荐架构

我推荐以下设置：

```
ISP Modem
   ↓
OpenWrt Router
   ↓
PassWall2 / sing-box
   ↓
Hysteria2 Server (Los Angeles)
   ↓
Internet
```

所有设备通过 WiFi 连接到路由器。

无需 USB 网络。

无需手动 DNS。

---

# 6. 典型的 OpenWrt 设置步骤

配置大致如下：

### 步骤 1

安装软件包

```
luci-app-passwall2
sing-box
```

---

### 步骤 2

添加 Hysteria2 服务器节点

参数包括：

```
server address
port
auth string
obfs
TLS
```

---

### 步骤 3

启用透明代理

```
LAN → Proxy
China IP → Direct
Private IP → Direct
```

---

### 步骤 4

启用 DNS 劫持

```
53 → sing-box DNS
```

---

### 步骤 5

启用路由规则

示例：

```
China IP → DIRECT
Apple domains → DIRECT
Global → Hysteria2
```

---

# 7. AI 代理的作用（OpenClaw）

使用像 **OpenClaw** 这样的 AI 代理可以极大帮助，因为 OpenWrt 配置通常涉及：

* 编辑配置文件
* opkg 安装
* 防火墙调整

代理可以自动化任务，如：

```
install passwall
configure sing-box
add hysteria2 node
enable dns hijack
restart firewall
```

这消除了大部分手动工作。

---

# 8. 最终推荐

鉴于您的情况，**最佳路径是**：

1. 使用您的 **OpenWrt 小米路由器**
2. 安装 **PassWall2**
3. 通过 **sing-box** 配置 **Hysteria2**
4. 让路由器处理 DHCP + DNS + NAT

除非您特别需要以下功能，否则避免使用笔记本路由器：

* 实验
* 调试
* 高带宽测试

对于日常家用，基于路由器的架构**更简单且更稳定**。

---

如果您愿意，我也可以解释：

* **2026 年最佳 OpenWrt 代理栈（PassWall2 vs OpenClash vs sing-box）**
* **中国网络的理想规则配置**
* 如何构建**非常可靠的 Hysteria2 家用网关架构**。