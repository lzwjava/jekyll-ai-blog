---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Switch Function and MAC Addresses
translated: false
type: note
---

Question: 1. What is the primary function of a switch in a network?
A) Routing packets between different networks
B) Forwarding frames based on MAC addresses
C) Providing IP addresses to hosts
D) Encrypting data traffic

2. (The user's answer: B)

Answer:

### Question 1
The correct answer is **B) Forwarding frames based on MAC addresses**.

A network switch operates primarily at **Layer 2 (Data Link layer)** of the OSI model. Its main function is to receive Ethernet frames, examine the destination MAC address in the frame header, and forward the frame only to the port associated with that MAC address (or broadcast if unknown). This process reduces collisions, segments the network, and improves efficiency within a single local area network (LAN).

#### Why the other options are incorrect:
- **A) Routing packets between different networks**: This is the primary function of a **router** (Layer 3 device), which forwards IP packets based on IP addresses and routes between different subnets or networks.
- **C) Providing IP addresses to hosts**: This is performed by a **DHCP server**, which can run on various devices (routers, servers, etc.), but not a core function of a switch.
- **D) Encrypting data traffic**: Encryption is handled at higher layers (e.g., by protocols like IPsec, TLS) or by specialized security devices, not by standard switches.

### Question 2
Your selected answer **B** is **correct**.

Well done! Switches are fundamental Layer 2 devices that build and use MAC address tables (via learning and flooding) to intelligently forward frames within the same broadcast domain.
