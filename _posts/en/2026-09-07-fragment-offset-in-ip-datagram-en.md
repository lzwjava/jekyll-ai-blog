---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fragment Offset in IP Datagram
translated: false
type: note
---

Question: What is the Fragment Offset field in an IP datagram?

Answer:

The **Fragment Offset** field is a 13-bit field in the IPv4 header that indicates where in the original (unfragmented) datagram a particular fragment belongs.

**Key details:**

- **Size:** 13 bits
- **Unit:** Measured in units of **8 bytes** (64 bits), so the actual byte offset = field value × 8
- **Purpose:** Allows the destination host to reassemble fragments in the correct order, even if they arrive out of order

**How it works:**

When a router needs to fragment a large IP datagram (because it exceeds the MTU of the next link):
1. It splits the data into smaller fragments
2. Each fragment gets the **same Identification number** (so the destination knows they belong together)
3. Each fragment gets a **Fragment Offset** value indicating its position in the original data
4. All fragments except the last have the **More Fragments (MF) flag** set to 1

**Example:**

If an original datagram has 4000 bytes of data, split into 3 fragments:

| Fragment | Data bytes | Offset value (÷8) |
|---|---|---|
| 1st | 0–1479 | 0 |
| 2nd | 1480–2959 | 185 |
| 3rd | 2960–3999 | 370 |

The destination uses the offset values to reconstruct the original datagram in the correct order.

References:
- [RFC 791 – Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [Computer Networking: A Top-Down Approach – Kurose & Ross, Chapter 4](https://gaia.cs.umass.edu/kurose_ross/index.php)
