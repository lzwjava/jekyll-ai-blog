---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux Mint 代理路由器设置指南
translated: true
type: note
---

**任务摘要：SSH 连接测试 & Linux Mint 代理路由器设置**

**目标：** 测试到 `192.168.1.42` 的 SSH 连接，然后将 Linux Mint 笔记本配置为有线代理路由器，使用内置 Ethernet 作为 WAN 和 USB-Ethernet 作为 LAN，并使用 Clash TUN 透明代理。

---

### **阶段 1：SSH 连接测试**

**初始失败：**

- 首次尝试：`ssh lzwjava@192.168.1.42` 并交互式输入密码 `88888888`
- **问题：** SSH 在密码提示处挂起，超时，收到信号 15（终止）
- **诊断：** 密码可能错误，或 SSH 配置问题

**关键突破：**

- 安装 `sshpass` 以自动化密码传递
- 命令：`sshpass -p '88888888' ssh lzwjava@192.168.1.42 'echo "Connected as $(whoami)"'`
- **结果：** ✅ 成功！密码正确；交互式计时是问题所在

**经验：** 在脚本/自动化中使用 `sshpass` 进行自动化密码认证。

---

### **阶段 2：系统侦察**

**主机详情：**

- OS: Linux Mint 22.3 "Zena" (Ubuntu 24.04 base)
- Kernel: 6.17.0-14-generic
- Hardware: Lenovo G490 笔记本 (2013 年 ThinkPad)
- Network: 内置 Qualcomm Atheros Ethernet (`enp2s0`) 在 `192.168.1.42/24`
- USB Ethernet: 检测为 `enx00e04c362f89` (Realtek 芯片，MAC `00:e0:4c:36:2f:89`)

---

### **阶段 3：路由器配置**

**步骤 1：启用 IP 转发**

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
```

**步骤 2：配置 NAT 伪装**

```bash
iptables -t nat -A POSTROUTING -o enp2s0 -j MASQUERADE
```

- **目的：** 允许 LAN 客户端通过笔记本的 WAN 接口访问互联网
- **接口：** `enp2s0` (内置 Ethernet 面向调制解调器/路由器)

**步骤 3：配置 USB Ethernet 接口**

```bash
nmcli con add type ethernet ifname enx00e04c362f89 con-name usb-lan \
ip4 192.168.201.1/24 gw4 ""
nmcli con up usb-lan
```

- **子网：** `192.168.201.0/24` (不同于 WAN 的 `192.168.1.0/24`)
- **网关：** 无 (此设备即是网关)
- **状态：** 接口 UP 并有 IP 但 DOWN (尚未连接网线)

**步骤 4：安装 & 配置 dnsmasq DHCP 服务器**

**主要困难：**

- 初始 `dnsmasq` 服务启动失败
- **错误：** `failed to create listening socket for port 53: Address already in use`
- **诊断：** `systemd-resolved` 已监听端口 53 (DNS)

**关键突破：**
修改 `/etc/dnsmasq.d/usb-lan.conf`：

```ini
interface=enx00e04c362f89
dhcp-range=192.168.201.50,192.168.201.150,12h
dhcp-option=3,192.168.201.1 # Gateway
dhcp-option=6,192.168.201.1 # DNS
no-resolv
server=8.8.8.8
server=1.1.1.1
port=0 # Disable DNS server
bind-interfaces # Bind only to USB interface
```

**为什么有效：**

- `port=0`：禁用 dnsmasq 的 DNS 功能 (不需要，因为有 systemd-resolved)
- `bind-interfaces`：确保 dnsmasq 仅绑定到 USB Ethernet
- 服务成功启动，仅在 `192.168.201.0/24` 子网提供 DHCP

---

### **阶段 4：Clash 代理安装**

**步骤 1：安装 Clash Meta (mihomo)**

- 从 GitHub 下载最新版本：`mihomo-linux-amd64-compatible-v1.19.21.gz`
- 解压，重命名为 `clash-meta`，安装到 `/usr/local/bin/`
- 验证：`clash-meta -v` 显示 v1.19.21

**步骤 2：创建基本配置**

```yaml
tun:
enable: true
stack: system
dns-hijack:
- any:53
auto-route: true
auto-detect-interface: true
```

- **关键特性：** TUN 模式用于透明代理，auto-route 用于 LAN 流量
- DNS 劫持以将客户端 DNS 查询重定向通过 Clash

**步骤 3：创建 Systemd 服务**

- 服务文件位于 `/etc/systemd/system/clash.service`
- 以 `lzwjava` 用户运行，并带有 `CAP_NET_ADMIN` 权限 (TUN 所需)
- 失败时自动重启

---

### **当前网络架构**

```
[Internet] ←→ [Modem/Router] (192.168.1.1)
↓
[enp2s0] Linux Mint (192.168.1.42)
↓
[Clash TUN] ←→ [iptables NAT]
↓
[enx00e04c362f89] (192.168.201.1)
↓
[USB Ethernet Cable]
↓
[Client Devices] (DHCP: 192.168.201.50-150)
```

---

### **关键设计决策**

1. **分离子网：** WAN (`192.168.1.0/24`) 与 LAN (`192.168.201.0/24`) 防止路由冲突
2. **TUN 优于 REDIR：** 选择 TUN 模式以获得更好透明度 (处理 UDP、ICMP)
3. **dnsmasq 优于 ISC DHCP：** 轻量级，更易配置
4. **dnsmasq 的端口 0：** 避免与 systemd-resolved 冲突，同时保留 DHCP
5. **USB 静态 IP：** 确保一致的网关地址 (`192.168.201.1`)

---

### **剩余待办事项**

1. **物理连接：** 将网线从 USB 适配器插入交换机/客户端
2. **启动 Clash：** `sudo systemctl start clash`
3. **添加代理配置：** 编辑 `~/.config/clash/config.yaml` 并添加实际服务器详情
4. **测试客户端：** 连接设备，验证获取 IP，互联网流量通过代理路由

---

### **潜在性能考虑**

1. **老旧硬件：** 2013 ThinkPad 通过 Clash + 加密可能瓶颈在 ~100-300Mbps
2. **USB 2.0 瓶颈：** USB-Ethernet 适配器理论上限 ~480Mbps
3. **内存：** Clash 使用 ~50-100MB RAM；适用于 4GB+ 系统
4. **CPU：** 如果可用，AES-NI 有助于性能 (3 代 Intel 可能无)

**总时间：** ~22 分钟 (02:12 到 02:34)
**状态：** ✅ 准备好进行物理测试和代理配置
