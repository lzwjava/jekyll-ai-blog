---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: Switching and Routing Exam Knowledge Points
translated: false
type: note
---

Here is a comprehensive list of 100 knowledge points for the "Switching and Routing Technology" (13833) exam, structured according to the syllabus projects and assessment objectives.

### Project 1: eNSP and VRP Fundamentals

1. **eNSP Purpose:** eNSP is a graphical network simulation platform used to simulate Huawei enterprise-level network equipment.
2. **VRP System:** The Versatile Routing Platform (VRP) is the operating system used in Huawei network devices.
3. **User View:** The initial view upon login, denoted by `<Huawei>`, used for viewing basic device information.
4. **System View:** Entered using the `system-view` command, used for modifying global device parameters.
5. **Interface View:** Used for configuring specific physical or logical ports (e.g., `interface GigabitEthernet 0/0/1`).
6. **Command Completion:** The Tab key is used to automatically complete a partially typed command.
7. **Question Mark (?):** Provides a list of available commands or help with command parameters.
8. **Save Configuration:** The `save` command stores the current configuration in flash memory to prevent data loss after a reboot.
9. **Undo Command:** The `undo` keyword is used to delete a configuration or disable a specific function.
10. **Display Commands:** The `display` command (e.g., `display this`) is used to view the current status or configuration settings.

---

### Project 2: Switching Technology & Campus Networks

11. **Layer 2 Switching:** Switches forward data frames based on Destination MAC addresses at the Data Link Layer.
12. **MAC Address Table:** A dynamic table mapping MAC addresses to specific physical ports on a switch.
13. **Layer 3 Switching:** Combines Layer 2 switching with Layer 3 routing to achieve high-speed inter-VLAN data forwarding.
14. **VLAN Definition:** Virtual Local Area Networks logically segment a physical network into multiple broadcast domains.
15. **VLAN Advantages:** Improves security, reduces broadcast traffic, and simplifies network management.
16. **Access Port:** A port type used to connect to end devices (PCs) that belongs to a single VLAN.
17. **Trunk Port:** A port type that allows multiple VLANs to pass through a single physical link between switches.
18. **Hybrid Port:** A Huawei-specific port type that can handle both tagged and untagged traffic flexibly.
19. **PVID:** The Port VLAN ID identifies the default VLAN tag assigned to untagged frames entering a port.
20. **IEEE 802.1Q:** The standard industry protocol used for VLAN tagging in Ethernet frames.
21. **Inter-VLAN Routing:** Achieved using a Layer 3 switch or a router to allow communication between different VLANs.
22. **VLANIF Interface:** A logical Layer 3 interface on a switch used as a gateway for a specific VLAN.
23. **Link Aggregation:** Combines multiple physical links into one logical link to increase bandwidth and provide redundancy.
24. **LACP Protocol:** The Link Aggregation Control Protocol used to dynamically negotiate and manage aggregated links.
25. **Network Loops:** Occur when multiple active paths exist between switches, leading to broadcast storms.
26. **STP (Spanning Tree Protocol):** Prevents network loops by logically blocking redundant ports.
27. **Root Bridge:** The central switch in an STP topology, selected based on the lowest Bridge ID.
28. **RSTP (Rapid STP):** An evolution of STP that provides significantly faster convergence times when the topology changes.
29. **VRRP (Virtual Router Redundancy Protocol):** Provides gateway redundancy by grouping multiple routers/switches into one virtual router.
30. **Master Router:** The active device in a VRRP group responsible for forwarding traffic.
31. **Backup Router:** The standby device in a VRRP group that takes over if the Master fails.
32. **DHCP (Dynamic Host Configuration Protocol):** Automatically assigns IP addresses, masks, and gateways to network hosts.
33. **DHCP Server:** The device (router or switch) that manages the IP address pool and leases addresses.
34. **DHCP Relay:** Allows a DHCP server to provide addresses to clients located in different subnets/VLANs.
35. **Console Port:** A physical management port used for local initial configuration of a switch or router.
36. **Telnet/SSH:** Protocols used for remote management of network devices over the network.
37. **Full-Duplex:** Allows simultaneous bidirectional data transmission on a switch port.
38. **Half-Duplex:** Allows data transmission in both directions, but only one direction at a time.
39. **Port Security:** A feature that limits the number of MAC addresses allowed on a single switch port.
40. **Broadcast Storm:** Excessive broadcast traffic that consumes all bandwidth and crashes the network.

---

### Project 3: Routing Technology & Inter-Networking

