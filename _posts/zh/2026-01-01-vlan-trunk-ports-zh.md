---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 深入理解 VLAN Trunk 端口
translated: true
type: note
---

Question: 哪种类型的 switch port 允许通过多个 VLAN？
A) Access port
B) Trunk port
C) Hybrid port
D) Console port

Answer: 

正确答案是 **B) Trunk port**。

- **Access port**: 配置为仅属于单个 VLAN。它承载一个 VLAN 的流量，通常用于连接计算机或打印机等终端设备。发送和接收的是 Untagged frames。
- **Trunk port**: 旨在同时承载多个 VLAN 的流量。它使用 tagging（通常是 802.1Q）来识别每个 frame 属于哪个 VLAN，从而允许 VLAN 扩展到多个 switches。
- **Hybrid port**: 在某些 switches（例如 Huawei）上发现的一种私有模式，可以处理多个 VLAN 的 tagged 和 untagged 流量，但它不是跨厂商对该功能的标准术语。
- **Console port**: 一种管理端口，用于通过 serial connection 进行 out-of-band 配置；它不承载网络流量或 VLAN。

在标准 networking（例如 Cisco）中，允许通过多个 VLAN 的端口类型是 **trunk port**。