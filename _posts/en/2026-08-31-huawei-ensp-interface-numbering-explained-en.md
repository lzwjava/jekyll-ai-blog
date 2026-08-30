---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huawei eNSP Interface Numbering Explained
translated: false
type: note
---

Question: In Huawei eNSP, what does each number in `interface Ethernet0/0/1` represent?

Answer:

The format `Ethernet0/0/1` follows this structure:

```
Ethernet [Slot] / [Subslot] / [Port]
            0   /     0     /   1
```

| Position | Name | Meaning |
| ---------- | ------ | --------- |
| First `0` | **Slot number** | The physical slot (chassis slot) where the interface card is installed. `0` typically means the main/default chassis slot. |
| Second `0` | **Subslot number** | The sub-slot or card position within that slot. `0` means the first (or only) sub-card. |
| `1` | **Port number** | The actual physical port number on that card. Port numbering usually starts from `0`, so `1` means the **second port**. |

**In short:**

- `Ethernet 0/0/0` → Slot 0, Subslot 0, Port 0 (1st port)
- `Ethernet 0/0/1` → Slot 0, Subslot 0, Port 1 (2nd port)
- `Ethernet 1/0/0` → Slot 1, Subslot 0, Port 0 (on a different line card)

> **Note:** In eNSP simulated devices (like AR2220), most interfaces stay at slot `0` and subslot `0` since it's a virtual environment. The only number you typically change is the **port number**.

---

References:

- [Huawei AR Series Interface Naming Convention](https://support.huawei.com/enterprise/en/doc/EDOC1100055039)
- [eNSP User Guide – Huawei](https://support.huawei.com/enterprise/en/doc/EDOC1100063899)
