---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RARP: MAC to IP Address Mapping"
translated: false
type: note
---

Question: What is the RARP protocol?

Answer: **RARP (Reverse Address Resolution Protocol)** is an old network protocol that lets a machine discover its **IP address from its MAC address**.

The key idea is the reverse of ARP:

```text
ARP:
    IP address ──────> MAC address

RARP:
    MAC address ─────> IP address
```

### Why did RARP exist?

Imagine a diskless workstation booting with almost no network configuration:

```text
NIC:
    MAC = 00:11:22:33:44:55

        |
        | "What's my IP?"
        v

RARP server:
    00:11:22:33:44:55 -> 192.168.1.42

        |
        v

Client:
    My IP = 192.168.1.42
```

The client sends a **RARP Request** at the Ethernet layer containing its MAC address. A RARP server, which has a table mapping MAC → IP, responds with the assigned IP.

### Packet flow

Conceptually:

```text
Client                         RARP Server
  |                                |
  |  RARP Request                  |
  |  "MAC = AA:BB:CC:DD:EE:FF"    |
  |------------------------------->|
  |                                |
  |  RARP Reply                    |
  |  "Your IP = 10.0.0.42"        |
  |<-------------------------------|
```

RARP operates directly over **Ethernet**, rather than using IP, because the machine doesn't know its IP yet.

### Why RARP disappeared

RARP was extremely limited:

* Only provided an IP address.
* Required a RARP server on the **same Ethernet broadcast domain**.
* Couldn't provide subnet mask, gateway, DNS, boot-server information, etc.
* Required manual MAC → IP mappings.

It was largely replaced by **BOOTP**, and then **DHCP**.

Modern equivalent:

```text
RARP:
    MAC ──────────────> IP

DHCP:
    MAC + DHCP request
           │
           ├── IP address
           ├── subnet mask
           ├── default gateway
           ├── DNS servers
           ├── lease duration
           └── other options
```

One subtle but useful distinction:

**RARP is not simply "ARP backwards."** ARP maps IP → MAC dynamically and is part of normal IP networking; RARP was a mechanism for a host that didn't yet know its own IP to obtain one from a server.

If you're learning this from packet captures, I can also walk through the **Ethernet frame + RARP header byte-by-byte** and show exactly what Wireshark would see.