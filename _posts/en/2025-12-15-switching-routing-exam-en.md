---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Switching and Routing Exam Questions
translated: false
type: note
---

Question: Provide 30 multiple-choice questions for the course 13833 Switching and Routing Technologies (China National Higher Education Self-Study Examination, Guangdong).

Answer:

Here are 30 multiple-choice questions covering key topics in Switching and Routing Technologies, including network fundamentals, Ethernet switching, VLANs, STP, routing protocols (RIP, OSPF, BGP), IPv6, network security, and device configuration.

1. Which layer of the OSI model is responsible for logical addressing and routing?
   A) Physical Layer
   B) Data Link Layer
   C) Network Layer
   D) Transport Layer

2. What is the primary function of a switch in a network?
   A) Routing packets between different networks
   B) Forwarding frames based on MAC addresses
   C) Providing IP addresses to hosts
   D) Encrypting data traffic

3. In Ethernet switching, what happens when a switch receives a frame with a destination MAC address not in its MAC address table?
   A) It drops the frame
   B) It floods the frame out all ports except the incoming port
   C) It sends the frame to the default gateway
   D) It buffers the frame indefinitely

4. What is the purpose of VLANs in a switched network?
   A) To increase broadcast domains
   B) To segment broadcast domains and improve security
   C) To route traffic between switches
   D) To assign IP addresses dynamically

5. Which protocol is used to prevent loops in a Layer 2 network?
   A) OSPF
   B) RIP
   C) Spanning Tree Protocol (STP)
   D) BGP

6. In STP, which port state blocks traffic to prevent loops?
   A) Listening
   B) Learning
   C) Forwarding
   D) Blocking

7. What is the default priority value for a switch in STP?
   A) 0
   B) 32768
   C) 61440
   D) 65535

8. Which VLAN is the default VLAN on most switches?
   A) VLAN 0
   B) VLAN 1
   C) VLAN 100
   D) VLAN 1001

9. What type of VLAN carries traffic for multiple VLANs between switches?
   A) Access VLAN
   B) Native VLAN
   C) Trunk VLAN
   D) Voice VLAN

10. Which command is used to configure a port as a trunk port on a switch?
    A) switchport mode access
    B) switchport mode trunk
    C) switchport trunk encapsulation dot1q
    D) switchport access vlan 10

11. What is the administrative distance of a static route by default?
    A) 0
    B) 1
    C) 110
    D) 120

12. Which routing protocol uses hop count as its metric?
    A) OSPF
    B) RIP
    C) BGP
    D) EIGRP

13. What is the maximum hop count in RIP?
    A) 15
    B) 16
    C) 255
    D) Unlimited

14. OSPF is which type of routing protocol?
    A) Distance Vector
    B) Link State
    C) Path Vector
    D) Hybrid

15. In OSPF, what is the router ID used for?
    A) Identifying areas
    B) Electing the Designated Router (DR)
    C) Calculating the metric
    D) Advertising routes

16. Which protocol is used for exterior gateway routing between autonomous systems?
    A) RIP
    B) OSPF
    C) BGP
    D) IS-IS

17. What does NAT stand for?
    A) Network Address Translation
    B) Network Access Terminal
    C) Node Address Table
    D) New Area Type

18. Which type of NAT maps multiple private IPs to a single public IP?
    A) Static NAT
    B) Dynamic NAT
    C) PAT (Overload)
    D) One-to-One NAT

19. What is the purpose of an Access Control List (ACL)?
    A) To assign IP addresses
    B) To filter traffic based on rules
    C) To configure VLANs
    D) To enable routing

20. In IPv6, what is the loopback address?
    A) ::1
    B) FE80::1
    C) FF02::1
    D) 127.0.0.1

21. How many bits are in an IPv6 address?
    A) 32
    B) 64
    C) 128
    D) 256

22. Which protocol is used for stateless address autoconfiguration in IPv6?
    A) DHCPv6
    B) SLAAC
    C) NAT66
    D) OSPFv3

23. What is the primary benefit of using DHCP?
    A) Manual IP assignment
    B) Automatic IP address allocation
    C) Traffic encryption
    D) Loop prevention

24. Which command displays the routing table on a router?
    A) show ip route
    B) show interfaces
    C) show vlan
    D) show mac address-table

25. What is the purpose of ARP?
    A) Resolve IP to MAC address
    B) Resolve MAC to IP address
    C) Route packets
    D) Encrypt data

26. In a switched network, what causes a broadcast storm?
    A) Too many unicast frames
    B) Network loops without STP
    C) Misconfigured VLANs
    D) High bandwidth usage

27. Which port security feature limits the number of MAC addresses on a port?
    A) Sticky MAC
    B) Violation Restrict
    C) Maximum MAC addresses
    D) Portfast

28. What is the default encapsulation for trunks on modern switches?
    A) ISL
    B) 802.1Q
    C) PPP
    D) HDLC

29. Which OSPF area type does not allow external routes?
    A) Backbone Area
    B) Stub Area
    C) Totally Stubby Area
    D) NSSA

30. What is the multicast address range in IPv4?
    A) 192.168.0.0/16
    B) 224.0.0.0 to 239.255.255.255
    C) 10.0.0.0/8
    D) 172.16.0.0/12

**Correct Answers:**
1. C
2. B
3. B
4. B
5. C
6. D
7. B
8. B
9. B (Note: Trunk ports carry multiple VLANs)
10. B
11. B
12. B
13. A
14. B
15. B
16. C
17. A
18. C
19. B
20. A
21. C
22. B
23. B
24. A
25. A
26. B
27. C
28. B
29. B
30. B

References:

- [广东交换与路由技术自考考试大纲(13833免费下载)](https://www.zikaosw.cn/news/22147405.html)
- [路由交换技术及应用（第4版）图书内容概述](https://www.ryjiaoyu.com/book/details/47556)
- [路由交换技术复习题示例](https://blog.csdn.net/m0_64000952/article/details/139968916)
