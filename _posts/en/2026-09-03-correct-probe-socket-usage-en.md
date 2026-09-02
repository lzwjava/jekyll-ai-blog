---
audio: false
generated: true
image: false
lang: en
layout: post
title: Correct Probe Socket Usage
translated: false
type: note
---

Question: Which two of the 4 bottom sockets on the 8901S should I use for the black and red probes?

Answer:

For **DC voltage / AC voltage measurements**, normally use:

```text
⚫ Black probe → COM
🔴 Red probe   → VΩmA / VΩHz socket
```

**Do NOT use the `20A` socket for voltage measurement.**

The `20A` socket is specifically for measuring **large current**, and using it incorrectly across a power rail can short the circuit.

So for your motherboard experiment:

```text
8901S

┌───────────────┐
│  20A          │ ← ❌ don't use for voltage
│  A/mA         │ ← ❌ don't use for normal voltage
│  VΩ...        │ ← 🔴 RED
│  COM          │ ← ⚫ BLACK
└───────────────┘
```

Set the dial to **DC V (`V⎓`)**, then:

```text
BLACK → GND
RED   → point you want to measure
```

If you upload a photo of the **bottom four sockets of your exact 8901S**, I can identify the two sockets visually before you connect it.
