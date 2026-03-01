---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 防火墙类型及数据包过滤限制
translated: true
type: note
---

Question: 根据不同的工作原理，firewall technologies 主要分为四类。除了 packet filtering technology，其他三类是什么？packet filtering technology 的基本思想是什么？packet filtering technology 的主要缺点是什么？

Answer: 

根据工作原理分类，firewall technologies 的四种主要类别是：

1. Packet Filtering (包过滤技术)  
2. Proxy Service (代理服务技术) / Application Gateway  
3. Stateful Inspection (状态检测技术) / Dynamic Packet Filtering  
4. NAT (Network Address Translation) technology (NAT技术)

**packet filtering technology 的基本思想：**  
Packet filtering 检查通过防火墙的每个 IP packet (datagram)，并基于 packet header 中包含的信息做出允许/拒绝决定。决定主要根据以下字段做出：

- Source IP address  
- Destination IP address  
- Source port number  
- Destination port number  
- Protocol type (TCP, UDP, ICMP 等)  
- 有时其他字段，如 TCP flags

防火墙将这些 header 值与预定义的 filtering rules 集（Access Control List – ACL）进行比较，以决定是否允许 packet 通过或丢弃/拒绝它。

**packet filtering technology 的主要缺点：**

- 容易进行 IP spoofing（source IP address 可以轻易伪造），这可以绕过 filtering rules 并导致 filtering 失败。  
- 它只能检查 network layer (Layer 3) 和 transport layer (Layer 4) 的有限信息，无法识别或区分特定的 application-layer protocols 或 application behaviors。  
- Filtering logic 相对简单，可用于决策的信息量有限，难以处理复杂的 attack scenarios 或特定于应用的 threats。  
- 它是 stateless（经典意义上），因此无法跟踪 connection 的上下文或状态，这使其容易受到某些 attacks（如 TCP sequence prediction attacks 或 fragmented packet attacks）的影响。

References:  

- 无（这是网络安全教科书和认证材料中的标准分类和解释）