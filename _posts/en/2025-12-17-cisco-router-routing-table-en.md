---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Cisco Router Routing Table Command
translated: false
type: note
---

Question: Which command displays the routing table on a Cisco router, and why is D the correct answer?

Answer: 

The correct answer is **A) show ip route**.

### Comprehensive Explanation:

- **show ip route**: This is the primary Cisco IOS command used to display the IP routing table on a router. The routing table contains information about known networks (destinations), how they were learned (e.g., connected, static, or via dynamic routing protocols like OSPF, EIGRP, RIP, BGP), the next-hop address, administrative distance, metric, and the outgoing interface. It is essential for troubleshooting routing issues, verifying route installation, and understanding how the router forwards packets.

  Example output snippet:
  ```
  Router# show ip route
  Codes: C - connected, S - static, R - RIP, O - OSPF, B - BGP ...
  Gateway of last resort is 203.0.113.1 to network 0.0.0.0

  C    192.168.1.0/24 is directly connected, GigabitEthernet0/0
  O    10.0.0.0/8 [110/20] via 172.16.1.2, GigabitEthernet0/1
  S*   0.0.0.0/0 [1/0] via 203.0.113.1
  ```

- **show interfaces**: This command displays detailed status and statistics for all router interfaces (or a specific interface if specified, e.g., `show interfaces GigabitEthernet0/0`). It includes information like up/down status, IP address, MTU, bandwidth, errors, and traffic counters. It does **not** show the routing table.

- **show vlan**: This command is primarily used on Cisco switches (not routers) to display VLAN configuration and membership information. On multilayer switches it might show VLAN-related details, but it has no relation to the IP routing table on a router.

- **show mac address-table**: This command is used on Cisco switches to display the MAC address table (CAM table), showing learned MAC addresses, associated ports, and VLANs. It is unrelated to IP routing and does not exist or function the same way on pure routers.

### Why the user selected D is incorrect:
Selecting **D) show mac address-table** indicates a possible confusion between Layer 2 switching functions (MAC learning and forwarding on switches) and Layer 3 routing functions (IP route lookup on routers). Routers operate primarily at Layer 3 and maintain a routing table for IP forwarding decisions, whereas the MAC address table is a Layer 2 construct used by switches.

In summary, for viewing the routing table on a Cisco router, always use **show ip route** (or its variants like `show ip route ospf` to filter by protocol).