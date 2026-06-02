---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 由于网络分段导致的 SSH 连接失败
translated: true
type: note
---

## Diagnosis Complete: The Real Problem

根据我的诊断，实际情况如下：

### Key Findings

1. **你的 Mac 位于 192.168.1.0/24 网络** (IP: 192.168.1.37)
2. **Router 位于 192.168.2.0/24 网络** (IP: 192.168.2.1)
3. **无 ARP entry** 对应 192.168.2.1（无法直接触达 Router）
4. **Port 22 超时**，即使在没有 Proxy 变量的情况下也是如此
5. **Ping 正常** 是因为它通过 Gateway 192.168.1.1 进行路由

### The Real Issue: Network Segmentation

SSH 失败**与你的 Proxy 无关**。问题在于：

```
Your Mac (192.168.1.37) → Gateway (192.168.1.1) → Router (192.168.2.1)
```

Router 处于 **不同的 Subnet**。当你尝试 SSH 时：

- Ping 正常是因为 ICMP 报文通过 Gateway 进行了路由
- SSH Port 22 在跨越网络边界时被 **Blocked 或不可访问**

### Why Your Proxy Theory Was Wrong

你的 SSH Config 显示：

```
Host !192.168.*.*
    ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

这意味着“除了 192.168.*.* 之外的所有地址都使用 Proxy” —— 因此 192.168.2.1 **本来就不会**经过 Proxy。取反符号 `!` 已经排除了本地网络。

### How to Fix

**Option 1: 直接连接到 Router 的网络**

- 物理连接到 192.168.2.0/24 网络
- 或者配置你的 Gateway 允许 SSH Forwarding

**Option 2: 检查 Router 是否真的开启了 SSH**

```bash
# 首先尝试 telnet (如果 OpenWrt 开启了的话)
telnet 192.168.2.1

# 或者检查 HTTP 管理界面是否正常
curl -I http://192.168.2.1
```

**Option 3: 通过 Gateway 进行 SSH**
如果你的 Gateway (192.168.1.1) 可以触达 Router：

```bash
ssh -J user@192.168.1.1 root@192.168.2.1
```

### Test This Theory

运行以下命令确认 Router 的 Port 22 是否真的无法触达：

```bash
# 这应该也会超时（证明不是 Proxy 的问题）
env -u ALL_PROXY -u HTTP_PROXY -u HTTPS_PROXY \
  nc -zv -w 5 192.168.2.1 22
```

Proxy 环境变量只是个烟雾弹 —— 真正的问题是两个 Subnet 之间的 Network Routing 或 Firewall 设置。
