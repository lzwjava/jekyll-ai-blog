---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 调试 iPad USB 网络共享失败
translated: true
type: note
---

**问题：** 在通过 Linux 笔记本电脑进行 iPad USB 共享网络设置（DHCP 正常工作，NAT 已激活，DNS 已配置）的情况下，为什么 iPad 仍然无法连接互联网，以及如何系统地调试和修复它？

**回答：**

根据您的设置摘要，一切 *看起来* 在纸面上是正确的——但有几个常见的故障点很容易被忽略。这里是一个从 Layer 2 到 Layer 7 的结构化诊断方法。

---

## 步骤 1：首先验证绝对基础

在 **Linux 笔记本电脑** 上运行这些命令，以确认当前实时状态（磁盘上的配置 ≠ 内存中的配置）：

```bash
# 1. IP 转发当前是否实际开启？
cat /proc/sys/net/ipv4/ip_forward
# 必须返回 1，而不是 0

# 2. iptables FORWARD 链是什么样子？
sudo iptables -L FORWARD -v -n

# 3. NAT MASQUERADE 规则是否实际已加载？
sudo iptables -t nat -L POSTROUTING -v -n

# 4. 确认接口名称（可能已更改！）
ip link show
# 注意：您的 USB 接口（enx00e04c362f89）和 WAN 接口名称
```

如果 `ip_forward` 是 `0`，这本身就会导致一切失败——立即修复：

```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

---

## 步骤 2：检查流量是否实际被转发

使用 `tcpdump` 同时监视两个接口。打开 **两个终端**：

```bash
# 终端 1 — 监视 USB 接口（来自 iPad 的流量）
sudo tcpdump -i enx00e04c362f89 -n not arp

# 终端 2 — 监视 WAN 接口（流出的流量）
sudo tcpdump -i eth0 -n host 8.8.8.8
# （将 eth0 替换为您的实际 WAN 接口）
```

然后从 iPad 尝试访问任何网站。您应该看到：

- **终端 1：** 来自 `192.168.201.136` 的数据包到达
- **终端 2：** 相同的那些数据包出现在 WAN 侧，以笔记本电脑的 IP 作为源地址

如果数据包出现在终端 1 但 **不在** 终端 2 → 转发已损坏（UFW/iptables 问题）。
如果数据包 **两者都不出现** → iPad 根本没有发送流量（检查 iPad 上的默认网关）。

---

## 步骤 3：验证 iPad 的网络设置

在 iPad 上，转到 **设置 → Wi-Fi**（或本次的 USB 网络）。检查：

- **IP 地址：** 应该是 `192.168.201.x`
- **子网掩码：** `255.255.255.0`
- **路由器/网关：** 必须是 `192.168.201.1` ← **这是最常见的故障点**
- **DNS：** 应该是 `192.168.201.1`

如果 **路由器字段为空或错误**，iPad 不知道将流量发送到哪里。这可能发生在 dnsmasq 的 DHCP 未正确发送 `option:router` 时。

验证 dnsmasq 配置：

```bash
# 检查 dnsmasq 是否实际发送网关选项
grep -E "dhcp-option|gateway|router" /etc/dnsmasq.conf
# 应该有类似内容：
# dhcp-option=3,192.168.201.1   ← 网关
# dhcp-option=6,192.168.201.1   ← DNS
```

**强制 iPad 续订 DHCP 租约：** 在 iPad 上，切换飞行模式开启 → 关闭，或转到网络设置并点击“续订租约”。

---

## 步骤 4：使用简单绕过测试（隔离 Clash 为问题）

为了确定是 Clash TUN 问题还是 NAT/路由问题，**临时绕过 Clash**，使用直接 NAT 规则：

```bash
# 添加直接 MASQUERADE，绕过 Clash，使用您的 WAN 接口
sudo iptables -t nat -A POSTROUTING -s 192.168.201.0/24 -o <WAN_INTERFACE> -j MASQUERADE
sudo iptables -A FORWARD -i enx00e04c362f89 -o <WAN_INTERFACE> -j ACCEPT
sudo iptables -A FORWARD -i <WAN_INTERFACE> -o enx00e04c362f89 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

将 `<WAN_INTERFACE>` 替换为您的实际 WAN 接口（例如 `eth0`、`wlan0`、`enp3s0`）。

现在在 iPad 上测试：能否加载 `http://1.1.1.1`？（仅 IP，无需 DNS。）

- **是** → NAT/转发正常；**Clash TUN 是问题**
- **否** → 问题在较低的路由/转发层

---

## 步骤 5：修复 Clash TUN 特定问题

如果 Clash 是瓶颈，检查这些：

### 5a. 确认 Clash TUN 接口已启动

```bash
ip link show | grep -i tun
# 应该显示类似 "utun" 或 "Meta" 的 tun 接口。
ip addr show <tun_interface>
```

### 5b. 验证 Clash 作为 DNS 服务器在监听

```bash
# Clash DNS 应该监听在 192.168.201.1:53
sudo ss -ulnp | grep 53
# 或：
sudo netstat -ulnp | grep 53
```

### 5c. 从笔记本电脑手动测试 DNS（模拟 iPad）

```bash
# 直接查询 Clash DNS — 对于代理域名应返回 fake-IP (198.18.x.x)
dig google.com @192.168.201.1

# 如果返回真实 IP 而非 198.18.x.x，则 fake-IP 模式未工作
```

### 5d. 检查 Clash 配置中的 TUN auto-route

在您的 Clash `config.yaml` 中，TUN 部分必须有：

```yaml
tun:
  enable: true
  stack: system   # 或 "gvisor"
  auto-route: true
  auto-detect-interface: true
  dns-hijack:
    - any:53
```

如果缺少 `auto-route: true`，Clash 不会为转发流量设置路由。

---

## 步骤 6：UFW 规则顺序问题（非常常见）

`sudo ufw default allow routed` 设置 **默认**，但 UFW 可能有链中较早的明确 DENY 规则覆盖它。检查：

```bash
sudo ufw status verbose
sudo iptables -L FORWARD -v -n --line-numbers
```

如果看到针对您的子网的任何 `DROP` 或 `REJECT` 规则，在它们 **之前** 插入明确 ACCEPT 规则：

```bash
sudo iptables -I FORWARD 1 -i enx00e04c362f89 -j ACCEPT
sudo iptables -I FORWARD 2 -o enx00e04c362f89 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

---

## 步骤 7：快速全栈测试序列

一旦认为已修复，从 iPad 或从笔记本电脑模拟运行此序列：

```bash
# 从笔记本电脑，使用 iPad 的 IP 模拟其流量：
# 测试 1：能否到达网关？
ping -I enx00e04c362f89 192.168.201.1

# 测试 2：能否到达互联网上的原始 IP（无需 DNS）？
curl --interface enx00e04c362f89 http://1.1.1.1

# 测试 3：通过 Clash 的 DNS
nslookup google.com 192.168.201.1
# 对于代理目标域名应返回 198.18.x.x (fake-IP)

# 测试 4：完整代理路径
curl --interface enx00e04c362f89 https://api.ipify.org
# 应返回您的代理出口 IP
```

---

## 最可能的根本原因摘要

根据历史，**最可能的剩余问题** 是以下之一：

| # | 可能原因 | 如何确认 |
| --- | --- | --- |
| 1 | iPad 未续订 DHCP（仍使用旧 DNS/网关） | 手动检查 iPad 的网络设置 |
| 2 | Clash 缺少 `auto-route: true` — TUN 未捕获转发数据包 | 检查 Clash 配置 |
| 3 | UFW 有链中较早的明确 FORWARD DROP 规则覆盖 `allow routed` | `sudo iptables -L FORWARD -n --line-numbers` |
| 4 | MASQUERADE 规则中的 WAN 接口名称不匹配 | `ip link show` 验证 |
| 5 | 重启后 `ip_forward` 为 0（未在 sysctl.conf 中持久化） | `cat /proc/sys/net/ipv4/ip_forward` |
