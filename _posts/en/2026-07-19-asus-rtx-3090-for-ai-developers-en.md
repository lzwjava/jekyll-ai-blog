---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS RTX 3090 for AI Developers
translated: false
type: note
---

Question: Why is this ASUS RTX 3090? Is ASUS an NVIDIA partner?

Answer:

Yes. ASUS is one of NVIDIA's major **AIB (Add-In Board) partners**.

NVIDIA designs the GPU chip itself:

```
NVIDIA
  |
  |-- GPU silicon (GA102 for RTX 3090)
  |-- reference design
  |-- CUDA / drivers
  |
  +---- ASUS
  +---- MSI
  +---- Gigabyte
  +---- Zotac
  +---- PNY
  +---- Palit
        |
        +-- custom PCB
        +-- cooler
        +-- power design
        +-- factory overclock
```

ASUS does not manufacture the RTX 3090 GPU chip. NVIDIA sells the GA102 GPU dies to partners, and ASUS builds the final graphics card.

---

ASUS RTX 3090 product lines:

### ASUS TUF Gaming RTX 3090

Target: value + durability

* 3-fan cooler
* thick heatsink
* good VRM
* usually lower price
* slightly lower factory OC

### ASUS ROG Strix RTX 3090

Target: enthusiast

* larger cooler
* higher power limit
* better PCB
* more expensive

### ASUS ProArt / workstation lines

Target: creators

---

Why ASUS has a good reputation:

1. **Long GPU history**

ASUS has been making NVIDIA graphics cards since the 1990s.

2. **Strong cooling designs**

3090 is a very hot GPU:

```
GA102 chip:
350W+ power
24GB GDDR6X memory
```

The cooler matters a lot.

ASUS TUF uses:

* large fin stack
* multiple heat pipes
* three axial fans
* good VRM cooling

3. **Better resale value**

Used market usually values:

```
ASUS ROG Strix
    >
ASUS TUF
    >
MSI Gaming X Trio
    >
Gigabyte Gaming OC
    >
Zotac / Palit / Colorful lower models
```

(Depends on country.)

---

For AI use, brand matters less than:

```
VRAM size
+
cooling
+
power stability
+
memory temperature
```

CUDA performance is almost identical.

A:

```
ASUS TUF RTX 3090
```

and:

```
MSI RTX 3090
```

with the same GA102 chip will train your PyTorch model at almost the same speed.

The reason I like this listing is not "ASUS" alone. It is:

```
RTX 3090
+
24GB VRAM
+
good cooler
+
70°C stress temperature
```

That combination is exactly what an AI developer wants from a used GPU.
