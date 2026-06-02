---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向连接网络基础
translated: true
type: note
---

问题：日常打电话的过程被描述为“pick up the phone - dial the number - connect and talk - hang up”。类似于这个打电话过程的网络服务叫什么？

答案：

类似于所述打电话过程的网络服务称为 **Connection-Oriented** 服务（或中文中的 **面向连接** 服务）。

### 解释

1. **与电话通话的类比**：
    * **Pick up/Dial (Setup)**：正如你必须拨号并等待对方接听才能说话一样，connection-oriented 服务需要在传输任何数据之前，通过一个特定阶段在发送方和接收方之间建立逻辑路径。在网络术语中，这通常称为 "handshake"（例如，TCP three-way handshake）。
    * **Talk (Data Transfer)**：一旦连接建立，数据就在双方之间顺序且可靠地流动，就像对话一样。
    * **Hang up (Teardown)**：对话结束后，线路断开。同样，connection-oriented 服务需要一个正式的终止阶段来释放资源并关闭连接。

2. **关键特性**：
    * **Setup Phase**：数据传输之前必须建立连接。
    * **Reliability**：数据通常按顺序、无错误到达（guaranteed delivery）。
    * **Stateful**：网络在会话期间维护连接的状态。
    * **Example**：Internet 协议套件中最常见的示例是 **TCP** (Transmission Control Protocol)。

3. **对比**：
    * 这与 **Connectionless** 服务相反（如同寄信或使用 UDP），其中每个数据包独立发送，没有事先建立，且没有顺序或交付的保证。

参考资料：

* [Transmission Control Protocol (TCP) - Wikipedia](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
* [Connection-oriented communication - Wikipedia](https://en.wikipedia.org/wiki/Connection-oriented_communication)
