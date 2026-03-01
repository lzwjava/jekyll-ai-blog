---
audio: false
generated: true
image: false
lang: en
layout: post
title: Firewall Types and Packet Filtering Limits
translated: false
type: note
---

Question: According to different working principles, firewall technologies are mainly divided into four categories. Besides packet filtering technology, what are the other three categories? What is the basic idea of packet filtering technology? What are the main disadvantages of packet filtering technology?

Answer: 

The four main categories of firewall technologies, classified by their working principles, are:

1. Packet Filtering (包过滤技术)  
2. Proxy Service (代理服务技术) / Application Gateway  
3. Stateful Inspection (状态检测技术) / Dynamic Packet Filtering  
4. NAT (Network Address Translation) technology (NAT技术)

**Basic idea of packet filtering technology:**  
Packet filtering examines each IP packet (datagram) passing through the firewall and makes allow/deny decisions based on the information contained in the packet header. The decision is primarily made according to the following fields:

- Source IP address  
- Destination IP address  
- Source port number  
- Destination port number  
- Protocol type (TCP, UDP, ICMP, etc.)  
- Sometimes other fields such as TCP flags

The firewall compares these header values against a predefined set of filtering rules (Access Control List – ACL) to decide whether to allow the packet to pass through or to drop/reject it.

**Main disadvantages of packet filtering technology:**

- IP spoofing is easy to perform (source IP address can be easily forged), which can bypass the filtering rules and cause filtering failure.  
- It can only inspect limited information at the network layer (Layer 3) and transport layer (Layer 4), and cannot identify or distinguish specific application-layer protocols or application behaviors.  
- The filtering logic is relatively simple and the amount of information it can use for decision-making is limited, making it difficult to handle complex attack scenarios or application-specific threats.  
- It is stateless (in the classic sense), so it cannot track the context or state of a connection, which makes it vulnerable to certain attacks (such as TCP sequence prediction attacks or fragmented packet attacks).

References:  

- None (this is a standard classification and explanation in network security textbooks and certification materials)