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

Here are 30 multiple-choice questions for the course **13833 Switching and Routing Technologies** (China National Higher Education Self-Study Examination, Guangdong), covering key topics such as Ethernet switching, VLAN, Spanning Tree Protocol, IP routing, OSPF, BGP, IPv6, routing security, etc. Questions are in English (standard for technical content).

1. Which layer of the OSI model does a Layer 2 switch primarily operate on?
A) Layer 1
B) Layer 2
C) Layer 3
D) Layer 4

2. What is the destination MAC address of a broadcast frame in an Ethernet network?
A) 0000.0000.0000
B) FFFF.FFFF.FFFF
C) 0100.5E00.0000
D) The MAC of the default gateway

3. In a switch MAC address table, what does the term “aging time” refer to?
A) Time a port stays in forwarding state
B) Time before a dynamic MAC entry is removed
C) Time a VLAN remains active
D) Time before ARP cache expires

4. Which command enables PortFast on a Cisco switch interface?
A) spanning-tree portfast
B) spanning-tree bpduguard enable
C) no spanning-tree uplinkfast
D) spanning-tree mode rapid-pvst

5. What is the main purpose of VLANs in a switched network?
A) Increase broadcast domain size
B) Segment Layer 2 broadcast domains
C) Replace the need for routers
D) Provide Layer 3 encryption

6. Which VLAN is the native VLAN by default on Cisco switches?
A) VLAN 1
B) VLAN 1002
C) VLAN 0
D) VLAN 4094

7. Which protocol prevents Layer 2 switching loops?
A) VTP
B) DTP
C) STP
D) LACP

8. In RSTP, which port role is equivalent to the blocking port in traditional STP?
A) Root Port
B) Designated Port
C) Alternate Port
D) Edge Port

9. Which command configures an access port for VLAN 20 on a Cisco switch?
A) switchport mode access vlan 20
B) switchport access vlan 20
C) switchport mode access
D) switchport trunk allowed vlan 20

10. What does the command “switchport mode dynamic desirable” do?
A) Forces trunking
B) Forces access mode
C) Actively attempts to form a trunk
D) Only accepts trunking if the other side initiates

11. Which VTP mode does NOT allow a switch to create or delete VLANs?
A) Server
B) Client
C) Transparent
D) Off

12. Which EtherChannel load-balancing method uses source and destination MAC addresses by default on most Cisco switches?
A) src-mac
B) dst-mac
C) src-dst-mac
D) src-ip

13. What is the administrative distance of a static route by default?
A) 0
B) 1
C) 5
D) 110

14. Which routing protocol uses bandwidth and delay as its default metric?
A) RIP
B) OSPF
C) EIGRP
D) IS-IS

15. In OSPF, which packet type is used to discover neighbors?
A) Hello
B) DBD
C) LSR
D) LSU

16. What is the OSPF router ID election order by default?
A) Highest loopback IP > Highest physical IP
B) Lowest loopback IP > Lowest physical IP
C) Manually configured > Highest loopback > Highest physical
D) Randomly assigned

17. Which EIGRP packet is sent as a unicast and requires acknowledgment?
A) Hello
B) Update
C) Query
D) Reply

18. In BGP, which attribute is used first in the path selection process?
A) Local Preference
B) AS Path
C) Weight
D) MED

19. Which BGP neighbor state indicates that a TCP three-way handshake has been completed?
A) Idle
B) Connect
C) Active
D) Established

20. What is the primary purpose of route summarization?
A) Increase routing table size
B) Reduce routing table size and update traffic
C) Encrypt routing updates
D) Prioritize one path over another

21. Which command enables IPv6 routing on a Cisco router?
A) ipv6 enable
B) ipv6 unicast-routing
C) ipv6 address autoconfig
D) ipv6 router ospf 1

22. What is the IPv6 loopback address?
A) ::1
B) FE80::1
C) FF02::1
D) 2001::1

23. Which IPv6 address type is used for provider-independent addressing?
A) Link-local
B) Unique Local Address (ULA)
C) Global Unicast
D) Multicast

24. Which protocol is the IPv6 equivalent of ARP?
A) NDP
B) ICMPv6
C) DHCPv6
D) SLAAC

25. Which command configures an IPv6 static route to destination 2001:DB8::/32 via next-hop 2001:DB8:1::1?
A) ipv6 route 2001:DB8::/32 2001:DB8:1::1
B) ip route 2001:DB8::/32 2001:DB8:1::1
C) ipv6 route 2001:DB8::/32 serial0/0
D) route ipv6 2001:DB8::/32 2001:DB8:1::1

26. What is the main goal of First-Hop Redundancy Protocols (FHRP)?
A) Load balance traffic across multiple links
B) Provide default gateway redundancy
C) Encrypt traffic to the gateway
D) Reduce ARP broadcasts

27. Which FHRP protocol uses a virtual MAC address of 0000.0C9F.Fxxx?
A) HSRP
B) VRRP
C) GLBP
D) IRDP

28. Which feature prevents a rogue device from becoming the STP root bridge?
A) BPDU Guard
B) Root Guard
C) Loop Guard
D) UDLD

29. What does the command “ip verify unicast source reachable-via rx” enable?
A) uRPF (Unicast Reverse Path Forwarding)
B) IP Source Guard
C) DHCP Snooping
D) Dynamic ARP Inspection

30. In route filtering, which Cisco access-list type can match both prefix and prefix-length?
A) Standard ACL
B) Extended ACL
C) Prefix-list
D) Route-map

These questions are suitable for the 13833 exam level and cover the core syllabus content. Good luck with your studies!
