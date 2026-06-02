---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: BGP 已建立状态解释
translated: true
type: note
---

问题：哪个 BGP 邻居状态指示 TCP 三次握手已完成？
A) Idle
B) Connect
C) Active
D) Established

答案：

正确答案是 **D) Established**。

### BGP 邻居状态的全面解释

BGP 通过可靠的 TCP 连接（端口 179）建立邻居关系（对等）。在交换任何 BGP 路由信息之前，两台路由器必须首先建立 TCP 会话。BGP 有限状态机 (FSM) 通过六个主要状态跟踪此邻居关系的进度：

| 状态        | 描述                                                                                              | TCP 会话状态                          |
|-------------|----------------------------------------------------------------------------------------------------------|---------------------------------------------|
| **Idle**    | 初始状态。BGP 正在等待 Start 事件（手动或自动）。尚未分配任何资源。               | 未尝试 TCP 连接                 |
| **Connect** | BGP 正在等待 TCP 三次握手完成。本地路由器已向邻居发起 TCP 连接。       | TCP SYN 已发送，等待 SYN-ACK           |
| **Active**  | TCP 连接尝试失败（例如，在 Connect 状态中超时）。BGP 正在通过重复发起新连接来主动尝试建立 TCP。 | 尝试建立 TCP（重新发送 SYN）    |
| **OpenSent**| TCP 三次握手已完成。BGP 已发送 OPENP 消息并正在等待对等方的 OPEN 消息。 | TCP 会话已完全建立               |
| **OpenConfirm** | 收到对等方发送的有效 OPEN 消息，发送 KEEPALIVE，并正在等待对等方发送的 KEEPALIVE。 | TCP 会话已完全建立               |
| **Established** | 收到对等方的 KEEPALIVE。BGP 对等已完全建立。现在可以交换 UPDATE、KEEPALIVE 和 NOTIFICATION 消息。 | TCP 会话已完全建立               |

### 关键点
TCP 三次握手（SYN → SYN-ACK → ACK）必须成功完成，BGP 才能从 Connect/Active 状态继续前进。这发生在 FSM 转换为 **OpenSent** 时。因此，从 **OpenSent** 开始（OpenSent → OpenConfirm → Established），TCP 会话已完全建立。

但是，问题 specifically 询问的是哪个状态**指示**TCP 三次握手已完成，并且 BGP 会话已完全可用于路由交换。这个状态是 **Established** 状态——这是 BGP 对等被认为是“正常”并且实际正在交换路由信息的唯一状态。

### 快速总结
- **Idle → Connect → (可能 Active)**：尝试完成 TCP 握手
- **OpenSent → OpenConfirm → Established**：TCP 握手已完成
- **Established** = BGP 邻居完全正常（TCP + BGP 会话成功）

因此，**D) Established** 是确认 TCP 三次握手已完成且 BGP 会话已正常运行的明确状态。

参考文献：
- [RFC 4271 – A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271.html)
- [Cisco BGP Finite State Machine](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html)
