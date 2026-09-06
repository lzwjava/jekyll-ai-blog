---
audio: false
generated: true
image: false
lang: en
layout: post
title: "0x8100: Assigned EtherType Origin"
translated: false
type: note
---

Question: Why is the TPID value `0x8100` in 802.1Q, and where does this number come from?

Answer:

**`0x8100`** is simply an **assigned EtherType value** — a unique hexadecimal identifier registered with the **IEEE (Institute of Electrical and Electronics Engineers)** to identify a specific protocol inside an Ethernet frame.

---

**Understanding EtherType:**

Every Ethernet frame has an **EtherType field** (2 bytes / 16 bits) that tells the receiving device:
> *"What kind of data is inside this frame?"*

| EtherType | Protocol |
|---|---|
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| **`0x8100`** | **802.1Q VLAN-tagged frame** |
| `0x8847` | MPLS |

These values are **not mathematically derived** — they are simply **reserved and registered numbers**, like area codes or country codes. IEEE/IANA acts as the authority that assigns them to avoid conflicts.

---

**So why specifically `0x8100`?**

- When the 802.1Q standard was being developed in the **late 1990s**, the IEEE needed a unique EtherType to signal *"this frame carries a VLAN tag"*
- `0x8100` was the value **allocated by IEEE** for this purpose — it was an available slot in the EtherType registry at that time
- There is no deeper mathematical meaning — it's purely a **bureaucratic assignment**

---

**How it works in practice:**

```
Normal Ethernet Frame:
[ Dst MAC | Src MAC | EtherType(0x0800) | IP Payload ]

802.1Q Tagged Frame:
[ Dst MAC | Src MAC | 0x8100 | PCP+DEI+VID | EtherType(0x0800) | IP Payload ]
                       ↑
              "Hey! A VLAN tag follows me!"
```

When a switch sees `0x8100`, it knows the next 2 bytes are the VLAN tag (PCP + DEI + VID), not payload data. After the tag, the **original EtherType** (e.g., `0x0800` for IP) resumes normally.

---

**In short:** `0x8100` has no special mathematical origin — it's simply the unique ID that IEEE officially registered and assigned to 802.1Q when the standard was created, just like a product getting a barcode.

References:
- [EtherType - Wikipedia](https://en.wikipedia.org/wiki/EtherType)
- [IEEE Registration Authority - EtherType](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries)
- [IEEE 802.1Q Frame Format](https://en.wikipedia.org/wiki/IEEE_802.1Q#Frame_format)
