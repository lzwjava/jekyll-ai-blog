---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 非管理型交换机缺少配置接口
translated: true
type: note
---

问题：我的 Mercury 5 端口 1000Mbps 交换机（型号 5G105C，深色，5V 0.4A）不像路由器那样工作，也没有用于配置的 IP 地址。它不能通过 192.168.2.1 或类似地址访问吗？

回答：

您的设备是 **Mercury**（或可能是更名后的 **Mercusys**）5 端口 Gigabit 以太网交换机，型号类似于 SG105C、SG105M 或 MS105G。这些是**非网管桌面交换机**，旨在实现简单的即插即用操作。

### 主要特点

- **非网管交换机**：它没有 Web 界面，没有配置页面，也没有可分配的 IP 地址。与路由器（通常使用 192.168.1.1、192.168.0.1 或 192.168.2.1 等地址进行设置）不同，非网管交换机在网络第 2 层运行。它只是在连接的设备之间转发以太网帧，没有任何管理功能。
- **无 IP 地址**：设备本身不获取或使用 IP 地址进行访问。您无法通过浏览器登录或配置 VLAN、端口镜像或 QoS 等设置。
- **电源规格匹配**：许多类似型号（例如 Mercusys MS105G）使用 5V 电源适配器（通常约为 0.6A，但 0.4A 接近且在各种型号中很常见）。
- **行为正常**：它“不像路由器那样工作”，因为它不是路由器——它只是一个基本的交换机，用于扩展您的网络端口并以千兆速度连接多个设备（例如计算机、电视、打印机）。

### 您可以做什么

- 将您的主路由器连接到交换机的一个端口。
- 将其他设备插入剩余端口。
- 一切都应该立即工作——无需设置。

如果您需要高级功能（例如 Web 配置页面），则需要**网管交换机**。

参考资料：

- <https://skit.com.sg/products/mercury-sg105c-5-port-gigabit-ethernet-network-desktop-switch> (Mercury SG105C 被描述为即插即用集线器)
- <https://www.mercusys.com/en/product/details/ms105g/> (Mercusys MS105G：5 端口千兆非网管桌面交换机，即插即用，无需配置)
- <https://www.newegg.com/luom-sg105m-5-x-rj45/p/0XP-018B-00003> (类似的 Mercury SG105M 列为非网管、即插即用)
