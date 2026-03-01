---
audio: false
generated: true
image: false
lang: en
layout: post
title: IEEE 802.1Q VLAN Tag Structure Explained
translated: false
type: note
---

Question: Provide a detailed extension and explanation of the structure of the VLAN Tag as defined in the IEEE 802.1Q standard, including the fields TPID and TCI with their sub-components.

Answer: 

The **VLAN Tag** (also called the 802.1Q tag) is a 4-byte (32-bit) field that is inserted into the Ethernet frame to support Virtual LANs (VLANs) as defined in the IEEE 802.1Q standard. It is placed between the Source MAC Address and the EtherType/Length field of the original Ethernet II frame.

The complete structure of the VLAN Tag is:

- **TPID – Tag Protocol Identifier** (16 bits / 2 bytes)  
  - Fixed value: **0x8100**  
  - This value identifies the frame as an IEEE 802.1Q-tagged frame.  
  - When a switch or other device sees EtherType = 0x8100, it knows the next 2 bytes contain VLAN-related control information and the real EtherType follows afterward.

- **TCI – Tag Control Information** (16 bits / 2 bytes)  
  The TCI field is further divided into three sub-fields:

  1. **PCP – Priority Code Point** (3 bits)  
     - Also known as the Class of Service (CoS) field.  
     - Values range from 0 to 7.  
     - Used to indicate the priority level of the frame (Quality of Service – QoS).  
     - Higher values generally mean higher priority (e.g., 7 = network control traffic, 5 = voice, 0 = best effort).  
     - This allows switches to apply different queuing and forwarding behaviors based on priority.

  2. **DEI – Drop Eligible Indicator** (1 bit)  
     - Formerly called **CFI** (Canonical Format Indicator) in earlier versions.  
     - In modern usage (after IEEE 802.1Q amendments), it is the **Drop Eligible Indicator**.  
     - 0 = frame is not drop-eligible (preferred traffic)  
     - 1 = frame is drop-eligible (can be dropped first during congestion)  
     - This bit is especially useful when the PCP value is mapped to a service class that supports drop precedence (similar to IP DiffServ’s ECN or ATM CLP bit).

  3. **VID – VLAN Identifier** (12 bits)  
     - The actual VLAN number.  
     - Range: 0 to 4095 (2¹² = 4096 possible values).  
     - Commonly used values:  
       - 0 = reserved (sometimes used for priority-tagged frames without a VLAN)  
       - 1 = default VLAN (often called the native VLAN on trunks)  
       - 2–4094 = user-assignable VLAN IDs  
       - 4095 = reserved  
     - The VID is the primary field that determines which VLAN the frame belongs to.

Full bit layout of the 32-bit VLAN Tag:

```
Bits:    15 14 13 12 11 10 9  8  7  6  5  4  3  2  1  0
         ┌──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┐  ← TPID (16 bits)
         │                 0x8100 (fixed)                 │
         └─────────────────────────────────────────────────┘
Bits:    15 14 13 12 11 10 9  8  7  6  5  4  3  2  1  0
         ┌───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┐  ← TCI (16 bits)
         │ PCP     │ DEI │          VID (12 bits)         │
         └─────────┴─────┴─────────────────────────────────┘
```

Total: 4 bytes = 32 bits = TPID (16 bits) + TCI (16 bits).

This tag enables:
- VLAN segmentation on a single physical link (trunking)
- Quality of Service differentiation
- Selective dropping during congestion

References:  

- None (standard knowledge based on IEEE 802.1Q specification)