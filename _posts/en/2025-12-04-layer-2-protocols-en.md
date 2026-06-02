---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Layer 2 Protocols and Technologies
translated: false
type: note
---

Question: What things/protocols typically run on Layer 2 (Data Link Layer) of the OSI model?

Answer:

The **Data Link Layer (Layer 2)** is responsible for node-to-node delivery of frames over a physical link, error detection/correction, and medium access control. The following protocols, technologies, and functions typically operate at Layer 2:

### Common Layer 2 Protocols
- **Ethernet** (IEEE 802.3) – the most widely used LAN technology
- **Wi-Fi** (IEEE 802.11) – wireless LAN framing and medium access
- **PPP** (Point-to-Point Protocol) – used on serial links (e.g., WANs, dial-up)
- **HDLC** (High-Level Data Link Control) – serial link protocol
- **Frame Relay** – legacy WAN technology
- **ATM** (Asynchronous Transfer Mode) – cell-based Layer 2 protocol
- **MPLS** (Multiprotocol Label Switching) – often considered Layer 2.5, but labels are inserted at Layer 2
- **LLDP** (Link Layer Discovery Protocol) – neighbor discovery (Cisco uses CDP instead)
- **STP** (Spanning Tree Protocol) and its variants (RSTP, MSTP) – prevents Layer 2 loops
- **LACP** (Link Aggregation Control Protocol, part of 802.1AX/802.3ad) – EtherChannel/port-channel negotiation
- **ARP** (Address Resolution Protocol) – technically operates between Layer 2 and Layer 3 (resolves IP to MAC), but uses Layer 2 frames

### Layer 2 Technologies & Concepts
- **MAC addresses** (48-bit hardware addresses)
- **Switches** and **bridges** – primary Layer 2 devices
- **VLANs** (802.1Q tagging)
- **MAC address table** (CAM table) learning and forwarding
- **Frame encapsulation** (Ethernet frames, Wi-Fi frames, etc.)
- **Error detection** (via FCS – Frame Check Sequence using CRC)
- **Flow control** (e.g., Ethernet pause frames)

### Summary Table

| Category              | Examples                                      |
|-----------------------|-----------------------------------------------|
| Wired LAN             | Ethernet (802.3)                              |
| Wireless LAN          | Wi-Fi (802.11)                                |
| WAN/Serial            | PPP, HDLC, Frame Relay                        |
| Switching protocols   | STP, RSTP, LACP, LLDP/CDP                     |
| VLAN tagging          | 802.1Q                                        |
| Addressing            | MAC addresses, ARP                            |

In short: **Anything that deals with MAC addresses, frames (not packets), switches, and physical-link-specific framing is Layer 2.**
Layer 3 (e.g., IP, ICMP, routing protocols) runs on top of these Layer 2 protocols inside the frame payload.
