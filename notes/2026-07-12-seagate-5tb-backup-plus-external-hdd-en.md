---
audio: false
generated: true
image: false
lang: en
layout: post
title: Seagate 5TB Backup Plus External HDD
translated: false
type: note
---

Question: Intro to Seagate 5TB Backup Plus External Portable Drive USB 3.0, Black

Answer:

Seagate Backup Plus 5TB Portable is a **2.5-inch external HDD** designed mainly for **backup, archive, and moving large files**. It is not an SSD; it uses a traditional spinning magnetic disk. ([Seagate.com][1])

### [Seagate Backup Plus Portable 5TB External Hard Drive USB 3.0 Black](https://www.walmart.com/ip/Seagate-5TB-Backup-Plus-External-Portable-Drive-USB-3-0-BLACK/677085372?utm_medium=feed&utm_source=chatgpt.com)

*$189.00*

## Key specifications

* Capacity: **5TB**
* Interface: **USB 3.0** (backward compatible with USB 2.0)
* Form factor: **2.5-inch portable HDD**
* Power: USB-powered (no external power brick)
* Weight: about **247–265g**
* Size: about **115 × 80 × 21 mm**
* Warranty: typically **2 years limited warranty** depending on region/model ([Seagate.com][1])

## What is inside?

Basically:

```
Computer
   |
 USB 3.0 cable
   |
[ USB-SATA bridge ]
   |
[ 2.5" Seagate HDD ]
   |
[ Magnetic platters + read/write heads ]
```

It is similar to the internal hard disk inside a laptop, but placed inside a USB enclosure.

Typical real-world performance:

```
Sequential read/write:
~100-150 MB/s (sometimes higher)

Random access:
~1-10 MB/s
```

Compared with SSD:

```
                 HDD          SSD
Capacity/$       ★★★★★        ★★★
Speed            ★★           ★★★★★
Shock resistance ★★           ★★★★★
Long archive     ★★★★         ★★★
Noise            Yes          No
```

## Good use cases

### 1. Backup

Good for:

* photos
* videos
* documents
* source code archives
* machine learning datasets
* model checkpoints

Example:

```
Laptop SSD 1TB
       |
       v
Seagate 5TB backup

~/projects
~/datasets
~/models
~/photos
```

For your AI work, it can store:

* HuggingFace datasets
* model weights
* training logs
* Docker images
* checkpoints

Example:

```
datasets/
 ├── FineWeb/
 │    └── 100B tokens
 ├── SEC-EDGAR/
 └── custom_corpus/

models/
 ├── gpt2-124m/
 ├── llama/
 └── checkpoints/
```

## Limitations

### 1. Not suitable for training directly

For PyTorch training:

Bad:

```
GPU
 |
PCIe
 |
RAM
 |
USB HDD  ← bottleneck
```

Better:

```
GPU
 |
PCIe
 |
NVMe SSD
```

Training datasets should stay on NVMe SSD if possible.

Use the HDD for:

```
cold storage
↓
backup
↓
archive
```

### 2. Mechanical failure risk

The disk has moving parts:

* spindle motor
* actuator arm
* magnetic platters

Dropping it while running can kill it.

Rule:

```
Important data:
1 copy = data
2 copies = safer
3 copies = professional
```

Example:

```
Local NVMe
      +
Seagate 5TB HDD
      +
Cloud backup
```

## Seagate Backup Plus vs other Seagate models

Seagate has several portable HDD lines:

```
Backup Plus
    |
    +-- nicer enclosure
    +-- backup software
    +-- consumer premium model

Expansion Portable
    |
    +-- cheaper
    +-- basic storage

One Touch
    |
    +-- newer premium model
    +-- encryption/features
```

Many users report that different Seagate portable lines often contain similar internal HDDs; the difference is mostly enclosure/software/features. ([Reddit][2])

## For your use case

Given you do:

* LLM training experiments
* datasets
* GPU machines
* lots of code/checkpoints

A good storage architecture:

```
PC
 |
 +-- 1TB/2TB NVMe SSD
 |       |
 |       +-- active training
 |
 +-- Seagate 5TB HDD
         |
         +-- datasets archive
         +-- checkpoints
         +-- backups
```

This drive is a **cheap capacity layer**, not a performance layer.

For AI development, a rough priority:

```
1. NVMe SSD  ⭐⭐⭐⭐⭐
2. RAM       ⭐⭐⭐⭐⭐
3. GPU VRAM  ⭐⭐⭐⭐⭐
4. External HDD ⭐⭐⭐
```

References:

* Seagate Backup Plus Portable Drive specifications ([Seagate.com][1])
* Seagate Backup Plus 5TB product listing

[1]: https://www.seagate.com/support/external-hard-drives/portable-hard-drives/backup-plus/?q=STDR1000200&utm_source=chatgpt.com "Backup Plus Portable Drive Support Page | Seagate US"
[2]: https://www.reddit.com/r/DataHoarder/comments/opmod3/is_the_seagate_one_touch_5tb_a_good_or_at_least_a/?utm_source=chatgpt.com "Is the Seagate One Touch 5TB a good (or at least a decent) hard drive?"
