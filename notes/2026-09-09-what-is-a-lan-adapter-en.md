---
audio: false
generated: true
image: false
lang: en
layout: post
title: What Is a LAN Adapter
translated: false
type: note
---

**Question:** What is 局域网适配器 (LAN Adapter)?

**Answer:**

**局域网适配器** literally translates to **LAN Adapter** (Local Area Network Adapter). It refers to a **network adapter** (also called a network interface card / NIC) that connects your computer to a local area network.

In Windows, this term commonly appears in:

- **`ipconfig`** command output — where you see sections like `以太网适配器 局域网连接` (Ethernet adapter Local Area Connection)
- **Device Manager** under "Network Adapters"
- **Network Connections** settings panel

**Key concepts:**

| Term | Meaning |
| --- | --- |
| 局域网 (LAN) | Local Area Network |
| 适配器 (Adapter) | Hardware/software interface component |
| 局域网适配器 | The NIC that connects your PC to a LAN (typically via Ethernet cable) |

A network adapter is the hardware and software component that connects your computer to the internet or other networks. Most computers have at least one built-in Ethernet (wired) adapter and possibly a wireless (Wi-Fi) adapter.

In Windows `ipconfig` output, you'll typically see entries like:

```
以太网适配器 局域网连接:
   IPv4 地址 . . . . . : 192.168.1.100
   子网掩码  . . . . . : 255.255.255.0
   默认网关. . . . . . : 192.168.1.1
```

This is simply showing your **wired Ethernet (LAN) adapter's** IP configuration.

**References:**

- [How to Configure Network Adapters in Windows](https://techlasi.com/savvy/how-to-configure-network-adapters-in-windows/)
- [Managing Network Adapters – Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/win32/iphlp/managing-network-adapters)
