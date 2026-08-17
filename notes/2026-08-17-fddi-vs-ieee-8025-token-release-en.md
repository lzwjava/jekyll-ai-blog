---
audio: false
generated: true
image: false
lang: en
layout: post
title: FDDI vs IEEE 802.5 Token Release
translated: false
type: note
---

This question is from a networking exam. Let me explain the key concept clearly.

## The question

Both **FDDI** and **IEEE 802.5** use a token-passing ring protocol — but they differ in **when the token is released** after sending a frame. Which statement is correct?

**Answer: C**

> FDDI: after the sending station finishes transmitting its frame, it can **immediately** transmit a new token.
> IEEE 802.5: a new token is only transmitted when the sent frame **returns** to the sending station.

## Why the difference matters

**IEEE 802.5 (Token Ring)** — "single token" operation:
- A station must wait until the frame it sent travels all the way around the ring and comes back to it.
- Only then does the station remove (strip) its frame and release a new token.
- Consequence: at any moment there is **at most one frame on the ring**, which wastes bandwidth on high-speed rings.

**FDDI (Fiber Distributed Data Interface)** — "early token release" (ETR):
- A station transmits its frame(s) and then **immediately** releases the token — it doesn't wait for the frame to loop back.
- Consequence: **multiple frames can circulate on the ring simultaneously**, greatly improving utilization — which is why FDDI can efficiently run at 100 Mbps over rings up to 100 km.

## Breaking down the wrong options

- **A** — Wrong: 802.5 does *not* release immediately; it waits for the frame to return.
- **B** — Wrong: it has the behavior backwards (802.5 waits, but FDDI does *not* wait).
- **D** — Wrong: FDDI releases the token *after* sending the frame (immediately), not *while* sending it; and 802.5 doesn't release it immediately after sending.

## Quick facts from the explanation (commonly tested)

- FDDI uses the IEEE 802.5 token ring MAC protocol as a basis, plus IEEE 802.2 (LLC).
- Data rate: **100 Mbps**; up to **1000 nodes**; ring length up to **100 km**.
- Supports **dual ring** (counter-rotating) topology with fault tolerance.
- Supports **synchronous and asynchronous** traffic with dynamic bandwidth allocation (via the *timed token* protocol — stations hold the token no longer than a target rotation time).

So the core takeaway: **FDDI = release token immediately after sending (early token release); 802.5 = release token only when the frame returns.**