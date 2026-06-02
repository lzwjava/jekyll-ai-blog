---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 传输层数据传输模式
translated: true
type: note
---

Question: transport layer 在两个 transport entities 之间的数据传输服务模式是什么？

Answer:

正确答案是 **B**。

**解释：**
transport layer 的主要任务是在两个端系统（transport entities）之间提供可靠或不可靠的数据传输服务。

- **Full-Duplex Service**：在大多数标准网络场景中（如 TCP connections），transport layer 以 **full-duplex** 模式运行。这意味着两个实体可以同时发送和接收用户数据和控制数据。这是默认且最常见的配置。
- **Half-Duplex Service**：虽然在现代通用协议如 TCP 中不太常见，但在特定上下文或专用协议中，通信可能被限制为 **half-duplex**（数据一次只在一个方向流动）。因此，表述为“一般为 full-duplex，但在个别情况下可以是 half-duplex”准确反映了该层的灵活性和典型操作。

选项 A 和 C 错误，因为它们使用了绝对术语（“only”），没有考虑到协议实现的多样性和特定用例。选项 D 错误，因为选项 B 提供了有效的描述。

References:
