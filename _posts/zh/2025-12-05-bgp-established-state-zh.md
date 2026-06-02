---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: BGP建立状态解释
translated: true
type: note
---

问题：哪个BGP邻居状态表示TCP三次握手已完成？
A) Idle
B) Connect
C) Active
D) Established

答案：

**D) Established**

BGP有限状态机中的 **Established** 状态只有在TCP三次握手成功完成，并且BGP对等体交换了有效的Open消息，随后是Keepalive消息之后才能达到。这是BGP会话完全运行并可以交换路由信息（Update消息）的唯一状态。

供参考，与TCP连接建立相关的BGP邻居状态有：

- **Idle**：初始状态，尚未尝试连接。
- **Connect**：等待TCP三次握手完成。
- **Active**：TCP握手失败或超时；正在主动重试建立TCP。
- **Established**：TCP连接已建立，BGP Open消息已成功交换 → 对等关系已完全建立。

因此，正确答案是 **D) Established**。
