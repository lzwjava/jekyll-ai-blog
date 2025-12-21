---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: iPhone 和 Mac 上的 DHCP 问题
translated: true
type: note
---

问题：通过适配器/转换器将 iPhone 和 Mac 连接到 5 端口的 Mercury 以太网交换机，然后该交换机连接到路由器时，DHCP 在哪些情况下会失败？为什么连接顺序很重要（例如，需要在断开 Mac 连接后先连接 iPhone）？

答案：

您的设置中，iPhone（可能通过 USB-C/Lightning 转以太网适配器）和 Mac（通过 Thunderbolt/USB-C 转以太网适配器）都连接到一个 5 端口的非网管型以太网交换机（可能是 Mercusys 或类似的入门级品牌交换机），交换机的一个端口上行连接到您的路由器。路由器充当 DHCP 服务器，为网络上的设备分配 IP 地址。

间歇性的 DHCP 问题，即一个设备（通常是 iPhone）无法获取 IP 地址，除非以特定的顺序连接，通常是由以下原因之一造成的：

### 1. **交换机中的 ARP 缓存或 MAC 地址表问题**
   - 非网管型交换机维护 MAC 地址表以高效转发流量。
   - 如果 Mac 首先连接，交换机将在上行端口（朝向路由器）学习 Mac 的以太网 MAC 地址。
   - 当 iPhone 随后连接并发送 DHCP 请求（广播）时，交换机可能会根据过时的条目错误地转发它，或者可能存在 ARP 解析冲突。
   - 路由器的 ARP 表也可能缓存第一个设备的 MAC 地址，导致它忽略或未能正确响应第二个设备的请求。
   - 反转顺序（iPhone 先连接）暂时有效，因为它会清除或更新 iPhone MAC 地址的缓存。

### 2. **路由器 DHCP 服务器限制或 Bug**
   - 某些家用路由器（特别是 ISP 提供的路由器）存在一些怪癖，它们将网络与第一个连接设备的 MAC 地址关联起来。
   - 类似于某些供应商报告的“仅限调制解调器”模式问题，DHCP 服务器可能只在重新启动或重新排序之前，可靠地为交换机后面的一个设备分配地址。
   - Apple 设备（iPhone 和 Mac）似乎更容易出现这种情况，因为 iOS/macOS 处理通过 USB 以太网适配器发出的 DHCP 请求的方式。

### 3. **适配器特定的行为**
   - Apple 设备上的基于 USB 的以太网适配器有时会导致 DHCP 协商延迟或失败，尤其是当多个适配器都位于交换机后面时。
   - 曾有报道称，诸如 ARP 解析缓慢或适配器未按特定顺序插入就无法完全初始化等问题。

### 推荐修复方法
- **重启路由器和交换机电源**：拔掉两者的电源 30 秒，然后重新连接。这会清除 ARP/MAC 表。
- **手动续订 DHCP 租约**：
  - 在 Mac 上：系统设置 > 网络 > 以太网 > 详细信息 > 续租 DHCP。
  - 在 iPhone 上：设置 > 以太网 > 续租（或切换以太网开关）。
- **尝试不同的连接顺序或端口**：测试交换机上的线缆/端口。
- **暂时使用静态 IP**：在路由器的 IP 范围（例如 192.168.1.x）中手动分配 IP，以测试在没有 DHCP 的情况下是否可以连接。
- **最佳长期解决方案**：如果可能，将路由器直接连接到一台设备，或者添加一个更好的交换机/路由器。如果您的路由器支持，请在其 DHCP 设置中通过 MAC 地址保留 IP。
- **切换设备时重启路由器**：这可以可靠地重置缓存。

这种行为是某些与交换机和 USB 以太网适配器（尤其是 Apple 设备）相关的家庭网络中已知的怪癖。

参考文献：

- https://apple.stackexchange.com/questions/317888/apple-usb-ethernet-adapter-has-a-self-assigned-ip-address-and-will-not-be-able-t
- https://discussions.apple.com/thread/6497865
- https://apple.stackexchange.com/questions/297328/my-mac-wont-connect-with-ethernet-but-will-to-wireless
- https://forums.tomshardware.com/threads/can-dhcp-be-effected-by-a-network-switch.3696191/
- https://serverfault.com/questions/161225/router-dhcp-not-working-with-switch