---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Spanning Tree Protocol Overview
translated: false
type: note
---

Question: What is the Spanning Tree Protocol (STP) and can you provide a comprehensive introduction to it?

Answer:

The Spanning Tree Protocol (STP) is a Layer 2 network protocol defined in IEEE 802.1D that prevents loops in Ethernet networks built with redundant links. Loops are dangerous because they cause broadcast storms, MAC address table instability, and can bring an entire switched network down in seconds. STP solves this by automatically disabling redundant paths while keeping full connectivity, creating a logical loop-free tree topology that “spans” all switches in the network.

### Key Concepts and Goals
- Goal: Ensure exactly one logical path between any two nodes in the Layer 2 domain while allowing physical redundancy for fault tolerance.
- When a link or switch fails, STP automatically reconfigures the topology (convergence) to use previously blocked paths.
- Operates transparently to end devices (PCs, servers, etc.) – they see only one active path.

### Core Components of STP (Original 802.1D)
1. **Bridge ID (BID)**
   8 bytes: 2-byte Bridge Priority (default 32768) + 6-byte MAC address).
   Lower BID = more likely to become Root Bridge.

2. **Root Bridge**
   The “reference point” of the entire spanning-tree topology.
   Every other switch calculates its best path toward the Root.
   Only one Root Bridge per network (or per VLAN in later versions).

3. **Path Cost**
   Cost of traversing a link, based on bandwidth (IEEE 802.1D-1998 values):
   - 10 Mbps → 100
   - 100 Mbps → 19
   - 1 Gbps → 4
   - 10 Gbps → 2
   (Modern “short mode” in 802.1t uses smaller numbers: 1G = 20 000, 10G = 2 000, etc.)

4. **Port Roles**
   - Root Port (RP): Best path toward the Root Bridge on each non-root switch (lowest cumulative path cost). Only one per switch (except Root).
   - Designated Port (DP): Port that forwards traffic toward the Root on each LAN segment. Only one per segment.
   - Blocked Port (Alternate/Backup): All other ports – they listen but do not forward any traffic (prevents loops).

5. **Port States** (original 802.1D – very slow convergence)
   - Blocking → Listening → Learning → Forwarding (20–50 seconds total)
   - Disabled

### STP Election and Operation Process
1. Every switch starts believing it is the Root and sends Bridge Protocol Data Units (BPDUs) out all ports every 2 seconds (Hello Time).
2. When a switch receives a superior BPDU (lower Root BID, or same Root but lower cost/sender BID/port priority), it stops claiming to be Root and starts forwarding that superior BPDU.
3. Root Bridge election: Lowest BID wins. Tiebreaker is lowest MAC address.
4. Every non-root switch chooses:
   - One Root Port (lowest cost path to Root)
   - Designated Ports for each segment it is attached to
   - All remaining ports become Blocked
5. Topology Change Notification (TCN) process informs the Root, which then shortens MAC address aging for faster recovery.

### Major Improvements Over the Years

| Version                  | Year | Key Features                                                                 | Convergence Time |
|--------------------------|------|------------------------------------------------------------------------------|------------------|
| Original STP (802.1D)    | 1990 → 1998 | Basic loop prevention, slow port states                                       | 30–50 seconds    |
| Rapid STP (RSTP, 802.1w) | 2001 | Alternate/Backup ports, proposal/agreement, fast transition                  | < 1–3 seconds    |
| Per-VLAN STP (PVST/PVST+) | Cisco | One STP instance per VLAN                                                    | Same as base     |
| Rapid PVST+              | Cisco | RSTP per VLAN                                                                | Sub-second       |
| Multiple STP (MSTP, 802.1s)| 2002 | Maps many VLANs to few instances, interoperable with RSTP                     | Sub-second       |

### RSTP (802.1w) Major Enhancements
- Only three port states: Discarding, Learning, Forwarding (Blocking+Listening+Disabled merged into Discarding)
- Ports can transition immediately when topology changes
- Proposal/Agreement handshake for instant Designated port activation
- Backup and Alternate port roles defined explicitly
- UplinkFast, BackboneFast, and PortFast features integrated

### Common Extensions and Features (mostly Cisco)
- PortFast – Immediately puts access ports into Forwarding (for end devices)
- BPDU Guard – Shuts down PortFast ports that receives BPDU (prevents rogue switches)
- BPDU Filter – Stops sending/receiving BPDUs (rarely used)
- Root Guard – Prevents a port from becoming Root Port if superior BPDUs arrive
- Loop Guard – Prevents a port from going to Forwarding if BPDUs stop arriving

### Example Topology (simple)

```
         [SW1 - Root]
        /    1G    \
   1G /            \ 1G
[SW2]              [SW3]
   \                /
    \   100M       /
     [SW4]------[SW5]
```

SW1 will be Root (assume lowest BID).
SW2 and SW3 will have their ports to SW1 as Root Ports.
The link SW2–SW4–SW5–SW3 will have the highest cost path, so one port on that segment (likely on SW4 or SW5) will be blocked.

### Summary Table of STP Timers (default)

| Timer             | Default Value | Meaning                                      |
|-------------------|---------------|----------------------------------------------|
| Hello Time        | 2 seconds     | BPDU transmission interval                   |
| Forward Delay     | 15 seconds    | Time spent in Listening + Learning (legacy)  |
| Max Age           | 20 seconds    | How long to keep old BPDU info before timing out |
| Message Age       | Increments    | Age field in received BPDUs                  |

In modern networks, almost everyone uses Rapid STP (802.1w) or its Cisco variants (Rapid PVST+, MSTP) because classic STP takes too long to converge after a failure.

STP is the foundation of Layer 2 redundancy in Ethernet networks. Even with newer technologies (TRILL, SPB, VXLAN with EVPN), understanding classic and rapid STP remains essential for any network engineer.

References:
- IEEE 802.1D-2004 Standard
- IEEE 802.1w-2001 (Rapid Spanning Tree Protocol)
- IEEE 802.1Q-2018 (includes MSTP)
- Cisco Press – “CCNP SWITCH 300-115 Official Cert Guide” (Chapters on STP)
