---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VLAN中的端口：物理交换机端口
translated: true
type: note
---

**问题：** 在基于端口的VLAN中，“端口”是什么意思？

**回答：** 在这种情况下，“端口”指的是**网络交换机上的物理插口/连接器**——而不是像TCP端口80或443那样的软件端口。可以把它想象成物理交换机设备背面或面板上的插口——就是插入以太网电缆的那些孔。下面通过一个直观的比较来区分两者的不同：

因此，在VLAN语境中，“端口”始终指交换机上的物理RJ-45插口——插入以太网电缆的孔。每个这样的插口可以分配给一个VLAN，这就是该方法被称为“基于端口”的原因。

这与TCP/UDP端口（如HTTP的80端口或SSH的22端口）完全不同，后者只是标识计算机上运行网络服务的软件编号。这两个含义恰好用了同一个词，但指代的是完全不同的东西。

---

参考资料：

- [什么是交换机端口？ — Cisco](https://www.cisco.com/c/en/us/products/switches/what-is-a-network-switch.html)
- [基于端口的VLAN详解 — NetworkLessons.com](https://networklessons.com/switching/introduction-to-vlans)
