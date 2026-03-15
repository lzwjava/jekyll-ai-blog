---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenWrt 路由器设置指南选项
translated: true
type: note
---

**重要：** 因为路由器运行 OpenWrt，您有两种配置选项：

## **Option 1: Router as Simple Client (Recommended)**

保持 OpenWrt 的 `br-lan` 不变（LAN 端口 + WiFi 的桥接）。将其 **WAN interface** 配置为从笔记本电脑获取 DHCP：

1. **在 OpenWrt 上：**
- 转到 Network → Interfaces
- 编辑 **WAN** interface（或创建新的）
- Protocol: **DHCP client**
- Physical interface: 连接到笔记本电脑 USB Ethernet 的端口

2. **结果：**
```
笔记本电脑 (192.168.201.1) → DHCP → OpenWrt WAN → OpenWrt LAN/WiFi 设备
```
- OpenWrt 从笔记本电脑获取类似 `192.168.201.50` 的 IP
- OpenWrt 为其 LAN 设备进行 NAT 流量
- 所有流量通过 Clash proxy 路由

## **Option 2: Router as Switch/Bridge (Advanced)**

将 OpenWrt 转换为桥接模式，让笔记本电脑处理所有路由/DHCP：

1. **在 OpenWrt 上：**
- 禁用 OpenWrt 上的 DHCP server
- 将 USB 连接的端口添加到 `br-lan` 桥接
- 将 OpenWrt LAN IP 设置为静态 `192.168.201.2`（或完全禁用 IP）

2. **结果：**
```
笔记本电脑 (192.168.201.1) → DHCP → 所有设备（有线+无线）
```
- 单一子网 `192.168.201.0/24`
- 笔记本电脑处理所有路由/DHCP/proxy
- OpenWrt 充当哑 AP/switch

## **Which to choose?**

**用于测试/快速设置 → Option 1**
- OpenWrt 改动最小
- 与现有 OpenWrt 配置兼容
- 双重 NAT 但适合 proxy 测试

**用于干净网络 → Option 2**
- 单一子网，无双重 NAT
- 所有设备直接通过 Clash
- 需要更多 OpenWrt 重新配置

## **Current recommendation:**

先尝试 **Option 1**，因为它更简单。在 OpenWrt 上：

1. 将 USB Ethernet 连接到 OpenWrt 的任意 LAN 端口
2. 登录 OpenWrt LuCI（web 界面）
3. Network → Interfaces → 编辑 WAN（或创建新的）
4. Protocol: **DHCP client**
5. Device: 选择连接到笔记本电脑的物理端口
6. Firewall: 分配到 **wan** zone
7. Save & Apply

然后将设备连接到 OpenWrt WiFi/LAN 并测试 `curl https://api.ipify.org`

需要我提供确切的 OpenWrt CLI 命令而不是 web 界面吗？