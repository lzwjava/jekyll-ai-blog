---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SNMP：主导网络管理协议
translated: true
type: note
---

问题：在TCP/IP网络中，最广泛使用的网络管理协议是什么？

答案：**SNMP**（简单网络管理协议）

SNMP是TCP/IP网络中占主导地位的网络管理协议。它工作在应用层，使管理员能够从中央系统监控和管理网络设备（路由器、交换机、服务器、打印机等）。其关键组件包括：

- **管理器** – 查询设备的中央系统
- **代理** – 在每个被管理设备上运行的软件
- **MIB**（管理信息库）– 设备参数的结构化数据库

SNMP几乎得到所有网络设备厂商的广泛支持，是网络管理的事实标准。

参考资料：
- [SNMP - Wikipedia](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol)
- [RFC 1157 – 简单网络管理协议](https://www.rfc-editor.org/rfc/rfc1157)