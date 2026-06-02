---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: X.25 Packet Switching Protocol Explained
translated: false
type: note
---

Question: What is X.25?

Answer:

**X.25** is an **ITU-T standard** protocol suite (originally developed by CCITT) for **packet-switched data communication networks**. It was the dominant wide-area networking protocol from the late 1970s through the 1990s and is still used in some niche applications today.

X.25 defines a complete **three-layer protocol stack** for reliable, connection-oriented packet switching over public data networks (PDNs):

1. **Physical layer**
   - Based on X.21, X.21bis (V.24/RS-232 compatible), or other interfaces
   - Specifies electrical and mechanical characteristics for DTE–DCE connection

2. **Link layer** (Layer 2)
   - **LAPB** (Link Access Procedure Balanced)
   - A bit-oriented HDLC-derived protocol
   - Provides reliable, error-free, sequenced frame delivery between DTE and DCE using numbering, acknowledgments, retransmissions, and error checking

3. **Packet layer** (Layer 3)
   - The core of X.25
   - Provides **virtual circuit** service (both switched virtual circuits – SVCs – and permanent virtual circuits – PVCs)
   - Main functions:
     - Call setup / call clearing
     - Data transfer with sequencing and flow control
     - Multiplexing of multiple logical channels over a single physical link
     - End-to-end error recovery and flow control (windowing)
     - Packet sizes typically 128, 256, 512, or 1024 bytes (negotiable)
   - Uses modulo-8 or modulo-128 sequence numbering

**Key characteristics of X.25:**

- **Connection-oriented** — requires call setup before data transfer
- **Reliable** — guarantees in-order, error-free delivery (both link layer and packet layer contribute)
- **Slow** — significant overhead from acknowledgments and retransmissions at every hop
- **High reliability on poor lines** — designed for noisy analog lines of the 1970s–1980s
- **Low throughput** — typical speeds were 9.6 kbit/s to 64 kbit/s (rarely higher)
- **Expensive** — charged per packet and per call duration in most public networks

**Main related ITU-T recommendations (X-series):**

- X.25 — Interface between DTE and DCE for terminals operating in the packet mode
- X.3 — PAD parameters
- X.28 — DTE–PAD interface (asynchronous terminal to PAD)
- X.29 — PAD–host communication protocol
- X.121 — International numbering plan for public data networks
- X.75 — Internetworking between packet-switched networks

**Historical context and decline:**

- Dominant in the 1980s–early 1990s for financial transactions (ATMs, credit card terminals), airline reservation systems, and early internet access in many countries
- Largely replaced in the mid-1990s onward by:
  - Frame Relay (less overhead, higher speed)
  - ATM
  - IP / MPLS / Internet-based VPNs
- Still exists in some legacy systems (e.g., certain banking networks, SCADA, air traffic control backups, and some countries' public X.25 networks)

In summary:
X.25 was the first widely deployed **international standard for packet switching**, providing reliable virtual circuits over inherently unreliable lines, but its heavy protocol overhead made it inefficient for modern high-speed networks.

References:

- None (standard ITU-T X.25 recommendation and historical networking knowledge)
