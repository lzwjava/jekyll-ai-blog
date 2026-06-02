---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复代理引起的 SSH 挂起问题
translated: true
type: note
---

问题：为什么我的 SSH 连接 OpenWrt 路由器（192.168.2.1）会卡死（停留在 "Connecting to..."），而 ping 却是正常的，该如何修复？

回答：

## 根本原因：你的 HTTP/HTTPS Proxy 拦截了 SSH

仔细观察你的终端输出，最关键的证据就在开头：

```
🚀 Proxy Settings Detected:
  - HTTP_PROXY: http://127.0.0.1:7890
  - HTTPS_PROXY: http://127.0.0.1:7890
```

SSH 使用 TCP port 22。当设置了 `HTTP_PROXY` 或 `HTTPS_PROXY` 环境变量时，某些 Proxy 工具（如运行在 7890 端口的 Clash、V2Ray、Shadowsocks 客户端）会拦截**所有传出的 TCP 连接**，包括 SSH。Proxy 尝试通过 HTTP CONNECT 隧道转发你的 SSH 连接，但目标 `192.168.2.1` 是私有 LAN IP，导致 Proxy 要么**拒绝连接**，要么**无法路由**，或者干脆**卡死**。

Ping (ICMP) 不受影响，因为 ICMP 不是 TCP，Proxy 不会处理它——这正是为什么 ping 正常但 SSH 不通的原因。

---

## 修复方案

### ✅ 方案 1：针对私有/LAN IPs 绕过 Proxy（最佳长期方案）

添加 `NO_PROXY` 来排除所有私有网段：

```bash
export NO_PROXY="localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12"
```

然后重试 SSH：

```bash
ssh root@192.168.2.1
```

若要永久生效，请将该 export 语句添加到你的 `~/.zshrc` 或 `~/.bashrc` 中。

---

### ✅ 方案 2：仅为此 SSH 命令临时取消 Proxy 变量

```bash
env -u HTTP_PROXY -u HTTPS_PROXY ssh root@192.168.2.1
```

这会在不改变当前环境的情况下，临时清除该命令的 Proxy 设置。

---

### ✅ 方案 3：在 `~/.ssh/config` 中使用 `ProxyCommand none`

你的 SSH config 中已经有一个为所有 Host 应用选项的 `*` 模块。请为你的路由器添加一个特定的覆盖规则：

```
Host 192.168.2.1
    ProxyCommand none
    User root
```

这会告知 SSH 直接连接，绕过任何可能设置的 ProxyCommand。

---

### ✅ 方案 4：配置你的 Proxy 应用绕过 LAN

如果你使用的是 **Clash**, **V2Ray**, **Mihomo** 或类似工具（7890 端口通常是 Clash）：

打开 Proxy 应用的配置并添加 LAN bypass 规则。以 Clash 为例：

```yaml
bypass:
  - localhost
  - 127.*
  - 10.*
  - 172.16.*
  - 192.168.*
  - "*.local"
```

如果你希望所有工具（SSH, curl 等）都能自动绕过 LAN 地址的 Proxy，这是最彻底的解决办法。

---

## 为什么你的 SSH Config 让情况变得更糟

根据你的 verbose 输出：

```
debug1: /Users/lzwjava/.ssh/config line 4: Skipping Host block because of negated match for 192.168.*.*
debug1: /Users/lzwjava/.ssh/config line 6: Applying options for *
```

你在 SSH config 中设置了一个否定规则 `!192.168.*.*`，接着是一个通配符 `*` 模块。这个 `*` 模块很可能设置了 `ProxyCommand` 或相关的 Proxy 选项（这在配置 SSH 通过 SOCKS Proxy 连接所有主机时很常见）。由于匹配到了通配符规则，它被应用到了 `192.168.2.1`，导致 SSH 握手通过你的 Proxy 进行。

**永久解决方案**（结合以上两个问题）：

```
# ~/.ssh/config

# 为所有 LAN 地址绕过 Proxy
Host 192.168.* 10.* 172.16.*
    ProxyCommand none
    ServerAliveInterval 30

# 你原有的通配符配置（包含 Proxy 设置）放在下方
Host *
    ...你现有的选项...
```

---

## 快速总结

| 症状 | 原因 |
|---|---|
| Ping 正常 | ICMP 绕过了 HTTP Proxy |
| SSH 卡在 "Connecting to" | Proxy 拦截了 TCP/22，且无法到达 LAN IP |
| 无错误提示，只是卡死 | Proxy 静默失败或等待超时 |

**TL;DR** —— 运行 `env -u HTTP_PROXY -u HTTPS_PROXY ssh root@192.168.2.1` 来确认这是否是原因。如果能立即连接，请添加永久的 `NO_PROXY` 或修复你的 `~/.ssh/config`。

参考资料：

- [https://discussions.apple.com/thread/255263733](https://discussions.apple.com/thread/255263733)
- [https://www.theregister.com/2020/04/01/apples_macos_catalina_ssh/](https://www.theregister.com/2020/04/01/apples_macos_catalina_ssh/)
