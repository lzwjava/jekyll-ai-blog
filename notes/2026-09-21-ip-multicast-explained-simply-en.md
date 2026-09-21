---
audio: false
generated: true
image: false
lang: en
layout: post
title: IP Multicast Explained Simply
translated: false
type: note
---

Question: What is IP multicast?

Answer: **IP multicast** means **one sender sends an IP packet to many receivers simultaneously**, without sending a separate copy to each receiver.

Think:

```text
Unicast:
                    ┌─ Client A
Server ─────────────┼─ Client B
                    └─ Client C
       3 separate packets

Multicast:
                    ┌─ Client A
Server ────────> [network]
                    ├─ Client B
                    └─ Client C
       1 logical stream, replicated by routers
```

The key idea is that the destination is **a multicast IP address representing a group**, not an individual machine.

### IPv4

Multicast addresses are:

```text
224.0.0.0 ~ 239.255.255.255
```

For example:

```text
239.1.2.3
```

A receiver says:

```text
"I want to receive traffic for 239.1.2.3"
```

Typically this is done using **IGMP**:

```text
Client ── IGMP Join ──> Router
                         │
Server ── UDP ─────────> 239.1.2.3
                         │
                         ├──> Client A
                         ├──> Client B
                         └──> Client C
```

Routers maintain multicast forwarding state and only forward the stream toward networks that have interested receivers.

### Why not just broadcast?

Broadcast:

```text
Server ──> EVERY machine on the subnet
```

Multicast:

```text
Server ──> ONLY machines that joined the group
```

So multicast is useful for things like:

* IPTV / live video
* service discovery
* market-data distribution
* routing protocols
* LAN streaming
* distributing the same data to many machines

### The important distinction

Multicast is **not**:

```text
TCP connection to N clients
```

It's usually:

```text
UDP packet
    ↓
destination = multicast group
    ↓
network replicates packets where necessary
```

This is why multicast can be extremely efficient for **1 → N** distribution.

One subtle point: **the Internet at large doesn't generally provide arbitrary end-to-end multicast**. Multicast is much more common inside controlled networks/datacenters, where the network infrastructure explicitly supports protocols such as **IGMP** and **PIM**.

If you're looking at this from a systems/networking angle, I can also walk through **one UDP multicast packet from `sendto()` → NIC → switch → IGMP → router → receivers**, including the actual packet headers.