41. **Router Function:** Connects different network segments and determines the best path for IP packet forwarding.
42. **Routing Table:** A database in a router that stores paths to various network destinations.
43. **Directly Connected Route:** A route automatically created when a router's interface is configured with an IP and is active.
44. **Static Route:** A manually configured path to a destination network defined by the administrator.
45. **Default Route:** A type of static route (0.0.0.0/0) used when no specific match is found in the routing table.
46. **Floating Static Route:** A backup static route with a higher preference value that only appears if the primary link fails.
47. **Dynamic Routing:** Protocols that allow routers to automatically learn and share network topology changes.
48. **Metric:** A value used by routing protocols to determine the "cost" or efficiency of a specific path.
49. **Administrative Distance/Preference:** A value used to select the best route when multiple protocols provide the same destination.
50. **RIP (Routing Information Protocol):** A distance-vector protocol that uses "hop count" as its metric.
51. **RIPv2:** An updated version of RIP that supports VLSM and uses multicast (224.0.0.9) for updates.
52. **OSPF (Open Shortest Path First):** A link-state protocol that uses the Shortest Path First (SPF) algorithm.
53. **OSPF Area:** A logical grouping of OSPF routers used to limit the size of the link-state database.
54. **OSPF Area 0:** The backbone area in an OSPF network to which all other areas must connect.
55. **Router ID:** A unique 32-bit number used to identify a router within an OSPF process.
56. **Neighbor Relationship:** A state where two OSPF routers exchange "Hello" packets and agree on parameters.
57. **Adjacency:** A more advanced state where OSPF neighbors synchronize their link-state databases.
58. **One-Arm Routing:** Using a single physical interface on a router (with sub-interfaces) to route between multiple VLANs.
59. **Sub-interface:** A logical division of a physical interface used in "Router-on-a-Stick" configurations.
60. **Dot1q Termination:** The process of a router sub-interface stripping a VLAN tag to process an IP packet.
61. **NAT (Network Address Translation):** Translates private internal IP addresses into public IP addresses for Internet access.
62. **Static NAT:** A one-to-one mapping between a private IP and a public IP address.
63. **Dynamic NAT:** Maps private IPs to a pool of public IP addresses on a first-come, first-served basis.
64. **NAPT (Network Address Port Translation):** Allows multiple internal hosts to share one public IP by using different port numbers.
65. **ACL (Access Control List):** A set of rules used to permit or deny traffic based on IP addresses or port numbers.
66. **Basic ACL:** Uses range 2000-2999 and filters based only on the source IP address.
67. **Advanced ACL:** Uses range 3000-3999 and filters based on source/destination IP, protocol, and port numbers.
68. **ACL Rule "Deny":** Explicitly drops packets that match the specified criteria in the rule.
69. **ACL Rule "Permit":** Allows packets that match the specified criteria to pass through.
70. **Wildcard Mask:** Used in ACLs to specify which bits of an IP address should be ignored during matching.
71. **PPP (Point-to-Point Protocol):** A widely used Data Link Layer protocol for direct connections between two routers.
72. **CHAP Authentication:** A secure three-way handshake authentication method used in PPP links.
73. **IPv6 Address:** A 128-bit address designed to replace IPv4, written in eight groups of hexadecimal digits.
74. **IPv6 Stateless Autoconfiguration (SLAAC):** Allows a host to generate its own IPv6 address using the prefix provided by a router.
75. **Dual Stack:** Running both IPv4 and IPv6 simultaneously on the same network equipment.
76. **Route Redistribution:** A process allowing a router to share routes learned from one protocol into another (e.g., RIP to OSPF).
77. **Convergence:** The time it takes for all routers in a network to update their routing tables after a change.
78. **Split Horizon:** A technique used by RIP to prevent routing loops by not sending info back out the interface it was learned from.
79. **LSA (Link State Advertisement):** The data packet OSPF uses to share local topology information with neighbors.
80. **DR (Designated Router):** The lead router in an OSPF multi-access segment responsible for managing LSAs.

---

### Project 4: Advanced Configuration & Design

81. **Subnetting:** The process of dividing a large network into smaller, more manageable sub-networks.
82. **CIDR (Classless Inter-Domain Routing):** A method for IP addressing that replaces traditional Class A, B, and C categories.
83. **Subnet Mask:** A 32-bit number that distinguishes the network portion of an IP address from the host portion.
84. **Gateway:** The point of exit from a local network to other networks, usually a router or Layer 3 switch.
85. **Loopback Interface:** A virtual interface on a router used for testing and as a stable identifier for OSPF.
86. **ARP (Address Resolution Protocol):** Resolves a known IP address into a physical MAC address.
87. **Proxy ARP:** Allows a router to answer ARP requests for a network it can reach but is not directly attached to.
88. **Tracert:** A diagnostic tool used to track the hop-by-hop path a packet takes to a destination.
89. **Ping:** Uses ICMP Echo messages to test basic connectivity between two IP devices.
90. **Bandwidth:** The maximum rate of data transfer across a given path in a network.
91. **Throughput:** The actual rate of successful data delivery over a specific period.
92. **VLAN Pruning:** Restricting VLAN traffic on Trunk links to only those switches that have active members in that VLAN.
93. **Root Port:** The port on a non-root bridge with the lowest path cost to the Root Bridge.
94. **Designated Port:** The port on a network segment responsible for forwarding STP traffic.
95. **MTU (Maximum Transmission Unit):** The largest size of a data unit that can be transmitted over a network interface.
96. **Cold Boot:** Starting a device from a powered-off state.
97. **Warm Boot/Reboot:** Restarting a device without removing power, often to apply new configurations.
98. **Network Topology:** The physical or logical layout of a network (e.g., Star, Mesh, Bus).
99. **Standardization:** Using protocols like OSPF and STP to ensure compatibility between different vendors' equipment.
100. **Troubleshooting:** The systematic process of identifying, locating, and fixing faults in a network configuration.

**Would you like me to create a practice quiz based on these 100 points to help you prepare for the exam?**