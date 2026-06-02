---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: EIGRP 需要确认的单播数据包
translated: true
type: note
---

问题：哪个 EIGRP 数据包以单播形式发送并需要确认？A) Hello B) Update C) Query D) Reply

答案：

正确答案是 **B) Update**、**C) Query** 和 **D) Reply**——这三者都以**单播**形式发送并需要**显式确认**。只有 **A) Hello** 不符合描述。

以下是关于每种 EIGRP 数据包类型在传输方法和确认方面的全面分析：

| 数据包类型 | 传输方法                     | 是否需要确认？                        | 备注                                                         |
| ---------- | ---------------------------- | ------------------------------------- | ------------------------------------------------------------ |
| **Hello**  | 组播 (224.0.0.10)            | 否                                    | 用于邻居发现和保活。Hello 包是不可靠的（无需 ACK）。       |
| **Update** | 单播（或向多个新邻居发送时组播） | 是 – 需通过 **ACK** 数据包确认      | 携带路由信息。以单播形式发送时（邻居建立后的常态），它是可靠的。 |
| **Query**  | 单播（发送给特定邻居）       | 是 – 需通过 **ACK** 数据包确认      | 当路由丢失时发送，EIGRP 向邻居请求替代路径。始终可靠。      |
| **Reply**  | 单播（回复 Query 的发起者）  | 是 – 需通过 **ACK** 数据包确认      | 对 Query 的响应，包含已知路径（或无路径）。始终可靠。       |
| **ACK**    | 单播                         | 不适用（它本身就是确认）              | 简单的数据包，不含数据，仅用于确认收到 Update/Query/Reply。 |

### EIGRP 可靠传输协议 (RTP) 的关键点

- EIGRP 使用其自身的**可靠传输协议 (RTP)** 来保证某些数据包的传输。
- 包含路由信息或影响路由表的控制信息的数据包 (**Update、Query、Reply**) 是**可靠地**发送的 → 它们总是单播（除了向新邻居的初始 Update），并且需要 **ACK**。
- **Hello** 和 **ACK** 数据包是**不可靠地**发送的（不需要确认）。
- ACK 是一个独立的 EIGRP 数据包（操作码 5），不含数据——仅仅是序列号确认。

### 为什么这个问题可能很棘手

许多练习题会将 **Update** 作为唯一答案，因为它最常见是可靠的单播数据包。然而，从技术上讲，**Update、Query 和 Reply** 都符合以单播形式发送并需要确认的标准。

如果问题强制选择单个答案，并且来自 Cisco 官方资料（例如 CCNP ENARSI），历史上最常见的预期答案是 **B) Update**。

参考资料：

- [Cisco EIGRP 数据包类型](https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/13669-1.html)
- [EIGRP 可靠传输协议 (RFC 7868)](https://datatracker.ietf.org/doc/html/rfc7868)
