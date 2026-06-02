---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停止等待ARQ过程步骤
translated: true
type: note
---

**问题：** 在数据通信的错误控制技术中，Stop-and-Wait ARQ 是错误检测和重传的常见方法之一。下图描述了发送方和接收方传输数据时使用 Stop-and-Wait ARQ 的过程。请根据提供的参考答案逻辑，写出图中①至⑥的内容。

**答案：**

根据提供的参考答案和 Stop-and-Wait ARQ 协议的标准机制（特别是使用 NAK - Negative Acknowledgment 的变体），以下是对①至⑥项目的详细推导和解释：

**事件序列：**

1. **上下文**：发送方很可能刚刚发送了 `PKT1` 并收到了确认，因此现在正尝试发送 `PKT2`。
2. **项目①：ACK**
    * **逻辑**：在发送新数据（`PKT2`）之前，发送方可能正在接收前一个数据包（`PKT1`）的最终确认，或者这代表前一步骤的成功确认，允许序列继续。在参考答案以 `ACK` 开头的上下文中，这意味着信道已清空或前一个事务已成功关闭。
    * **内容**：**ACK**（确认）

3. **项目②：PKT2**
    * **逻辑**：收到 ACK（或作为序列的下一步）后，发送方传输第二个数据包。
    * **内容**：**PKT2**（数据包 2）

4. **项目③：NAK**
    * **逻辑**：接收方收到 `PKT2` 但检测到错误（例如，通过 CRC 检查）。这种特定协议变体不是保持沉默（这将依赖超时），而是发送 **NAK**（Negative Acknowledgment）立即通知发送方 `PKT2` 已损坏，需要重传。
    * **内容**：**NAK**（否定确认）

5. **项目④：PKT2**
    * **逻辑**：收到 NAK 后，发送方立即重传损坏的数据包。它尚未推进到下一个序列号；必须重发 `PKT2`。
    * **内容**：**PKT2**（数据包 2 的重传）

6. **项目⑤：ACK**
    * **逻辑**：接收方成功收到重传的 `PKT2`。它验证完整性，接受数据，并发送正确认。
    * **内容**：**ACK**（针对 PKT2 的确认）

7. **项目⑥：PKT3**
    * **逻辑**：现在 `PKT2` 已确认，发送方继续发送序列中的下一个数据包。
    * **内容**：**PKT3**（数据包 3）

**流程总结：**

* 发送方收到前一数据的 **ACK**（①）。
* 发送方发送 **PKT2**（②）。
* 接收方检测到 PKT2 中的错误并发送 **NAK**（③）。
* 发送方重发 **PKT2**（④）。
* 接收方接受重发的 PKT2 并发送 **ACK**（⑤）。
* 发送方发送下一个数据 **PKT3**（⑥）。

此场景突显了在 Stop-and-Wait ARQ 中使用 NAK 的效率，因为当接收方立即检测到错误时，避免了等待超时期。

**参考资料：**

* [Stop-and-Wait ARQ Protocol - GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
* [Error Control: Flow Control & Error Control - Tutorialspoint](https://www.tutorialspoint.com/data_communication_computer_network/error_control.htm)
