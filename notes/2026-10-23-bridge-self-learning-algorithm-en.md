---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bridge Self-Learning Algorithm
translated: false
type: note
---

Question: How does the network bridge (网桥) self-learning algorithm work?

Answer:

A network bridge uses a **self-learning algorithm** (also called *transparent bridging*) to build and maintain a **MAC address table** (forwarding table) dynamically — without any manual configuration.

---

### Core Data Structure

The bridge maintains a **MAC Address Table**:

| MAC Address | Port | Timestamp |
| --- | --- | --- |
| AA:BB:CC:DD:EE:01 | Port 1 | t=10s |
| AA:BB:CC:DD:EE:02 | Port 3 | t=12s |

---

### Step-by-Step Algorithm

**Step 1 — Frame arrives on a port**
The bridge receives a frame on, say, Port 1.

**Step 2 — Learn from Source MAC**
The bridge reads the **source MAC address** of the frame and records:

```
MAC Table: source_MAC → Port 1, timestamp = now
```

If the entry already exists, it simply refreshes the timestamp.

**Step 3 — Forward based on Destination MAC**
The bridge looks up the **destination MAC** in its table:

```
if dest_MAC in table:
    if dest_MAC.port == incoming_port:
        DROP  # same segment, no need to forward
    else:
        FORWARD to dest_MAC.port only  # unicast
else:
    FLOOD to all ports except incoming_port  # unknown dest
```

**Step 4 — Aging (Entry Expiry)**
Each entry has a TTL (typically **300 seconds**). If no frame from that MAC is seen within the timeout, the entry is deleted:

```
if now - timestamp > aging_time:
    remove entry
```

---

### Visual Flow

```
Frame arrives on Port 1
        │
        ▼
[Record src_MAC → Port 1]
        │
        ▼
  Lookup dest_MAC
   /           \
Found         Not Found
  │               │
  ▼               ▼
Forward to    FLOOD to all
dest port     other ports
```

---

### Key Properties

| Property | Detail |
| --- | --- |
| **No pre-config needed** | The table builds itself from traffic |
| **Flooding** | Used for unknown destinations (and broadcasts) |
| **Aging** | Prevents stale entries when devices move |
| **Loop risk** | Self-learning alone doesn't prevent loops → STP (Spanning Tree Protocol) is needed alongside it |

---

### Example Walkthrough

Assume a bridge with Ports 1, 2, 3 and an empty table:

1. Host A (Port 1) sends to Host B (Port 2): table learns `A→Port1`; B is unknown → floods Ports 2 & 3.
2. Host B replies: table learns `B→Port2`; A is now known → forwards **only** to Port 1.
3. All subsequent A↔B traffic is switched directly, never flooded.

This is why bridges start slow (lots of flooding) but become efficient quickly as the table fills.

References:

- [IEEE 802.1D - MAC Bridges Standard](https://www.ieee802.org/1/pages/802.1D.html)
- [Transparent Bridging - Cisco Documentation](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/5234-5.html)
- [How Network Bridges Work - Cloudflare Learning](https://www.cloudflare.com/learning/network-layer/what-is-a-network-bridge/)
