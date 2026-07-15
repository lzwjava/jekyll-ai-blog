---
audio: false
generated: true
image: false
lang: en
layout: post
title: EATX Motherboard Guide
translated: false
type: note
---

## Question: what's EATX board?

**EATX (Extended ATX)** is a **larger-than-standard PC motherboard form factor**. It is an extension of the normal ATX size, designed for systems that need **more PCIe slots, more memory slots, more power delivery, or more expansion capability**.

![Image](https://images.openai.com/static-rsc-4/Qea2CXiQ9yClfkczPZbsw61MJI6HBF5wa9yElTyRnaiHlC_032VEObFcT3PGKLIMf3Sl67NX_hp7g7H1e5n-uwRlV0_nye58ZG_0XkQBk2h_5gcvHFJqZ6qkxcu2noJRhD-pDlfQ2LxWIfRsgSUBPgG_dLoUdiD8qUwJk1BYWNkXTTMdCbUDw4pMqmuBXdT3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/RauGj7lNjPyc-ts7GbL3zV9rgrbtvAPvBlQmw2Laic0DCRaUNEF94GHvv-sPWilqRhfkW60XHSbqYExTs-03aTabnImLk8kOZoL1Zn4HrIXj3jlSl3fWqy7T3v2JEJmewvRqx8gwtbizAtMSGdWxNUHuwJkNOfSIBwiGyB4Tkny9jxr2kB-alPgz0LdV1ZEK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/S8tKyk-5-JFLwTti8Qwm9jJFcqc3qQh3TW5BwSrsVBEcxBE_NU1wmYRNyrIbUXMeBs40Jyz-Vaj69wqmKPDyKgnRDeXHWaaWvfcvr7nz41D9mVo1Agcu__MbHefYA3NRoFUZQ8Hf_Iyd7Da229GW4cSk4uZT3dug-j7UaxXAHtYfOCP-MV86KEals0tbcobT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/QtnFaAmuvms4v5oFt4-T-MFvABuCCZy4uqkgr4J_PQqHpeKKRqbagvRmE-B-cDXIFLQSu7XLrUNYyQtyYhCz-_Ws1peqDP7Hdgl4JYPK75wIMUrhw-Su9amcDEc71fBExLS2jSXrMSVxDKI2DtC9fLJYqu8-6pTlBHFriL1T8g2WREeYaLGmOjLrQ9aILUOh?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LOgYafmdb_8xjicb2nQuAGN_gXeTE3wjUoA2w7nNEKuLJTLEZsE41LcajHZ1o_qgj79s05PzyYBI6cuNxAuu7l1s-_k8RCB6tevMWTXVgrlAlvk5az5yVg_Hud-UapmI1t7ayEt2IBptUvONemSATcslUj11UhviiuOJQI8j36MQuTNNLbZo7-MolR_GZxUW?purpose=fullsize)

### Size comparison

| Form factor |            Size (approx.) | Typical use                   |
| ----------- | ------------------------: | ----------------------------- |
| Mini-ITX    |              170 × 170 mm | Small PCs                     |
| Micro-ATX   |              244 × 244 mm | Budget / mainstream           |
| ATX         |              305 × 244 mm | Normal desktop                |
| **EATX**    | **305 × 330 mm** (varies) | Workstations / HEDT / servers |
| SSI-EEB     |              305 × 330 mm | Server-class                  |

The key difference is usually **width** (front-to-back depth). EATX is often wider than ATX.

---

## Why use EATX?

### 1. More PCIe slots

A normal ATX board:

```
[ CPU ]

PCIe x16
PCIe x1
PCIe x1
PCIe x16
```

EATX workstation board:

```
[ CPU ]

PCIe x16
PCIe x16
PCIe x16
PCIe x16
PCIe x16
```

Useful for:

* Multiple GPUs
* AI training rigs
* Video rendering
* Storage controllers
* Network cards

Example:

* 4 × RTX 4090
* 4 × RTX 3090
* Multiple MI50 / Radeon Instinct cards

---

### 2. More RAM

Desktop ATX:

```
DIMM DIMM DIMM DIMM
```

EATX workstation:

```
DIMM DIMM DIMM DIMM
DIMM DIMM DIMM DIMM
```

Especially for:

* Threadripper Pro
* Intel Xeon W
* AMD EPYC workstation boards

Examples:

* 8-channel DDR5 memory
* 1TB+ RAM capacity

---

### 3. Bigger CPU platforms

EATX is common with:

### AMD Threadripper Pro

Example:
ASUS Pro WS WRX80E-SAGE SE WIFI

Features:

* sWRX8 socket
* 8-channel DDR4 ECC
* 7 PCIe 4.0 x16 slots
* Supports Threadripper Pro 7000 series equivalents in newer boards

---

### AMD EPYC workstation

EPYC platforms often use:

* SP3/SP5 sockets
* EEB/EATX sizes
* Huge RAM capacity

Example:

```
EPYC CPU
   |
   +-- 8 channel memory
   |
   +-- 128 PCIe lanes
   |
   +-- many GPUs
```

---

## EATX vs normal gaming motherboard

Example:

### MSI X870E (ATX)

Good for:

* Ryzen 9000
* RTX 4070/4090
* Gaming
* Single GPU AI experiments

Usually:

```
CPU
 |
GPU
 |
GPU(optional)
```

---

### Threadripper Pro EATX

Designed for:

```
CPU
 |
GPU GPU GPU GPU
 |
NVMe NVMe NVMe
 |
1TB RAM
```

More like a mini server.

---

## For AI workloads

EATX becomes interesting when you move from:

```
RTX 4070 12GB
      |
      |
single GPU
```

to:

```
Threadripper Pro
+
4 × RTX 3090 24GB

= 96GB VRAM
```

or:

```
EPYC
+
8 × GPU

= serious training node
```

The motherboard is not faster by itself. The advantage is **I/O capacity**:

* more PCIe lanes
* more GPUs
* more memory channels
* more storage

---

For your current experiments (RTX 4070 + MI50 + possible multi-GPU), a normal **ATX X870/B550/X570** board is usually enough. EATX becomes valuable when building a **4–8 GPU local AI workstation**.
