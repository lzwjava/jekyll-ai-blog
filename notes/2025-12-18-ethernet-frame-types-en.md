---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ethernet Frame Types Explained
translated: false
type: note
---

Question: What are unicast frames? What are the other types of frames?

Answer: 

In computer networking, particularly at the data link layer (Layer 2) in Ethernet networks, frames are classified based on their destination MAC address. This classification determines how switches and other devices handle and forward them.

### Unicast Frames
- A **unicast frame** is an Ethernet frame sent from one sender to a single specific receiver.
- The destination MAC address is a unique unicast address assigned to a single network interface (e.g., starting with an even first octet in hexadecimal, where the least-significant bit of the first octet is 0).
- Switches forward unicast frames only to the specific port associated with the destination MAC address (learned via the MAC address table). If the destination is unknown, the frame is flooded (treated like a broadcast until learned).
- This is the most common type of traffic, used for everyday communication like web browsing or file transfers between two devices.

### Other Types of Frames
There are two main other types at Layer 2:

#### Broadcast Frames
- A **broadcast frame** is sent from one sender to **all devices** in the local network segment (broadcast domain).
- The destination MAC address is `FF:FF:FF:FF:FF:FF` (all binary 1s).
- Switches flood broadcast frames out all ports in the same VLAN (except the incoming port).
- Common uses: ARP requests, DHCP discoveries.
- Broadcasts do not cross routers (limited to the local Layer 2 domain).

#### Multicast Frames
- A **multicast frame** is sent from one sender to a **specific group** of interested receivers (not all devices).
- The destination MAC address has the least-significant bit of the first octet set to 1 (e.g., addresses starting with 01:00:5E for IPv4 multicast).
- Without optimizations (like IGMP snooping), switches flood multicast frames like broadcasts. With optimizations, they are sent only to ports with interested devices.
- Common uses: Video streaming, routing protocol updates (e.g., OSPF), discovery protocols (e.g., CDP).

Note: There is no "anycast" at the Ethernet frame level, as anycast is a Layer 3 (IP) concept where traffic is routed to the nearest device in a group.

These classifications help efficiently manage network traffic: unicast for direct communication, multicast for group efficiency, and broadcast for reaching everyone locally.

References:  

- [Unicast, Multicast, and Broadcast Addresses - Study CCNA](https://study-ccna.com/unicast-multicast-and-broadcast-addresses/)  
- [Unicast, Multicast, and Broadcast Explained](https://www.computernetworkingnotes.com/ccna-study-guide/unicast-multicast-and-broadcast-explained.html)  
- [Identifying Ethernet Multicast - Brad Hedlund](https://bradhedlund.com/2007/11/21/identifying-ethernet-multicast/)  
- [Unicast, multicast, broadcast addresses | CCNA](https://geek-university.com/unicast-multicast-broadcast-addresses/)