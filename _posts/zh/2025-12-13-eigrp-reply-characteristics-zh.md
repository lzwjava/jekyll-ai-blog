---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: EIGRP回复数据包的特征
translated: true
type: note
---

问题：哪个 EIGRP 数据包以单播形式发送并需要确认？  
A) Hello  
B) Update  
C) Query  
D) Reply

答案：

**D) Reply**

在 EIGRP 中，Reply 数据包始终以单播形式发送给发起 Query 的路由器。与 Update 和 Query 数据包一样，Reply 数据包通过 EIGRP 的可靠传输协议 (RTP) 可靠传输，需要接收方明确的确认 (ACK)。

- **Hello** 数据包是组播（在静态邻居等特定情况下为单播）且不可靠——不需要确认。
- **Update** 数据包可以是组播或单播，但发送时是可靠的。
- **Query** 数据包通常是组播（如果需要则重新发送为单播）且可靠。
- 只有 **Reply** 始终符合这两个标准：始终为单播且始终需要确认。

参考资料：  

- https://www.computernetworkingnotes.com/ccna-study-guide/eigrp-packet-types-and-rtp-protocol.html  
- https://www.geeksforgeeks.org/computer-networks/types-of-eigrp-packet-in-computer-network/  
- https://ipcisco.com/lesson/eigrp-packet-types-and-neighbourship-ccnp/  
- https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/13669-1.html