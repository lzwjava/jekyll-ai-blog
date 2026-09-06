---
audio: false
generated: true
image: false
lang: en
layout: post
title: MF Flag in IP Datagram Header
translated: false
type: note
---

Question: What does "MF" mean in an IP datagram header?

Answer:

**MF** stands for **More Fragments**.

It is a 1-bit flag in the **Flags field** of the IPv4 header. The Flags field is 3 bits total:

| Bit | Name | Meaning |
| ----- | ------ | --------- |
| 0 | Reserved | Always 0 |
| 1 | DF | Don't Fragment |
| 2 | **MF** | **More Fragments** |

**How MF works:**

- **MF = 1** → There are more fragments following this one. The receiver should keep waiting for additional fragments to reassemble the original datagram.
- **MF = 0** → This is the **last (or only) fragment**. The receiver knows the datagram is complete once all previous fragments arrive.

**Example scenario:**

If a large IP datagram is fragmented into 3 pieces:

- Fragment 1 → MF = 1 (more coming)
- Fragment 2 → MF = 1 (more coming)
- Fragment 3 → MF = 0 (last one)

The receiver uses the MF flag together with the **Fragment Offset** field to correctly reassemble the original data.

References:

- [RFC 791 – Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [IP Fragmentation – Wikipedia](https://en.wikipedia.org/wiki/IP_fragmentation)
