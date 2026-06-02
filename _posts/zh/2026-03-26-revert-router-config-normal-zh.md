---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将路由器配置还原为普通机器模式
translated: true
type: note
---

当然，这是发生过的事情的完整详细说明：

---

## Session Summary: 将 192.168.1.42 从 Router 恢复为普通主机

### Goal
在 192.168.1.42 (lzwjava-Lenovo-G490) 配置为通过 USB ethernet adapter 给 iPad 做 Router 后，将其重置回普通机器。

### Step 1: SSH Connection
- 需要 `sshpass`，因为服务器 (lzw-server) 没有可以进行交互式密码输入的 ssh-askpass
- 凭据：`lzwjava@192.168.1.42`，密码 `88888888`
- 必须将密码通过管道传给远程端的 `sudo -S`，因为 sudo 也需要交互式身份验证

### Step 2: Discovery (检查哪些部分仍处于 "routerified" 状态)
对你列出的所有配置区域运行了全面审核。结果如下：

| Component | Status |
|---|---|
| IP forwarding | **Enabled** — 包括运行时 (`/proc/sys/net/ipv4/ip_forward = 1`) 和持久化配置 (`/etc/sysctl.conf`) |
| dnsmasq | **Active** — 使用 `/etc/dnsmasq.d/usb-lan.conf` 在 `enx00e04c362f89` 上提供 DHCP (192.168.201.50–150) |
| Clash | **Running** — PID 12975, TPROXY 模式下的 `clash-meta` |
| UFW | 已处于 inactive 状态 — 你之前已经清理过 |
| iptables NAT/FORWARD | 在发现时显示为空 |
| Network interfaces | 主网卡 `enp2s0` 地址为 192.168.1.42, USB adapter `enx00e04c362f89` 处于 DOWN 状态 (未连接 iPad) |
| Netplan | 使用 `renderer: NetworkManager` — 未做更改 |

### Step 3: Reverting (我所做的操作)
使用 `sudo -S` 运行了一条远程命令，执行了以下操作：

1. **Disabled IP forwarding** — 注释掉了 `/etc/sysctl.conf` 中的 `net.ipv4.ip_forward=1`，并将运行时值设为 `0`
2. **Stopped & disabled dnsmasq** — 执行 `systemctl stop/disable dnsmasq`
3. **Removed USB LAN config** — 删除了 `/etc/dnsmasq.d/usb-lan.conf`
4. **Killed Clash** — 执行 `kill 12975`
5. **Flushed iptables** — 执行 `iptables -F`, `iptables -t nat -F`，清空了所有 chains

输出显示这五项操作全部成功。

### Step 4: Machine Went Dark
紧接着，机器停止了响应：
- SSH 连接失败，返回 exit code 255
- Ping 192.168.1.42 显示 100% packet loss
- 在约 2 分钟内的多次重试均告失败

### What Likely Went Wrong
**iptables flush** 可能过于激进了。TPROXY 模式下的 Clash 会通过以下规则挂载到网络栈：
- `TPROXY` 规则用于拦截流量
- `mangle` 表规则用于 packet marking
- 可能还存在 `filter` 表的 INPUT/OUTPUT 规则

当我清空所有 chains (`iptables -F` + `iptables -X`) 时，可能删除了维持主以太网接口 (`enp2s0`) 正常工作所需的规则。如果 Clash 当时正充当系统的 DNS resolver（配置暗示了这一点 — dnsmasq 中有 `no-resolv`，且 Clash 通过 fake-IP 处理 DNS），那么同时 kill 掉它并 flush iptables 可能会导致机器在失去 DNS 的同时路由信息也发生中断。

或者，机器可能由于某些系统反应而直接重启了，目前仍处于 boot 过程中。

### What Was Definitely Fixed
- IP forwarding: **off** ✅
- dnsmasq: **stopped + disabled** ✅
- USB LAN DHCP config: **removed** ✅
- Clash: **killed** ✅

### What Still Needs Verification (待机器恢复后)
- 主以太网接口仍能从 Router (192.168.1.1) 获取 DHCP
- Default route 正确
- 没有残留的 iptables 规则
- NetworkManager 正在正常管理 `enp2s0`
- `enx00e04c362f89` USB adapter 可以被忽略或从配置中移除

### Lesson Learned
应该对 iptables 采取更精确的操作 — 只 flush `nat` 和 `mangle` 表（Clash TPROXY 规则所在处），而不是清除所有内容。虽然 `filter` 表的默认策略 (ACCEPT) 理论上没问题，但 flush 操作可能对 connection tracking 或其他 kernel networking 状态产生了副作用。
