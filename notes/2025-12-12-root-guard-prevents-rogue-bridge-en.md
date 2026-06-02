---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Root Guard Prevents Rogue Root Bridge
translated: false
type: note
---

Question: Which STP feature prevents a rogue device from becoming the root bridge in a network?
A) BPDU Guard
B) Root Guard
C) Loop Guard
D) UDLD

Answer:

The correct answer is **B) Root Guard**.

### Comprehensive explanation of each option

- **A) BPDU Guard**
  BPDU Guard is typically enabled on access ports (e.g., PortFast ports connected to end devices).
  If the port receives any BPDU (which should never happen from a legitimate PC/phone), BPDU Guard immediately puts the port into **err-disabled** state.
  Purpose: Prevents rogue or misconfigured switches connected to access ports from participating in STP and potentially causing topology issues.
  It does **not** directly prevent a rogue switch from becoming the root bridge — it simply shuts the port down if the rogue device sends BPDUs. The rogue device could still influence the topology on other ports or segments if connected elsewhere.

- **B) Root Guard**
  Root Guard is enabled on designated ports where the network administrator expects the current root bridge to remain superior (usually downlink ports toward access-layer switches).
  If a superior BPDU (one advertising a better/lower root bridge ID or lower path cost to the current root) is received on a Root Guard-enabled port, the port is placed into **root-inconsistent** state (effectively blocked) until the superior BPDUs stop arriving.
  Purpose: Explicitly prevents any device connected to that port from ever becoming the root bridge or advertising itself as having a better path to the root.
  This is the feature designed specifically to stop a rogue switch from taking over as the STP root bridge.

- **C) Loop Guard**
  Loop Guard protects against situations where a blocking port stops receiving BPDUs (e.g., due to unidirectional link failure) and mistakenly transitions to forwarding, creating a loop.
  When enabled, if a non-designated port stops receiving BPDUs, Loop Guard puts the port into **loop-inconsistent** state instead of letting it move to forwarding.
  Purpose: Prevents Layer 2 loops caused by unidirectional failures, not rogue root bridge takeovers.

- **D) UDLD (UniDirectional Link Detection)**
  UDLD detects and disables unidirectional links (fiber or copper) where one side can transmit but not receive, which can cause spanning-tree loops or blackholing.
  It works in normal and aggressive modes; in aggressive mode it will err-disable the port if the neighbor is not responding properly.
  Purpose: Prevents loops and traffic blackholes caused by physical-layer unidirectional failures, not rogue root bridge election.

### Summary Table

| Feature       | Prevents rogue device from becoming root? | Primary purpose                                      |
|---------------|--------------------------------------------|-------------------------------------------------------|
| BPDU Guard    | No (shuts port on any BPDU)                | Protect access ports from rogue switches              |
| Root Guard    | Yes                                        | Prevent downstream switch from ever becoming root     |
| Loop Guard    | No                                         | Prevent loops from unidirectional link failures       |
| UDLD          | No                                         | Detect and disable unidirectional physical unidirectional links |

Therefore, the feature that specifically prevents a rogue device from becoming the STP root bridge is **Root Guard (B)**.
