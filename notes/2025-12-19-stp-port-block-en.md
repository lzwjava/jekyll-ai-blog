---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: STP Port State Blocks Traffic
translated: false
type: note
---

Question: In Spanning Tree Protocol (STP), which port state blocks traffic to prevent loops?

Answer:

The correct answer is **D) Blocking**.

In Spanning Tree Protocol (STP), as defined in IEEE 802.1D, switch ports transition through several states to prevent bridging loops in a redundant Layer 2 network.

- **Blocking**: The initial state for all ports. In this state, the port **does not forward any traffic** (no user data frames are sent or received). It only listens for BPDUs (Bridge Protocol Data Units) to determine the network topology and detect potential loops. This state actively prevents loops by blocking data traffic on redundant paths.

- **Listening**: The port transitions here after Blocking if it is selected to become part of the active topology. It still does not forward user data but sends and receives BPDUs to participate in the root bridge and path selection process.

- **Learning**: The port begins to learn MAC addresses by populating the MAC address table but still does not forward user data traffic.

- **Forwarding**: The final active state where the port fully participates in frame forwarding.

The Blocking state is specifically responsible for blocking traffic on redundant links to eliminate loops while the topology converges.

References:

- [IEEE 802.1D Standard Overview](https://www.ieee802.org/1/pages/802.1D.html)
- [Cisco Spanning Tree Protocol Port States Documentation](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24062-146.html)
