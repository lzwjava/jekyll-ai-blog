---
audio: false
generated: true
image: false
lang: en
layout: post
title: Key Characteristics of IP Networks
translated: false
type: note
---

Question: What are the key characteristics of an IP network?

Answer:

An **IP network** is fundamentally a network where devices communicate using the **Internet Protocol (IP)** to identify endpoints and forward packets across multiple interconnected networks.

The most important characteristics are:

### 1. Packet-switched

Data is divided into **packets**, rather than reserving a dedicated physical path.

```text
Application data
      ↓
+-----+-----+-----+
| pkt | pkt | pkt |
+-----+-----+-----+
   ↓     ↓     ↓
 Router Router Router
```

Each packet can potentially take a different route.

This is fundamentally different from a circuit-switched telephone network.

---

### 2. Address-based

Every IP interface gets an IP address.

IPv4:

```text
192.168.1.10
```

IPv6:

```text
2001:db8::10
```

The address has two conceptual parts:

```text
IP address
   │
   ├── network prefix
   │
   └── host/interface part
```

For example:

```text
192.168.1.10/24

network: 192.168.1.0/24
host:    10
```

This allows routers to aggregate destinations into **prefixes** rather than maintaining an entry for every individual machine.

---

### 3. Routers forward packets

The central operation of an IP network is essentially:

```text
packet arrives
     ↓
look at destination IP
     ↓
lookup routing table
     ↓
choose next hop
     ↓
forward packet
```

A simplified routing table:

```text
Destination       Next hop
10.0.0.0/8        router A
172.16.0.0/12     router B
0.0.0.0/0         router C
```

The router performs **longest-prefix matching**.

For example:

```text
10.123.45.6
```

matches both:

```text
10.0.0.0/8
10.123.0.0/16
```

so `/16` wins.

---

### 4. Connectionless at the IP layer

IP itself does **not** establish a connection before sending packets.

There is no:

```text
connect()
handshake()
reserve path()
```

at the IP layer.

You simply send:

```text
src IP → dst IP
```

and routers independently forward the packet.

This is why IP is called a **connectionless datagram protocol**.

TCP provides connection-oriented behavior **on top of IP**:

```text
Application
     ↓
    TCP
     ↓
     IP
     ↓
 Ethernet / Wi-Fi
```

---

### 5. Best-effort delivery

This is one of the most important characteristics.

IP basically says:

> I'll try to deliver your packet, but I don't guarantee it.

IP does **not inherently guarantee**:

* delivery
* ordering
* duplicate suppression
* retransmission
* bandwidth
* latency
* congestion-free operation

So packets can be:

```text
lost
duplicated
delayed
reordered
```

TCP handles many of these problems above IP.

---

### 6. Internetworking

The "I" in **IP** is important.

IP was designed to connect **different networks**.

```text
LAN A
  │
Router
  │
Internet
  │
Router
  │
LAN B
```

The underlying networks don't have to be identical:

```text
Ethernet
Wi-Fi
fiber
4G/5G
satellite
datacenter fabric
...
```

IP provides a common layer above them.

That's the key idea behind **internetworking**.

---

### 7. Hierarchical addressing

IP addresses are hierarchical rather than flat.

For example:

```text
13.107.0.0/16
```

means, conceptually:

```text
13.107
   ↓
network/prefix

remaining bits
   ↓
individual interfaces/subnets
```

This hierarchy is what makes Internet-scale routing possible.

Imagine the Internet had to maintain:

```text
8 billion devices
```

as individual routing entries.

That would be terrible.

Instead, routers can often say:

```text
13.0.0.0/8 → AS X
```

and aggregate huge numbers of addresses.

---

### 8. IP is layered

A useful mental model is:

```text
┌─────────────────────┐
│ Application         │ HTTP, DNS, SSH
├─────────────────────┤
│ Transport           │ TCP, UDP, QUIC
├─────────────────────┤
│ Internet            │ IPv4 / IPv6
├─────────────────────┤
│ Link                │ Ethernet, Wi-Fi
├─────────────────────┤
│ Physical            │ copper, fiber, radio
└─────────────────────┘
```

IP doesn't care whether the packet is physically traveling through Wi-Fi or fiber.

It sees an abstraction like:

```text
src IP
   ↓
destination IP
   ↓
forward packet
```

---

### 9. IP networks are distributed

There is no single central router controlling the Internet.

Instead:

```text
           ISP A
          /     \
       ISP B    ISP C
        |         |
      AS X       AS Y
        \         /
         Internet
```

Different networks operate independently and exchange routing information.

At the global level, **BGP** is used to exchange reachability information between autonomous systems.

---

### The essence

If you reduce IP networking to a few principles:

```text
             IP network
                 │
       ┌─────────┴─────────┐
       │                   │
 hierarchical          packet
 addressing            forwarding
       │                   │
       └─────────┬─────────┘
                 ↓
       destination IP
                 ↓
        routing decision
                 ↓
           next hop
                 ↓
           next router
```

And the philosophical design is:

**IP provides a simple, scalable, connectionless, best-effort packet-delivery abstraction over heterogeneous underlying networks.**

That simplicity is actually one of the reasons IP scaled from small research networks into the global Internet.

I can next walk through **one packet from your laptop → home router → ISP → Google server**, including Ethernet headers, IP headers, routing tables, NAT, and where TCP/QUIC fits.
