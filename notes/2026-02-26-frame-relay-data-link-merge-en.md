---
audio: false
generated: true
image: false
lang: en
layout: post
title: Frame Relay Merges Data Link Layers
translated: false
type: note
---

Question: In Frame Relay, the concept of layers in switching equipment is simplified by merging the data link layer and the network layer.

(Determine whether the statement is true or false, and fill in the blank with the correct layer name from the reference answer perspective.)

Answer:

The statement is **true**.

Frame Relay indeed "fades out / simplifies" the strict layering concept on switching devices by merging / combining functions of the **data link layer** (Layer 2) and the **network layer** (Layer 3).

The correct word to fill in the blank is **数据链路** (data link).

### Explanation:

Traditional packet-switched networks (such as X.25) clearly separate:

- Layer 2: LAPB (framing, error control, flow control)
- Layer 3: X.25 PLP (virtual circuit management, routing, multiplexing)

Frame Relay removes most Layer 3 functions from the network (especially inside the carrier network). The Frame Relay switches only look at the DLCI (Data Link Connection Identifier) in the frame header to forward frames — this is essentially a Layer 2 forwarding decision.

However, DLCI has multiplexing and virtual circuit significance similar to Layer 3 virtual circuits. Therefore, Frame Relay is commonly described as having "merged" or "blurred the boundary" between the data link layer and the network layer.

So the standard textbook description in many Chinese teaching materials is:

Frame Relay淡化了交换设备上的层次概念，将**数据链路层**和网络层进行了融合。

The blank should be filled with **数据链路** (or 数据链路层).

References:

- None (standard knowledge in computer networking textbooks, especially in Chinese higher education materials for computer networks)
