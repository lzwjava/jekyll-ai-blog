---
audio: false
generated: true
image: false
lang: en
layout: post
title: Firewall Tech Beyond NAT Explained
translated: false
type: note
---

Question: What are the three main firewall technologies besides NAT, what does NAT stand for in Chinese, what are its specific functions, and how does NAT technology in firewall products contribute to network protection?

Answer:

Based on working principles, firewall technologies are primarily categorized into four types. Besides **Network Address Translation (NAT)**, the other three main technologies are:

1. **Packet Filtering Technology (包过滤技术)**
    * This is the most basic form of firewall. It examines each packet entering or leaving the network and accepts or rejects it based on user-defined rules (such as source/destination IP addresses, ports, and protocols). It operates at the network layer (Layer 3) and sometimes the transport layer (Layer 4).

2. **Proxy Service Technology (代理服务技术)**
    * Also known as Application Layer Gateways. This technology acts as an intermediary between internal clients and external servers. The proxy receives the request from the internal user, validates it, and then forwards it to the external server on behalf of the user. This hides the internal network structure completely and allows for deep inspection of application-layer data.

3. **Stateful Inspection Technology (状态检测技术)**
    * This combines the speed of packet filtering with the security of proxy services. Instead of examining packets in isolation, it tracks the state of active connections (e.g., TCP handshakes). It makes decisions based on the context of the traffic flow, ensuring that incoming packets are part of a legitimate, established session.

### NAT Details

* **Chinese Meaning**: The Chinese term for NAT is **网络地址转换** (Wǎngluò Dìzhǐ Zhuǎnhuàn). Sometimes it is referred to as the Network Address Translation Protocol, but strictly speaking, it is a method/function rather than a standalone protocol.
* **Specific Function**: The primary function of NAT is to map **internal private IP addresses** to **legal public IP addresses**. This allows multiple devices on a local network (using non-routable private IPs like 192.168.x.x) to share a single public IP address when accessing the Internet. It modifies the IP header of packets as they pass through the router or firewall.

### Protective Role of NAT in Firewalls

While NAT was originally designed to conserve IPv4 addresses, it provides a significant side benefit regarding network security:

* **Hiding Internal Topology**: NAT hides the internal network's addressing scheme from the outside world. External networks only see the public IP address of the firewall, not the specific private IPs of individual computers inside.
* **Preventing Direct Attacks**: Because external attackers cannot see or directly route traffic to specific internal private IP addresses, they cannot easily initiate direct attacks against a specific computer within the internal network. An attacker would first need to compromise the firewall or exploit a specific port mapping rule to reach an internal host. This creates a natural barrier often described as "security through obscurity," though it is most effective when combined with stateful inspection.

References:
