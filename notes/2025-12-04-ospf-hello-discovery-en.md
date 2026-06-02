---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OSPF Neighbor Discovery via Hello
translated: false
type: note
---

Question: In OSPF, which packet type is used to discover neighbors?

Answer:
**A) Hello**

The Hello packet is used in OSPF for neighbor discovery and to maintain neighbor adjacency. It is sent periodically on OSPF-enabled interfaces (typically every 10 seconds on broadcast networks) to discover neighboring routers, verify bidirectional communication, and elect the Designated Router (DR) and Backup Designated Router (BDR). Once neighbors are discovered and move to further states using other packet types (e.g., DBD for Database Description, LSR for Link State Request, LSU for Link State Update).

- DBD, LSR, and LSU are used later in the adjacency formation and LSDB synchronization process, not for initial discovery.
