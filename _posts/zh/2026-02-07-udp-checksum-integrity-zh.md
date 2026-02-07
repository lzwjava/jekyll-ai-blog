---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 确保数据完整性的 UDP 校验和
translated: true
type: note
---

Question: UDP header 中的哪个字段用于确保数据完整性，它是如何工作的？

Answer:

User Datagram Protocol (UDP) header 中用于确保数据安全的字段是 **Checksum** (检验和)。

虽然 UDP 以“尽力而为” (best-effort) 和不可靠的协议著称，但 Checksum 提供了一个基本的错误检测层，以防止交付损坏的数据。

### UDP Checksum 如何工作

Checksum 旨在验证 UDP header 和数据 payload 中的位在传输过程中没有被更改。

1. **Pseudo-Header**: 为了使校验更加稳健，UDP 会创建一个 "pseudo-header"，其中包含 Source IP Address、Destination IP Address 和 Protocol number (UDP 为 17)。这确保了数据包没有被错误路由。
2. **Calculation**: 发送方将 pseudo-header、UDP header 和数据视为一系列 16-bit integers。它对这些整数执行 **one's complement sum** (反码求和)。
3. **Verification**: 接收方执行相同的计算。如果结果全为 1（在反码运算中），则认为数据是完整的。
4. **Action on Failure**: 如果 Checksum 不匹配，UDP 层会 **静默丢弃 (silently discards)** 该数据包。与 TCP 不同，UDP 不会请求重传。

---

### UDP Checksum 的关键特性

* **IPv4 中可选**: 在 IPv4 中，Checksum 在技术上是可选的。如果不使用，该字段将填充为零。
* **IPv6 中强制**: 因为 IPv6 移除了 IP 层的 header checksum，所以 **必须** 使用 UDP Checksum 以确保基本完整性。
* **局限性**: 它只能检测错误，不能修复错误。它也无法防止数据包丢失或乱序到达。

---

### Comparison: UDP vs. TCP Checksum

| Feature | UDP Checksum | TCP Checksum |
| --- | --- | --- |
| **Requirement** | Optional (IPv4) / Mandatory (IPv6) | Always Mandatory |
| **Error Handling** | Discards packet silently | Discards and requests retransmission |
| **Focus** | Speed and low overhead | Reliability and data integrity |

您是否需要我为您展示计算 one's complement checksum 的逐步数学运算？