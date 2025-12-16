---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding STP Port Roles
translated: false
type: note
---

Question: How to understand Spanning Tree Protocol (STP) port roles?

Answer: 

Spanning Tree Protocol (STP) prevents loops in Ethernet networks with redundant paths by electing a root bridge and assigning specific roles to each switch port. These roles determine whether a port forwards traffic, blocks it, or serves a special purpose. Here's a clear breakdown:

### Key Port Roles in STP

1. **Root Port**  
   - Exists **only on non-root switches** (every switch except the root bridge has exactly one root port).  
   - It is the **best port** (lowest cumulative path cost) on that switch to reach the root bridge.  
   - Role: **Forwarding** – carries traffic toward the root bridge.  
   - How it's chosen: The port with the lowest root path cost. If costs tie, it uses tiebreakers (lowest sender bridge ID, sender port ID, etc.).

2. **Designated Port**  
   - Exists on **every network segment** (each link between two switches or a switch and a segment with end devices).  
   - It is the port that **forwards traffic away from the root bridge** toward the segment (leaves/hosts).  
   - On the **root bridge itself**: All active ports are designated ports (since the root has no root port).  
   - On non-root switches: Some ports become designated for their attached segments.  
   - Role: **Forwarding**.  
   - How it's chosen: The port on the segment with the lowest root path cost (i.e., the switch closest to the root "wins").

3. **Blocked Port** (also called Alternate or Non-Designated Port)  
   - These are ports on redundant links that are **not chosen** as root or designated.  
   - Role: **Blocking** – listens for BPDUs (Bridge Protocol Data Units) to detect topology changes but **does not forward data traffic**.  
   - Purpose: Prevents loops. If the topology changes (e.g., a link fails), a blocked port can transition to forwarding.

### Path Costs (Classic STP values – IEEE 802.1D)
These are the default costs used to calculate the best paths:

- 10 Mbps: cost 100  
- 100 Mbps: cost 19  
- 1 Gbps: cost 4  
- 10 Gbps: cost 2  

(Note: Modern Rapid STP uses different scaling where 10 Gbps = 2,000, but the concept remains the same.)

### Simple Example
Imagine three switches: A (root), connected redundantly to B and C, and B connected to C.

- On A (root): Both ports to B and C → **Designated** (forwarding).  
- On B: Port toward A → **Root Port** (best path to root). Port toward C → likely **Designated** (if B is closer to root than C).  
- On C: Port toward A → **Root Port**. Port toward B → **Blocked** (to prevent loop).

### Quick Way to Remember
- Root bridge: "I'm the boss – all my ports are **designated** (sending traffic out)."  
- Non-root switches: "I pick one **root port** (my uplink to the boss) and compete to be **designated** on downstream segments."  
- Losers on redundant links: "**Blocked** – stay quiet unless something breaks."

Understanding these roles helps visualize how STP creates a loop-free logical tree while maintaining redundancy for failover.