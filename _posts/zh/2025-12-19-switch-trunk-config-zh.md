---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 配置交换机Trunk端口
translated: true
type: note
---

问题：哪个命令用于在交换机上将端口配置为 trunk 端口？

答案：

正确答案是 **B) switchport mode trunk**。

### 解释：
- 在 Cisco 交换机（此问题最常见的上下文）上，命令 **switchport mode trunk** 会明确地将接口配置为 trunk 端口，允许其承载多个 VLAN 的流量。
- **A) switchport mode access**: 这将端口配置为 access 端口（仅用于单个 VLAN），与 trunk 相反。
- **C) switchport trunk encapsulation dot1q**: 这指定了 trunk 封装类型 (802.1Q)，但它本身并不能使端口成为 trunk。它在将模式设置为 trunk *之后* 用于支持多种封装类型（例如 ISL 或 dot1q）的旧交换机上。在现代交换机上，802.1Q 通常是默认或唯一的选项。
- **D) switchport access vlan 10**: 这会将特定 VLAN 分配给 access 端口，与 trunk 配置无关。

要完整配置一个基本的 trunk 端口，您通常输入：
```
interface GigabitEthernet0/1
switchport mode trunk
```
根据要求，可能会接着输入封装或允许的 VLAN 列表等附加命令，但 **switchport mode trunk** 是将端口设置为 trunk 模式的核心命令。