---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TPROXY DNS 冲突详解
translated: true
type: note
---

**问题：** 在 Clash TPROXY 设置中，我们可以设置 `dns: enable: false` 并使用 `systemd-resolved` 代替吗？

**答案：**

简短回答：**技术上是的，但这会破坏基于域名的路由规则。** 原因如下。

---

## 为什么在 TPROXY 模式下不能简单禁用 Clash DNS

### 核心问题：TPROXY 看到的是 IP，而不是域名

当 iPad 流量到达 TPROXY 端口时，Clash 只看到带有 **IP addresses** 的原始 TCP/UDP 数据包。它不知道最初请求的域名。例如：

```
Clash sees:  192.168.201.136:54321 → 142.250.80.46:443
Clash needs: "this is google.com → route via proxy"
```

如果没有自己的 DNS 拦截原始查询，Clash **无法匹配基于域名的规则**，例如：
```yaml
- DOMAIN-SUFFIX,google.com,Proxy
- DOMAIN-SUFFIX,baidu.com,DIRECT
- GEOSITE,cn,DIRECT
```

DNS 查询通过 UDP 发送，无法通过标准的 iptables 规则重定向，这可能导致不正确的结果。这就是为什么使用 Clash 的内置 DNS 来替换 systemd-resolved —— 它记住从域名到 IP 的映射，因此 Clash 知道重定向连接的域名，并可以应用与域名相关的规则。

---

## 各种场景下会发生什么

### 场景 A：`dns: enable: false` + systemd-resolved

```
iPad → DNS query → systemd-resolved → returns real IP (e.g. 142.250.80.46)
iPad → connects to 142.250.80.46:443
iptables TPROXY → Clash receives packet
Clash: "What domain is this? I don't know." → can only match by IP/GEOIP
→ Domain rules like DOMAIN-SUFFIX,google.com ALL FAIL
→ Only IP-CIDR and GEOIP rules still work
```

你的代理路由变得非常粗糙——一切要么走 DIRECT 要么 PROXY，没有域名级控制。

### 场景 B：`dns: enable: true` + Clash DNS（当前推荐）

```
iPad → DNS query → Clash DNS (port 53) → Clash records "198.18.0.5 = google.com"
iPad → connects to 198.18.0.5:443 (real IP in redir-host mode)
iptables TPROXY → Clash receives packet
Clash: "I know 142.250.80.46 = google.com" → matches DOMAIN rules correctly
→ Full domain-based rule matching works ✅
```

---

## 端口 53 冲突问题

人们想要禁用 Clash DNS 的真正原因是 **systemd-resolved 已经占用了端口 53**，导致 Clash 无法启动。在 Clash 的 DNS 模块工作之前，你可能需要杀死 systemd-resolved 和任何占用 UDP 端口 53 的其他进程。

正确的修复**不是**禁用 Clash DNS，而是释放端口 53：

```bash
# Stop systemd-resolved from occupying port 53
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved

# Point resolv.conf to Clash directly
sudo rm /etc/resolv.conf
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf

# Now Clash can listen on 0.0.0.0:53
```

或者，更优雅的方法——让 Clash 监听 `127.0.0.53:53`（systemd-resolved 使用的确切地址），然后将 systemd-resolved 的上游指向 Clash：

```yaml
# Clash config: listen on systemd-resolved's stub address
dns:
  enable: true
  listen: 127.0.0.53:53     # takes over systemd-resolved's slot
  enhanced-mode: redir-host
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
```

配置 Clash 监听 `127.0.0.53:53` 后，使用 dnsmasq 作为 DNS 缓存层，`server=127.0.0.53` 指向 Clash，并将 `/etc/resolv.conf` 设置为使用 dnsmasq 作为本地解析器。

---

## 决策树：何时可以禁用 Clash DNS？

| 你的规则 | 可以禁用 Clash DNS 吗？ |
|---|---|
| 仅 `IP-CIDR` 和 `GEOIP` 规则 | ✅ 是的，工作正常 |
| `DOMAIN-SUFFIX`、`DOMAIN-KEYWORD` 规则 | ❌ 否，域名匹配会中断 |
| `GEOSITE` 规则（例如 `cn` 站点 DIRECT） | ❌ 否，GEOSITE 需要域名数据 |
| 仅 `MATCH` 捕获所有 | ✅ 是的（一切走一个代理） |

对于你的用例（中国站点 DIRECT，其他一切通过 Hysteria2），你**必须保持 Clash DNS 启用**，因为你依赖基于域名的路由决策。

---

## 推荐设置（干净地避免端口冲突）

```bash
# 1. Disable systemd-resolved stub listener (but keep the service)
sudo mkdir -p /etc/systemd/resolved.conf.d/
sudo tee /etc/systemd/resolved.conf.d/no-stub.conf << EOF
[Resolve]
DNSStubListener=no
EOF
sudo systemctl restart systemd-resolved

# 2. Now Clash can freely take port 53
# In Clash config:
# dns:
#   enable: true
#   listen: 0.0.0.0:53
```

这保持 systemd-resolved 运行（用于笔记本电脑自身的名称解析），但让 Clash 拥有端口 53 用于面向 iPad 的接口。

引用：

- [Setup Clash TPROXY on Linux Router - DEV Community](https://dev.to/jysperm/setup-clash-redir-proxy-on-a-linux-router-4jnh)
- [Clash as TPROXY Gateway - GitHub Gist](https://gist.github.com/phlinhng/38a141862de775b10c613f7f2c6ade99)
- [systemd-resolved - ArchWiki](https://wiki.archlinux.org/title/Systemd-resolved)
