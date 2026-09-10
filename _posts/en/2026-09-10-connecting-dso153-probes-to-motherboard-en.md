---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connecting DSO153 Probes to Motherboard
translated: false
type: note
---

Question: Where exactly do the **red and black DSO153 probe leads** go when measuring the powered motherboard?

Answer: For a simple voltage measurement:

```text
BLACK probe → GND
RED probe   → voltage you want to measure
```

### Easiest first test: ATX +5VSB

With the PSU connected to the motherboard:

```text
ATX 24-pin:

BLACK wire  ────── BLACK probe
                 │
                 └── GND

PURPLE wire ───── RED probe
                 │
                 └── +5VSB
```

You should read approximately:

```text
+5 V
```

**Do not swap them.**

Then you can measure:

| ATX wire | Red probe   | Black probe | Expected |
| -------- | ----------- | ----------- | -------: |
| Purple   | Purple wire | Black wire  |     ~5 V |
| Red      | Red wire    | Black wire  |     ~5 V |
| Orange   | Orange wire | Black wire  |   ~3.3 V |
| Yellow   | Yellow wire | Black wire  |    ~12 V |

For your **first measurement**, I strongly recommend **purple → red probe, black → black wire**. It's the easiest and safest way to confirm the DSO153 is working.

If you upload a photo of your actual ATX connector, I can identify the exact holes/wires for you.