---
audio: false
generated: true
image: false
lang: en
layout: post
title: x16 is 4x speed of x4
translated: false
type: note
---

Question: Does PCIe x16 mean 4× the speed of PCIe x4?

Answer: **Yes, if everything else is the same.** `x16` means 16 PCIe lanes; `x4` means 4 lanes.

Think of lanes as parallel wires:

```text
PCIe x1   = █
PCIe x4   = ████
PCIe x8   = ████████
PCIe x16  = ████████████████
```

So:

```text
x16 / x4 = 4
```

An x16 link has **4× the theoretical bandwidth** of an x4 link **at the same PCIe generation**.

For example, roughly:

| Link | PCIe 3.0 bandwidth per direction |
| ---- | -------------------------------: |
| x1   |                          ~1 GB/s |
| x4   |                          ~4 GB/s |
| x8   |                          ~8 GB/s |
| x16  |                         ~16 GB/s |

But there's an important distinction: **physical slot size ≠ electrical link width**.

Your B350 board can have:

```text
Slot 1: x16 physical → x16 electrical
Slot 2: x16 physical → x4 electrical
```

So both slots look like this:

```text
[================]  ← x16 physical
[================]  ← x16 physical
```

but electrically:

```text
Slot 1:  ████████████████  x16
Slot 2:  ████              x4
```

For GPUs, this usually means the second GPU gets much less PCIe bandwidth, although **GPU compute performance is not necessarily 4× slower**. Once the model/data is in VRAM, PCIe bandwidth often isn't the bottleneck.
