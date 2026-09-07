---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv4 Header Checksum Error Detection
translated: false
type: note
---

Question: How does IPv4 perform error checking, and which specific field is used for it?

Answer:

IPv4 uses a **Header Checksum** for error detection — but it only protects the **header**, not the payload/data.

---

## The Checksum Field

| Field | Size | Position in Header |
|---|---|---|
| Header Checksum | 16 bits (2 bytes) | Bytes 10–11 |

---

## How It Works

**Sending side (calculation):**
1. Set the checksum field to `0x0000`
2. Split the entire IPv4 header into **16-bit words**
3. Sum all 16-bit words using **one's complement addition**
4. Take the **one's complement** of the result → this is the checksum
5. Insert it into the checksum field

**Receiving side (verification):**
1. Split the received header into 16-bit words (including the checksum field)
2. Sum all of them
3. If the result is `0xFFFF` → header is **valid**; otherwise → **corrupted**, packet is discarded

---

## Key Points

- ✅ Protects: **header fields only** (TTL, source IP, dest IP, flags, etc.)
- ❌ Does NOT protect: **payload/data** (that's left to TCP/UDP checksums or upper-layer protocols)
- ♻️ **Recalculated at every router hop** — because TTL is decremented each hop, changing the header
- IPv6 **removed** the header checksum entirely, relying on layer-4 checksums instead

---

## Which Header Fields Are Covered

All fields in the 20-byte (minimum) header are checked:

```
Version | IHL | DSCP/ECN | Total Length
Identification | Flags | Fragment Offset
TTL | Protocol | [Checksum field itself, set to 0]
Source IP Address
Destination IP Address
Options (if any)
```

---

References:
- [RFC 791 – Internet Protocol](https://datatracker.ietf.org/doc/html/rfc791)
- [IPv4 Header – Wikipedia](https://en.wikipedia.org/wiki/IPv4#Header)
- [IPv4 Checksum Explained – GeeksforGeeks](https://www.geeksforgeeks.org/error-detection-in-computer-networks/)
