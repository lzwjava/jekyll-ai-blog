---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 带有标签的帧在访问端口的处理方式
translated: true
type: note
---

Question: Access port 如何处理带有 VLAN-tagged 的数据帧？

Answer:

交换机上的 **access port** 旨在连接终端设备（如 PC、打印机、IP 电话），并且属于单个 VLAN（配置为 access VLAN）。它在该 VLAN 中以 **untagged** 模式运行。

当 access port 接收到数据帧时：

- 如果数据帧是 **untagged** 的，交换机会在内部添加配置的 access VLAN tag，并将其转发到相应的 VLAN。
- 如果数据帧带有 **VLAN-tagged**（即已经包含 802.1Q tag），在大多数交换机（包括 Cisco）上的默认和标准行为是 **drop（丢弃）该 tagged 帧**。这是因为 access port 预期来自不自行标记帧的终端设备的流量，接收到 tagged 帧通常意味着配置错误或潜在的安全问题。

因此，正确答案是 **D) It drops all tagged frames**。

选项 A、B 和 C 对于 access port 是错误的：

- A) Forwarding unchanged 意味着将其视为 trunk port。
- B) Adding a tag 仅针对输入的 untagged 帧。
- C) Removing the tag (stripping) 发生在 **egress**（出站）时，即通过 access port 向 untagged 设备发送帧时，而不是在 ingress（入站）时。

此行为在 IEEE 802.1Q 中定义，并由 Cisco、Juniper 和 Arista 等主要厂商一致实现。
