---
audio: false
generated: true
image: false
lang: en
layout: post
title: MAC Address Length in Ethernet
translated: false
type: note
---

Question: In the IEEE 802.3 MAC frame structure, there are two addresses: the source address and the destination address. Both of these addresses are how many bits long?

A. 16-bit  
B. 32-bit  
C. 48-bit  
D. 96-bit  

Answer: 

**C. 48-bit**

**Detailed explanation:**

In the IEEE 802.3 standard (Ethernet), the MAC frame format includes the following main fields in order:

- **Preamble** (7 bytes) + **Start Frame Delimiter (SFD)** (1 byte)  
- **Destination MAC Address** — **6 bytes (48 bits)**  
- **Source MAC Address** — **6 bytes (48 bits)**  
- **Length/Type** field — 2 bytes  
- **Data** (payload) — 46–1500 bytes (padded if necessary)  
- **Frame Check Sequence (FCS)** — 4 bytes  

Both the **destination address** and **source address** fields are fixed at **6 bytes**, which equals **48 bits**.  

These 48-bit addresses are commonly called **MAC addresses** (Media Access Control addresses). They are globally unique hardware addresses assigned to network interface controllers (NICs), usually expressed in hexadecimal format (e.g., 00:1A:2B:3C:4D:5E).

**Why not the other options?**

- **A. 16-bit**: Too short — used in some older or specialized protocols, not Ethernet  
- **B. 32-bit**: Matches IP addresses (IPv4), but MAC addresses are always 48 bits in Ethernet  
- **D. 96-bit**: No standard Ethernet MAC frame uses 96-bit addresses  

Your answer (C) was **correct**.

References:  

- None (standard IEEE 802.3 / Ethernet specification knowledge)