---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Upgrading to MI50 for AI: Caveats"
translated: false
type: note
---

Question: Can this i5-10400F + B460M machine be upgraded from RX 6500 XT to AMD MI50 / Radeon Pro VII class GPU for AI?

Answer:

Short answer: **technically yes, but with important caveats.** The motherboard can physically run an AMD MI50, but this is not an ideal platform for it.

Your machine:

```
CPU: i5-10400F
Motherboard: ASUS B460M
PCIe: 3.0 x16 slot
RAM: 16GB DDR4
PSU: "百硕600W"
GPU: RX6500XT -> replace with MI50
```

## 1. PCIe compatibility

AMD MI50:

AMD Radeon Instinct MI50

uses:

* PCIe 4.0 x16
* 16GB HBM2 ECC
* ~300W TDP

B460M:

* PCIe 3.0 x16

PCIe is backward compatible:

```
MI50 PCIe 4.0
        |
        v
B460 PCIe 3.0 x16
```

It will work.

Bandwidth:

PCIe 4.0 x16:
≈32 GB/s

PCIe 3.0 x16:
≈16 GB/s

For training, most data stays in VRAM after loading, so it is usually acceptable.

---

## 2. Power is the real issue

RX6500XT:

```
~100W
```

MI50:

```
~300W
```

Difference:

```
+200W
```

Your PSU:

> 百硕600W

is the unknown.

A good 600W PSU:

✅ probably OK

A cheap no-name 600W:

⚠️ risky

Because MI50 is a workstation accelerator. It can pull sustained power for hours.

I would prefer:

* Seasonic
* Corsair
* Super Flower
* FSP
* Delta

600-750W quality PSU.

---

## 3. Cooling

You mentioned:

> 烤鸡十分钟温度90度

This is normal-ish for MI50.

MI50 is not a gaming card.

It uses a blower design:

```
air intake
    |
    v
[GPU]
    |
    v
hot air out
```

It expects a workstation/server chassis.

In a normal ATX case:

* 85-95°C is common
* fan noise can be high

90°C under FurMark is not automatically bad.

---

## 4. Display output problem

Important:

MI50 usually has:

* no display output

It is a compute card.

But you said:

> Radeon Pro VII, one mini-DP output

This changes things.

AMD Radeon Pro VII

is basically a workstation sibling of MI50:

* Vega 20
* 16GB HBM2
* ECC
* one mini DisplayPort
* compute support

It can drive a monitor.

So if it is actually **Radeon Pro VII**, it is easier.

---

## 5. AI software situation

This is the biggest caveat.

NVIDIA:

```
PyTorch
   |
CUDA
   |
RTX 4070
```

works smoothly.

AMD:

```
PyTorch
   |
ROCm
   |
MI50
```

is more complicated.

MI50 support:

* ROCm support existed historically
* newer ROCm versions dropped many Vega GPUs

You may need:

* older ROCm
* Linux
* specific PyTorch versions

Example:

```
Ubuntu 22.04
ROCm 5.7
PyTorch ROCm build
```

Possible, but not plug-and-play.

---

## 6. Compared with RX6500XT

Huge upgrade:

|                  | RX6500XT       | MI50          |
| ---------------- | -------------- | ------------- |
| VRAM             | 4GB GDDR6      | 16GB HBM2 ECC |
| Compute          | gaming         | HPC           |
| AI               | almost useless | useful        |
| Memory bandwidth | ~144GB/s       | ~1TB/s        |
| Power            | 100W           | 300W          |

For AI workloads:

MI50 is another category.

---

## My recommendation for this specific machine

If you already own the i5-10400F machine:

I would do:

```
i5-10400F
+
B460M
+
32GB RAM upgrade
+
quality 750W PSU
+
MI50 / Radeon Pro VII
+
Ubuntu
```

It becomes a cheap AI experiment box.

But I would not spend money upgrading:

```
256GB SSD
16GB RAM
cheap PSU
```

first.

Priority:

1. Replace PSU ✅
2. Add RAM to 32GB/64GB ✅
3. Add 1TB SSD ✅
4. Install MI50 ✅

Then it becomes a reasonable "ROCm playground" machine.

For your situation (already having RTX 4070), this box makes sense mainly as a **cheap AMD GPU research machine**, not as your main AI training machine.
