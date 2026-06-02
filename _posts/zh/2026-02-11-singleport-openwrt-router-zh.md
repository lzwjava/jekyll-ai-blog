---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 单臂 OpenWrt 路由器解决方案
translated: true
type: note
---

Question: 但令人遗憾的是，这台笔记本电脑只有一个 Ethernet 端口，且没有 WiFi。这对将其转变为 OpenWrt 软路由有什么影响，有哪些解决方案？

Answer:

是的，这是许多旧笔记本电脑常见的局限性 —— 只有一个内置 Ethernet 端口（在 OpenWrt 中通常为 eth0）且没有可用的 WiFi 网卡（或者不受 OpenWrt 支持）。这使得仅靠硬件实现独立的 **WAN**（互联网输入）和 **LAN**（家庭网络输出）连接变得有些棘手。

但这仍然是非常可行且被广泛使用的。按照推荐程度（从最简单/最佳开始），以下是实际的解决方案：

### 1. 最佳且最简单：添加一个廉价的 USB Ethernet adapter（强烈推荐）

- 插入一个 USB-to-Ethernet adapter → 现在你就拥有了两个物理端口。
- 将其中一个（内置）分配为 WAN，另一个（USB）分配为 LAN —— 反之亦然。
- 大多数现代 USB 适配器都可以开箱即用，或者只需安装一个软件包。

2026 年流行且可靠的芯片组（具备良好的 OpenWrt 支持）：

- **Realtek RTL8153 / RTL8156** (gigabit) → 安装 `kmod-usb-net-rtl8152`
- **ASIX AX88179** (gigabit USB 3.0)
- **TP-Link UE300 / UE306** (非常常见且便宜，基于 RTL8153)
- 如果你追求 gigabit 速度，请避免使用非常老旧的仅支持 USB 2.0 的适配器。

安装 OpenWrt 后的步骤：

1. 插入 USB 适配器。
2. 通过 SSH 或 LuCI → System → Software → Update lists → 搜索并安装驱动（例如 `kmod-usb-net-rtl8152` 或 `kmod-usb-net-asix`）。
3. 重启或热插拔 —— 新的 interface 就会出现（例如 eth1）。
4. Network → Interfaces → Add new interface：
   - Name: wan (或 lan)
   - Protocol: DHCP client (用于 WAN) 或 static 192.168.1.1/24 (用于 LAN)
   - Physical: 选择新的 eth1 (或出现的对应网口)
5. Firewall → 分配到 wan zone (input/reject, forward/reject, masq on) 或 lan zone。
6. 完成 —— 现在的 WAN 在一个端口，LAN 在另一个端口。将 modem/ISP 接到 WAN 口，switch/设备接到 LAN 口。

这能以较低的开销提供完整的路由器功能（NAT, firewall, OpenClash/Clash, SQM 等），并达到 gigabit 速度。

### 2. 在单端口上使用 VLANs + 网管型交换机（更进阶，无需额外硬件）

如果你不想购买额外的适配器：

- 使用一台 **managed/VLAN-capable switch**（网管交换机，例如廉价的 TP-Link TL-SG108E，约 20-30 美元）。
- 在单个 Ethernet 端口上配置两个 VLAN：
  - VLAN 10 = WAN
  - VLAN 1 = LAN (默认)
- 在交换机（switch）上：
  - Port 1 (连接 modem/ISP) → tagged VLAN 10
  - Port 2 (连接笔记本单口) → trunk/tagged VLAN 1 + 10
  - Ports 3-8 → untagged VLAN 1 (你的 LAN 设备)
- 在 OpenWrt 中：
  - 在 eth0 上创建 VLAN 接口（例如 eth0.10 用于 WAN，eth0.1 用于 LAN）
  - 将 eth0.10 分配给 wan 接口 (DHCP client)
  - 将 eth0.1 (或 br-lan) 分配给 lan bridge (192.168.1.1)

这种方案效果很好，但需要一台支持 VLAN 的交换机和更复杂的配置（通过 LuCI：Network → Switch → 添加 VLANs）。适合不需要 USB 设备的整洁方案。

### 3. 临时 / 受限方案（不推荐作为完整路由器）

- **仅将内置端口作为 LAN 使用** → 将笔记本 Ethernet 连接到现有路由器的 LAN 端口。OpenWrt 充当 AP / 旁路由 (proxy box) / 广告拦截器（无 NAT，无完整路由功能）。
- **WiFi as WAN**（如果网卡可用）→ 但你提到了没有 WiFi。
- **USB WiFi adapter 作为 AP** → 购买 OpenWrt 支持的 USB WiFi 适配器（例如 mt7921u 芯片组），作为无线 LAN AP 使用，有线端口作为 WAN。但 USB WiFi 通常没有内置网卡稳定或强大。

### 总结

- **购买一个 $10-25 的 USB gigabit Ethernet adapter** → 这是实现标准双口路由器最简单的路径。
- 你的 i5 + 8GB 笔记本在性能上（VPN/proxy 吞吐量、多客户端处理、软件包运行）仍然会碾压大多数家用路由器。
- 没有 WiFi？你稍后可以添加一个优质的 USB WiFi 适配器作为无线 AP（或者临时使用手机网络共享）。

在中国和其他地区，许多人正是使用这种配置（旧笔记本 + USB 网卡）作为家庭路由/代理的日常主力设备。

References:

- [OpenWrt Wiki - Single-Port Devices / VLAN setup](https://openwrt.org/docs/guide-user/network/singleportrouter)
- [OpenWrt Forum - USB Ethernet adapter drivers discussion](https://forum.openwrt.org/t/usb-2-0-to-ethernet-adapter-driver-for-openwrt/185891)
- [OpenWrt single ethernet port VLAN tutorial video reference](https://www.youtube.com/watch?v=aqvbAQmAbAU)
- [Common USB adapters for OpenWrt (TP-Link UE300 etc.)](https://nelsonslog.wordpress.com/2022/04/21/openwrt-on-raspberry-pi-4)
