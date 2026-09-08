---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 什么是局域网适配器
translated: true
type: note
---

**问题：** 什么是局域网适配器 (LAN Adapter)？

**答案：**

**局域网适配器** 直译为 **LAN Adapter**（Local Area Network Adapter）。它指的是将计算机连接到局域网的一种**网络适配器**（也称为网络接口卡 / NIC）。

在 Windows 中，该术语通常出现在以下位置：

- **`ipconfig`** 命令输出 — 你会看到类似 `以太网适配器 局域网连接`（Ethernet adapter Local Area Connection）的部分
- **设备管理器**中的“网络适配器”下
- **网络连接**设置面板

**关键概念：**

| 术语 | 含义 |
| --- | --- |
| 局域网 (LAN) | 局域网（Local Area Network） |
| 适配器 (Adapter) | 硬件/软件接口组件 |
| 局域网适配器 | 将电脑连接到局域网（通常通过以太网线缆）的网络接口卡（NIC） |

网络适配器是将计算机连接到互联网或其他网络的硬件和软件组件。大多数计算机至少有一个内置的以太网（有线）适配器，可能还有一个无线（Wi-Fi）适配器。

在 Windows `ipconfig` 输出中，你通常会看到类似这样的条目：

```
以太网适配器 局域网连接:
   IPv4 地址 . . . . . : 192.168.1.100
   子网掩码  . . . . . : 255.255.255.0
   默认网关. . . . . . : 192.168.1.1
```

这只是显示你的**有线以太网（LAN）适配器**的 IP 配置。

**参考资料：**

- [如何在 Windows 中配置网络适配器](https://techlasi.com/savvy/how-to-configure-network-adapters-in-windows/)
- [管理网络适配器 – Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/win32/iphlp/managing-network-adapters)
