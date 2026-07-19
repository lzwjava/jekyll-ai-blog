---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual GPU Installation Guide for AI
translated: false
type: note
---

**Question: How to install two RTX 4070 or RTX 3090 GPUs together with an MSI motherboard? Is mATX too small? Which MSI boards are suitable?**

Answer:

Yes, **most mATX boards are a bad choice for dual large GPUs**, especially RTX 3090. The issue is not only PCIe slots — it is **physical spacing, airflow, power, and PCIe lane layout**.

For AI workloads (PyTorch, vLLM, training), you want:

* Two full-length PCIe x16 physical slots
* At least **3-slot GPU spacing**
* Good VRM/power delivery
* ATX/E-ATX case
* Enough PSU capacity

---

## 1. Why mATX is problematic

Typical MSI mATX board:

```
CPU
 |
PCIe x16  ---- RTX 3090 (3 slots)
 |
PCIe x1
 |
PCIe x16 ---- second GPU
```

A RTX 3090 is usually:

```
Slot 1: GPU
Slot 2: cooler
Slot 3: cooler thickness
```

After installing the first card:

```
[ RTX 3090 ]
[ RTX 3090 cooler ]
[ blocked PCIe slots ]
```

The second GPU gets:

* almost no airflow
* temperature +15~30°C
* possible thermal throttling

For RTX 4070 it is easier because most are 2-slot cards, but still tight.

---

## 2. MSI boards I would consider

### Option A: MSI MAG B760 Tomahawk WiFi (ATX)

MSI MAG B760 Tomahawk WiFi

Good balance:

* ATX size
* 2 × PCIe x16 physical slots
* DDR5
* supports 13th/14th gen Intel CPUs
* good VRM

Layout:

```
CPU

PCIe x16
   |
   |  RTX 3090

3 slots gap

PCIe x16
   |
   |  RTX 3090
```

This is probably the minimum I would buy.

---

### Option B: MSI PRO Z790-A MAX WiFi

Better for AI builds:

* more PCIe flexibility
* stronger VRM
* better memory support

Good with:

* i7-13700K
* i7-14700K
* i9-13900K

---

### Option C: MSI MAG Z790 Tomahawk MAX WiFi

Higher-end choice.

Advantages:

* stronger power design
* more expansion
* better if running two GPUs continuously

---

## 3. The real limitation: PCIe lanes

Important:

Most consumer Intel CPUs:

```
CPU PCIe lanes:

16 lanes GPU
4 lanes NVMe
```

Two GPUs become:

```
GPU1: x8
GPU2: x8
```

Example:

```
RTX 3090 #1
PCIe 4.0 x8

RTX 3090 #2
PCIe 4.0 x8
```

For LLM inference/training:

Usually OK.

You lose some bandwidth, but VRAM matters much more.

---

## 4. Power supply

Two RTX 3090:

GPU:

```
3090 ≈ 350W each
```

Two:

```
700W
```

CPU:

```
150-250W
```

System:

```
100W
```

Real requirement:

```
1000W minimum
1200W recommended
```

Good choices:

* Corsair HX1200
* Seasonic PRIME 1300W
* MSI MPG A1000G/A1250G

---

## 5. Case matters more than motherboard

For dual 3090:

Avoid normal gaming cases.

You want:

* 8-slot GPU support
* 420mm GPU clearance
* front mesh airflow

Examples:

Fractal Design Define 7 XL

Lian Li O11D XL

Server chassis is even better.

---

## 6. For your AI use case

Given you are thinking about:

* local LLM
* Qwen/DeepSeek style models
* fine-tuning
* vLLM

I would rank:

### Best value

```
2 × RTX 3090 24GB
+
MSI B760 Tomahawk
+
128GB DDR5 RAM
+
1200W PSU
```

Total VRAM:

```
48GB
```

This is a very capable local AI box.

---

### Cheaper path

```
2 × RTX 4070 12GB
```

VRAM:

```
24GB total
```

But for LLM:

```
48GB 3090 > 24GB 4070
```

because memory capacity dominates.

---

For your existing **i9-13900KF + MSI B760M Mortar + RTX 4070**, the first upgrade is actually motherboard + case + PSU. The B760M Mortar is a good gaming board, but it is not designed as a dual-GPU AI workstation.
