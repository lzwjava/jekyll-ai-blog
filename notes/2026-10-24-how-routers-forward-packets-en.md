---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Routers Forward Packets
translated: false
type: note
---

Question: How does a router work, and how does it forward (retransmit) packets?

Answer:

## How a Router Works

A router is a **Layer 3 (Network Layer)** device that connects different networks and forwards packets between them based on **IP addresses**.

### Core Components

| Component | Role |
| --- | --- |
| **Routing Table** | Maps destination networks → next-hop / outgoing interface |
| **Forwarding Engine** | Hardware that moves packets at line speed |
| **ARP Cache** | Maps IP addresses → MAC addresses for next hops |
| **Routing Protocol** | Builds/updates the routing table (OSPF, BGP, RIP…) |

---

## Packet Forwarding Step-by-Step

Here's a detailed breakdown:

---

### ① Receive packet — strip the L2 frame

When a packet arrives on a router interface, the router **strips the Ethernet (Layer 2) frame** — removing the MAC-address header. What's left is the raw **IP packet** (Layer 3).

---

### ② Read the IP header — decrement TTL

The router reads:

- **Destination IP address** — to decide where to send it
- **TTL (Time To Live)** — decremented by 1 each hop

If TTL hits **0**, the packet is dropped and an **ICMP "Time Exceeded"** message is sent back to the source. This prevents infinite routing loops.

---

### ③ Routing table lookup (the core decision)

The router consults its **routing table** using **longest prefix match**:

| Destination | Next Hop | Interface |
| --- | --- | --- |
| `10.0.0.0/8` | — | `eth1` |
| `192.168.0.0/16` | `10.0.0.1` | `eth0` |
| `0.0.0.0/0` | `203.0.1.1` | `eth2` (default) |

The most specific matching prefix wins. The router learns these entries via:

- **Static routes** — manually configured
- **Dynamic protocols** — OSPF, BGP, RIP (routers exchange routes with each other)

---

### ④ ARP + Re-encapsulate into a new L2 frame

The routing table gives a **next-hop IP**, but to actually send on the wire the router needs a **MAC address**. It uses **ARP (Address Resolution Protocol)** to resolve the next-hop IP → MAC, then **wraps the IP packet in a brand-new Ethernet frame** with:

- **New source MAC** = router's outgoing interface
- **New dest MAC** = next-hop device's MAC

> The IP packet itself is unchanged (same source/dest IPs), only the L2 wrapper is replaced.

---

### ⑤ Transmit

The new frame is sent out the correct physical interface toward the next hop. This repeats at every router until the packet reaches its destination.

---

### Key distinction: Routers don't "retransmit" — end hosts do

Routers **forward** (not retransmit). If a router **drops** a packet (queue full, TTL expired, no matching route), it silently drops it (or sends an ICMP error). **TCP retransmission** is handled entirely by the **sender** — it detects loss via timeout or duplicate ACKs and resends.

---

References:

- [RFC 791 — Internet Protocol (IP)](https://datatracker.ietf.org/doc/html/rfc791)
- [RFC 826 — ARP](https://datatracker.ietf.org/doc/html/rfc826)
- [RFC 792 — ICMP](https://datatracker.ietf.org/doc/html/rfc792)
