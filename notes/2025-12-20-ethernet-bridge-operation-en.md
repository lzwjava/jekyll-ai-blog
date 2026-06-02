---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ethernet Bridge Function and Operation
translated: false
type: note
---

Question: What is an Ethernet bridge? How does it work?

Answer:

An **Ethernet bridge** (also known as a network bridge) is a Layer 2 (Data Link layer) networking device that connects multiple Ethernet network segments into a single logical network. It filters and forwards Ethernet frames based on MAC addresses, reducing unnecessary traffic and collisions compared to hubs or repeaters.

### Key Characteristics

- Operates at **OSI Layer 2**, using MAC addresses (not IP addresses like routers).
- Creates one **broadcast domain** but separates **collision domains**.
- "Transparent" to devices—end stations are unaware of its presence.
- Historically used to extend Ethernet networks beyond cable length limits or to segment traffic for performance.
- Modern equivalent: Multiport bridges evolved into **network switches** (switches are essentially high-port-count bridges with hardware acceleration).

### How It Works

Ethernet bridges use a process called **transparent bridging** (IEEE 802.1D standard), involving learning, forwarding, filtering, and flooding:

1. **Learning**:
   - The bridge maintains a **forwarding table** (MAC address table or CAM table).
   - When a frame arrives on a port, the bridge records the **source MAC address** and the incoming port in its table.
   - Entries age out after a timeout (typically 300 seconds) if not refreshed.

2. **Forwarding/Filtering**:
   - For an incoming frame, the bridge checks the **destination MAC address**.
   - If the destination MAC is in the table and on a different port, it **forwards** the frame only to that port.
   - If the destination MAC is on the same incoming port, it **filters** (drops) the frame—no need to forward.
   - This reduces network congestion by sending traffic only where needed.

3. **Flooding**:
   - If the destination MAC is unknown, a broadcast, or multicast, the bridge **floods** the frame to all ports except the incoming one.

4. **Loop Prevention**:
   - Uses **Spanning Tree Protocol (STP)** to detect and block redundant paths, preventing broadcast storms in looped topologies.

### Example

- Segment A: Devices with MACs A1, A2 (connected to Port 1).
- Segment B: Devices with MACs B1, B2 (connected to Port 2).
- Device A1 sends a frame to B1.
- Bridge sees source A1 → learns A1 on Port 1.
- Destination B1 unknown → floods to Port 2.
- B1 replies → bridge learns B1 on Port 2 and forwards future traffic directly.

In practice, bridges were common in early Ethernet networks but have been largely replaced by switches, which perform the same functions faster and with more ports.

References:

- [Network bridge - Wikipedia](https://en.wikipedia.org/wiki/Network_bridge)
- [Bridges - How Ethernet Works | HowStuffWorks](https://computer.howstuffworks.com/ethernet12.htm)
- [What is a Network Bridge? - CBT Nuggets](https://www.cbtnuggets.com/blog/technology/networking/what-is-network-bridge)
- [Network bridge explained - Study CCNA](https://study-ccna.com/network-bridge-explained/)
