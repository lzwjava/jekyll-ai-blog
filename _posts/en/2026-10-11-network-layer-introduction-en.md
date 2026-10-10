---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Layer Introduction
translated: false
type: note
---

**Question:** What is an introduction to the Network Layer?

**Answer:**

## Overview

The **Network Layer** is **Layer 3** of the OSI model. Its primary job is **end-to-end delivery of packets across multiple networks** — it determines the best path from source to destination, even when they are on different networks across the globe.

> If the Data Link Layer is the *local postal service within a building*, the Network Layer is the *international courier system* that routes packages between cities and countries.

---

## Key Responsibilities

| Function | Description |
|---|---|
| **Logical Addressing** | Assigns IP addresses to identify hosts globally |
| **Routing** | Selects the best path for packets across networks |
| **Packet Forwarding** | Moves packets hop-by-hop toward the destination |
| **Fragmentation** | Breaks large packets into smaller ones if needed |
| **Error Handling** | Reports delivery failures (via ICMP) |

---

## IP Address — The Core Concept

The Network Layer uses **IP addresses** (not MAC addresses) to identify devices:

```
IPv4 Example:   192.168.1.100
                └──┬──┘ └─┬─┘
              Network    Host
               Part      Part

IPv6 Example:   2001:0db8:85a3::8a2e:0370:7334
```

- **IPv4**: 32-bit address → ~4.3 billion addresses
- **IPv6**: 128-bit address → 3.4 × 10³⁸ addresses (virtually unlimited)

---

## Packet Structure (IPv4)

```
┌─────────┬────────┬──────────┬──────────┬──────────────────────┐
│ Version │  TTL   │ Protocol │ Src IP   │   Destination IP     │
│ IHL/TOS │        │          │ 4 bytes  │      4 bytes         │
├─────────┴────────┴──────────┴──────────┴──────────────────────┤
│                        Payload (Data)                          │
└────────────────────────────────────────────────────────────────┘
```

- **TTL (Time to Live)**: Prevents packets from looping forever; decremented at each hop
- **Protocol**: Indicates what's inside (TCP=6, UDP=17, ICMP=1)
- **Src/Dst IP**: Where the packet comes from and where it's going

---

## How Routing Works

Packets travel **hop by hop** through routers:

```
Your PC ──► Router A ──► Router B ──► Router C ──► Web Server
(Src IP)                                           (Dst IP)

Each router:
  1. Receives the packet
  2. Looks up Destination IP in its routing table
  3. Forwards to the next best hop
```

### Routing Table Example

| Destination Network | Next Hop | Interface |
|---|---|---|
| 192.168.1.0/24 | Direct | eth0 |
| 10.0.0.0/8 | 172.16.0.1 | eth1 |
| 0.0.0.0/0 | 203.0.113.1 | eth2 (default) |

---

## Key Protocols

| Protocol | Purpose |
|---|---|
| **IP** (v4/v6) | Core addressing and packet delivery |
| **ICMP** | Error messages & diagnostics (`ping`, `traceroute`) |
| **OSPF** | Interior routing protocol (within a network) |
| **BGP** | Exterior routing protocol (between ISPs/ASes) |
| **RIP** | Simple distance-vector routing protocol |
| **NAT** | Translates private IPs ↔ public IPs |

---

## Subnetting in 30 Seconds

IP addresses are split into **Network + Host** parts using a **subnet mask**:

```
IP Address:   192.168.1.100
Subnet Mask:  255.255.255.0  (or /24)

Network part: 192.168.1.0    ← same for all devices in LAN
Host part:          .100     ← unique per device
```

- `/24` = 256 addresses (254 usable)
- `/16` = 65,536 addresses
- `/8`  = 16,777,216 addresses

---

## Key Device: The Router

| Feature | Switch (Layer 2) | Router (Layer 3) |
|---|---|---|
| Address used | MAC address | IP address |
| Scope | Local network | Between networks |
| Makes decisions based on | Frame | Packet |
| Connects | Same network | Different networks |

---

## Where It Sits

```
Layer 4  Transport     ← TCP/UDP segments
─────────────────────────────────────────
Layer 3  Network       ← IP Packets        ← YOU ARE HERE
─────────────────────────────────────────
Layer 2  Data Link     ← Ethernet Frames
Layer 1  Physical      ← Raw bits
```

> **Important relationship**: A Network Layer **packet** is *encapsulated inside* a Data Link Layer **frame** at each hop. The frame changes at every router; the packet stays the same end-to-end.

---

## Quick Summary

```
Data Link Layer  →  Delivers frames between  ADJACENT nodes (same network)
Network Layer    →  Delivers packets between  ANY two nodes  (across networks)
```

---

**References:**
- [Network Layer – Wikipedia](https://en.wikipedia.org/wiki/Network_layer)
- [IP Addressing & Subnetting – Cisco](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html)
- [How Routing Works – Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-routing/)
- [IPv4 Packet Structure – GeeksForGeeks](https://www.geeksforgeeks.org/introduction-and-ipv4-datagram-header/)