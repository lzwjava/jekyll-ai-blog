---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv6 Address Types and Uses
translated: false
type: note
---

Question: What are IPv6 unicast, multicast, and anycast addresses used for?

Answer: 

Each IPv6 address type serves distinct networking purposes:

## 1. Unicast Addresses
**Purpose**: Identify a single, specific network interface.

**Common Use Cases**:
- **Global Unicast Addresses (GUA)**: Publicly routable addresses for internet communication (similar to IPv4 public IPs).
- **Link-Local Addresses (fe80::/10)**: Used for communication within a single network segment; essential for neighbor discovery, router solicitation, and automatic configuration.
- **Unique Local Addresses (ULA, fc00::/7)**: Private addresses for internal networks, not routable on the public internet (similar to IPv4 private ranges like 192.168.x.x).
- **Loopback Address (::1)**: Used by a host to send packets to itself for testing and local services.

**Example**: When your computer accesses a website, it uses a global unicast address as the source, and the server's unicast address as the destination.

---

## 2. Multicast Addresses
**Purpose**: Enable one-to-many communication by delivering packets to all interfaces in a defined group.

**Common Use Cases**:
- **Network Discovery**: Protocols like Neighbor Discovery Protocol (NDP) use multicast (e.g., `ff02::1` for all nodes, `ff02::2` for all routers) to find devices on a local link.
- **Service Advertisement**: Devices announce services (printers, media servers) via multicast so clients can discover them automatically.
- **Streaming Media**: Efficiently distribute audio/video streams to multiple recipients without duplicating traffic.
- **Routing Protocols**: OSPFv3, RIPng, and PIM use multicast to exchange routing information.

**Prefix**: All multicast addresses start with `ff00::/8`.

---

## 3. Anycast Addresses
**Purpose**: Deliver packets to the *nearest* (topologically closest) interface among a group of interfaces sharing the same address.

**Common Use Cases**:
- **DNS Root Servers**: Multiple geographically distributed servers share the same anycast address; queries are automatically routed to the closest instance, improving latency and resilience.
- **Content Delivery Networks (CDNs)**: Route users to the nearest edge server for faster content delivery.
- **Gateway Redundancy**: Multiple routers can share an anycast address to provide failover without complex protocols.
- **Load Distribution**: Distribute requests across multiple service endpoints transparently.

**Note**: Anycast addresses use the unicast address format; the "anycast" behavior is configured via routing protocols, not the address itself.

---

## Key Comparison

| Address Type | Communication Model | Typical Use |
|--------------|---------------------|-------------|
| **Unicast** | One-to-One | End-to-end data transfer, web browsing, SSH |
| **Multicast** | One-to-Many | Service discovery, live streaming, routing updates |
| **Anycast** | One-to-Nearest | DNS, CDN, high-availability services |

> 💡 **Important**: IPv6 eliminates broadcast addresses entirely. Multicast addresses handle all former broadcast use cases more efficiently by allowing targeted group communication.

References:  

- [RFC 4291 - IPv6 Addressing Architecture](https://datatracker.ietf.org/doc/html/rfc4291)
- [Cisco - IPv6 Address Types Explained](https://www.cisco.com/c/en/us/support/docs/ip/ipv6/29199-ipv6-faq-29199.html)
- [Internet Society - IPv6 Address Types](https://www.internetsociety.org/resources/deploy360/ipv6/address-types/)