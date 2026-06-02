---
audio: false
generated: true
image: false
lang: en
layout: post
title: Self Learning in Ethernet Switches
translated: false
type: note
---

**Question:** An Ethernet switch is a plug-and-play device that gradually builds its forwarding table using the "________" algorithm. (Reference answer: Self-learning)

**Answer:**

The correct answer is **Self-learning (自学习)** algorithm.

---

## What is the Self-Learning Algorithm in Ethernet Switches?

An Ethernet switch is a plug-and-play device, meaning it requires **no manual configuration** to start working. It automatically builds its MAC address forwarding table (also called the CAM table) using the **self-learning algorithm**. Here is a comprehensive explanation:

---

### Core Concept

A switch dynamically builds its MAC address table by examining the **source MAC addresses** of frames received on a port. The switch forwards frames by searching for a match between the destination MAC address in a frame and an entry in the MAC address table.

---

### How the Self-Learning Algorithm Works — Step by Step

**Step 1 — Learn:** When a frame arrives, the switch examines the source MAC address and updates its MAC address table, recording the MAC address and the port it came from.

**Step 2 — Forward/Filter Decision:** The switch decides where to forward the frame based on the destination MAC address.

**Step 3 — Forward:**
- If the destination MAC is in the table (known unicast), the switch forwards the frame only to the correct port.
- If the destination MAC is NOT in the table (unknown unicast), the switch **floods** a copy of the frame out of all ports except the one it came in on.

**Step 4 — Aging:** If a MAC address isn't seen again within a certain time (default 300 seconds), it is removed from the MAC address table.

This overall process is also called **"Flood and Learn."**

---

### Detailed Example

Consider a switch connected to three computers H1, H2, and H3. When H1 sends a frame to H2:
- The switch reads the **source MAC address** of H1 and records it along with the incoming interface in its MAC address table.
- Since the switch has no entry for H2's MAC address yet, it floods the frame out of all interfaces except the one it came from.
- When H2 replies, the switch learns H2's MAC address from the source field of H2's reply frame and records it.
- From this point on, frames between H1 and H2 are switched directly — H3 no longer sees them.

---

### Key Properties of the Self-Learning Algorithm

| Property | Description |
|---|---|
| **Plug-and-play** | No manual configuration needed |
| **Source-based learning** | Only learns from the **source** MAC address of incoming frames |
| **Dynamic entries** | Entries are automatically added and removed |
| **Flooding for unknowns** | Unknown destination MAC addresses trigger flooding |
| **Aging mechanism** | Stale entries are removed after a timeout period |

---

### Why Is It Called "Self-Learning"?

Switches employ a self-learning algorithm to populate their MAC address tables **automatically**, without any administrator intervention. Dynamic entries are learned automatically as the default behavior.

In contrast, routers compute their forwarding tables using routing algorithms and IP addresses, whereas switches learn their forwarding tables using **flooding, learning, and MAC addresses**.

---

### Summary

The self-learning algorithm allows an Ethernet switch to:
1. Start with an **empty** forwarding table
2. **Gradually** learn MAC address-to-port mappings as frames flow through it
3. Eventually forward frames **efficiently** without unnecessary flooding
4. **Adapt** automatically when devices are moved or disconnected (via aging)

This is why Ethernet switches are described as **plug-and-play** devices — the self-learning algorithm does all the work automatically.

**References:**

- [How Switches Work – Study CCNA](https://study-ccna.com/how-switches-work/)
- [Overview of Switching Logic – NetworkAcademy.IO](https://www.networkacademy.io/ccna/ethernet/switching-logic)
- [Ethernet Switching – MAC Address Table – Cisco Press](https://www.ciscopress.com/articles/article.asp?p=3089352&seqNum=6)
- [How Does a Switch Learn MAC Addresses – NetworkLessons](https://networklessons.com/switching/how-does-a-switch-learn-mac-addresses)
- [Troubleshoot LAN Switching Environments – Cisco](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/12006-chapter22.html)
