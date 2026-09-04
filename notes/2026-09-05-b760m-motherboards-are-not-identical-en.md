---
audio: false
generated: true
image: false
lang: en
layout: post
title: B760M Motherboards Are Not Identical
translated: false
type: note
---

Question: **Is Gigabyte B760M the same thing as MSI B760M? Who makes B760M?**

Answer:

No. **Gigabyte B760M and MSI B760M are not the same motherboard.** They are boards from different manufacturers that use the **same Intel B760 chipset**.

Think of it like this:

```text
Intel
  │
  └── B760 chipset
       │
       ├── MSI → MAG B760M MORTAR WIFI
       ├── Gigabyte → B760M DS3H / AORUS ELITE
       ├── ASUS → TUF GAMING B760M / PRIME B760M
       ├── ASRock → B760M Pro RS
       └── Biostar → B760M series
```

### What does "B760M" mean?

Break the name apart:

```text
B760
│
└── Intel chipset

M
│
└── Micro-ATX form factor
```

**B760 is made/designed by Intel as a chipset/platform.**

The motherboard manufacturer then designs the actual motherboard around that chipset.

So:

> **B760M is not a factory/brand.**

It is essentially:

**Intel B760 chipset + mATX motherboard design.**

### Example

These are all different boards:

| Board                 | Manufacturer | Chipset    | Size |
| --------------------- | ------------ | ---------- | ---- |
| MAG B760M MORTAR WIFI | MSI          | Intel B760 | mATX |
| B760M DS3H            | Gigabyte     | Intel B760 | mATX |
| TUF GAMING B760M-PLUS | ASUS         | Intel B760 | mATX |
| B760M Pro RS          | ASRock       | Intel B760 | mATX |

They can all support the same general CPU family, e.g.:

```text
LGA1700
    ↓
12th Gen Intel
13th Gen Intel
14th Gen Intel
```

But **VRM, PCIe layout, M.2 count, BIOS, LAN chip, Wi-Fi, audio, USB, cooling, and build quality can be very different.**

### For your GPU-testing purpose

This distinction is important.

If someone says:

> "I have a B760M."

That tells you **almost nothing about the actual motherboard**.

You want the complete model:

```text
MSI MAG B760M MORTAR WIFI
Gigabyte B760M DS3H
Gigabyte B760M AORUS ELITE
ASUS TUF GAMING B760M-PLUS
...
```

Then we can inspect its **PCIe topology**.

For example, two "B760M" boards could have:

```text
Board A:
GPU #1 → PCIe x16
GPU #2 → PCIe x4

Board B:
GPU #1 → PCIe x16
GPU #2 → PCIe x1
```

For your **two-GPU repair/test bench**, that difference matters much more than the word `B760M`.
