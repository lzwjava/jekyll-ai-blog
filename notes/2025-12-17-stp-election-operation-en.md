---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: STP Election and Operation Process
translated: false
type: note
---

Question: What is the Spanning Tree Protocol (STP) election and operation process, and why is the provided summary confusing or hard to understand?

Answer:

Spanning Tree Protocol (STP) is a Layer 2 protocol that prevents loops in Ethernet networks with redundant links by creating a loop-free logical topology. The provided summary is mostly accurate but can be confusing due to oversimplification and minor inaccuracies (e.g., all switches don't continuously send BPDUs every 2 seconds claiming to be root—only during initial convergence or changes). Here's a clear, step-by-step explanation of the classic IEEE 802.1D STP process:

### 1. Initial State and BPDU Exchange
- When switches boot up or new links come online, **every switch initially assumes it is the Root Bridge**.
- Each switch sends **Configuration BPDUs** (Bridge Protocol Data Units) out all active ports. These BPDUs contain:
  - The sender's Bridge ID (BID): Priority (default 32768) + MAC address (lower is better).
  - The assumed Root Bridge ID (initially its own BID).
  - Path cost to the root (initially 0).
  - Sender's port details.
- BPDUs are sent every **Hello Time** (default 2 seconds), but only the elected Root Bridge continues sending them regularly once convergence is complete. Non-root switches relay superior BPDUs.

### 2. Superior vs. Inferior BPDUs
- A **superior BPDU** has better (lower) information:
  - Lower Root BID, **or**
  - Same Root BID but lower path cost to root, **or**
  - Same root and cost but lower sender BID, **or**
  - Same above but lower sender port priority/ID.
- When a switch receives a **superior BPDU** on a port:
  - It stops claiming to be root.
  - It updates its own stored root information.
  - It forwards (relays) the superior information out its other ports (with updated cost).
- Inferior BPDUs are ignored or used to confirm designated roles.

This exchange converges the network until all switches agree on the same Root Bridge.

### 3. Root Bridge Election
- The switch with the **lowest BID** becomes the Root Bridge.
- BID = Priority (configurable, multiples of 4096) + MAC address.
- Tiebreaker: Lowest MAC address if priorities are equal.
- The Root Bridge has all its ports as **Designated Ports** (forwarding).

### 4. Port Role Election on Non-Root Switches
After root election:
- **Root Port** (one per non-root switch): The port with the lowest cumulative path cost to the Root Bridge.
  - Tiebreakers: Lowest sender BID → lowest sender port ID.
  - Root Ports forward traffic toward the root.
- **Designated Port** (one per network segment/LAN link): The port sending the best (superior) BPDU on that segment.
  - The switch closest to the root (or with lowest BID if tie) wins.
  - Designated Ports forward traffic away from the root.
- **Non-Designated (Blocked) Ports**: All remaining ports that would create loops.
  - They listen for BPDUs but do not forward data frames (blocking state).

All Root and Designated Ports eventually forward; blocked ports stay blocked.

### 5. Topology Change Notification (TCN) Process
- When a topology change occurs (e.g., link failure, port up/down affecting forwarding):
  - The detecting non-root switch sends a **TCN BPDU** out its Root Port.
  - Upstream switches acknowledge with TCA (in next BPDU) and relay the TCN toward the root.
- The Root Bridge receives the TCN, sets the **Topology Change (TC) flag** in its Configuration BPDUs, and floods them network-wide.
- All switches receiving TC-flagged BPDUs shorten their MAC address table aging time from 300 seconds to Forward Delay (default 15 seconds).
- This flushes stale MAC entries quickly, allowing faster relearning after the change.

The summary you provided matches this closely, but point 1 is slightly misleading—ongoing BPDUs are mainly from the root (relayed by others), not all switches constantly claiming root status.

Here are visual diagrams to help understand:
























References:

- https://www.networkacademy.io/ccna/spanning-tree/how-stp-works
- https://www.geeksforgeeks.org/root-bridge-election-in-spanning-tree-protocol/
- https://networklessons.com/spanning-tree/spanning-tree-topology-change-notification-tcn
- https://www.networkacademy.io/ccna/spanning-tree/stp-topology-changes
