---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Clash 代理 DNS 设置选项
translated: true
type: note
---

问题：在 Linux Mint 代理路由器设置中使用 Clash TUN 时，我们需要停止 `systemd-resolved` 服务吗？

回答：

## 简短回答：**不需要停止它——但根据你的目标，你有选项。**

你的当前工作设置已经证明了这一点：Clash 正在运行，代理正常工作，`systemd-resolved` 为笔记本电脑本身处理 DNS。冲突已经通过在 Clash 配置中设置 `dns: enable: false` 和 dnsmasq 中的 `port=0` 解决了。

---

## 理解你的设置中的角色

| 组件 | 角色 |
|---|---|
| `systemd-resolved` | 为 **笔记本电脑本身** 处理 DNS（`127.0.0.53` 上的端口 53） |
| `dnsmasq` | 为 LAN 客户端提供 **仅 DHCP**（`port=0` 禁用其 DNS） |
| `Clash TUN` | 拦截并代理流量（包括通过 `dns-hijack: any:53` 的 DNS） |

---

## 三种方法

### ✅ 选项 1：保留 systemd-resolved（你的当前设置——推荐）

这就是你已经在做的，而且它有效：

- `systemd-resolved` 为 **笔记本电脑自身的进程** 处理 DNS
- Clash 通过 TUN 从 **LAN 客户端** 劫持 DNS（`dns-hijack: any:53`）
- dnsmasq 仅处理 DHCP（`port=0`）
- **无冲突，不会中断笔记本电脑自身的连接**

**何时选择此选项：** 你仍然正常使用笔记本电脑（浏览、SSH 等），并且需要它为自己解析 DNS。

---

### ⚠️ 选项 2：禁用 DNS Stub Listener（中间方案）

DNS stub listener 是 `systemd-resolved` 内置的一个轻量级 DNS 服务器，在 `127.0.0.53` 的端口 53 上监听 DNS 查询。你可以仅禁用 stub listener，而不停止完整服务。

编辑 `/etc/systemd/resolved.conf`：
```ini
[Resolve]
DNSStubListener=no
```
然后：
```bash
sudo systemctl restart systemd-resolved
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

这会完全释放端口 53，同时保留 `systemd-resolved` 的缓存和上游转发功能。如果希望 dnsmasq 也为客户端提供 DNS，则此选项很有用。

---

### 🔴 选项 3：完全禁用 systemd-resolved（仅路由器模式）

你可以使用 `sudo systemctl disable systemd-resolved` 和 `sudo systemctl stop systemd-resolved` 完全禁用它，然后手动将 `/etc/resolv.conf` 设置为静态 nameserver，如 `8.8.8.8`。

```bash
sudo systemctl disable systemd-resolved
sudo systemctl stop systemd-resolved
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**何时选择此选项：** 笔记本电脑是 **专用的无头路由器**——你不将其用作桌面，并且希望 dnsmasq 完全为 LAN 处理所有 DNS。

**风险：** 如果 Clash 或你的代理宕机，笔记本电脑本身将完全丢失 DNS 解析，除非你有备用方案。

---

## 对你的情况的推荐

由于你的设置 **已经正常工作**，并且 `systemd-resolved` 正在运行：

> ✅ **保持原状。** dnsmasq 中的 `port=0` 和 Clash 中的 `dns: enable: false` 已经避免了所有冲突。停止 `systemd-resolved` 是多余的，并且如果 Clash 宕机，可能会破坏笔记本电脑自身的 DNS。

唯一需要禁用它的场景是，如果你希望 dnsmasq 为 LAN 客户端提供 **DHCP 和 DNS**（例如，用于自定义域名过滤或 split DNS）。在这种情况下，选择 **选项 2**（仅禁用 stub listener），而不是完全停止。

参考资料：

- [How to Avoid Conflicts Between dnsmasq and systemd-resolved – Baeldung](https://www.baeldung.com/linux/dnsmasq-systemd-resolved-conflicts)
- [Install and Configure Dnsmasq on Ubuntu – ComputingForGeeks](https://computingforgeeks.com/install-and-configure-dnsmasq-on-ubuntu/)
- [systemd-resolved – ArchWiki](https://wiki.archlinux.org/title/Systemd-resolved)
