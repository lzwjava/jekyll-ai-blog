---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVLink vs GPU Power Connector
translated: false
type: note
---

Question: How does NVLink physically connect on RTX 3090? Is it related to the GPU power connector (12-pin on RTX 4070)?

Answer:

No. **NVLink has nothing to do with the GPU power connector.**

The confusion comes from both being "small connectors on the top of the GPU", but they are completely different.

## RTX 4070 power connector

RTX 4070 uses:

* **12VHPWR (12+4 pin) power connector** on many models

It looks like:

```
PSU cable
    |
    v
[ 12VHPWR ]
+----------------+
| Power input    |
+----------------+

RTX 4070 PCB
```

Purpose:

```
PSU ---> GPU
```

It provides electrical power.

---

## RTX 3090 power connectors

Most RTX 3090 cards use:

```
8-pin PCIe
8-pin PCIe
```

or sometimes:

```
8-pin
8-pin
8-pin
```

Example:

```
PSU
 |
 +----8 pin----+
              |
 +----8 pin----+ ---> RTX 3090
```

RTX 3090 power consumption:

* ~350W typical
* higher under power limit

So it needs more power connectors than RTX 4070.

---

## Where is NVLink on RTX 3090?

RTX 3090 has a **separate NVLink finger connector** on the top edge of the card.

Example:

```
                 Top of GPU

        NVLink connector
              ||
              ||
  +-------------------------+
  |                         |
  |       RTX 3090          |
  |                         |
  +-------------------------+

        |             |
     8-pin          8-pin
```

The NVLink bridge sits here:

```
RTX 3090 #1

  [ NVLink port ]
          ||
          ||
  [ NVLink bridge ]
          ||
          ||
  [ NVLink port ]

RTX 3090 #2
```

---

## Important: NVLink is not PCIe power

There are three separate connections:

### 1. Power

```
PSU
 |
8-pin connectors
 |
GPU
```

### 2. PCIe interface

```
GPU
 |
PCIe slot
 |
Motherboard
```

### 3. NVLink

```
GPU
 |
NVLink bridge
 |
GPU
```

They serve different purposes.

---

## RTX 3090 example AI workstation

Two RTX 3090:

```
             CPU
              |
        PCIe motherboard
        /              \
       /                \
 RTX3090 #1          RTX3090 #2
    |                   |
 8pin+8pin           8pin+8pin
    |
    +==== NVLink ====+
```

You need:

* motherboard with two x16 slots (physical)
* enough PCIe lanes
* large PSU (850W-1200W)
* enough airflow

---

## One more AI-specific note

For LLM training, NVLink bandwidth matters:

RTX 3090:

* PCIe 4.0 x16: ~32 GB/s bidirectional theoretical
* NVLink: ~112 GB/s bidirectional

So tensor parallel communication can improve.

But modern frameworks:

* PyTorch DistributedDataParallel
* DeepSpeed ZeRO
* FSDP

often work well over PCIe too.

For your situation (local LLM experiments), the main attraction of RTX 3090 is still:

```
24GB VRAM × 2 = 48GB total capacity
```

NVLink is a nice optimization, not the main reason to buy it.
