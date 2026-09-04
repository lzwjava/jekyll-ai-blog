---
audio: false
generated: true
image: false
lang: en
layout: post
title: B760M-K D5 Xianyu Listing Worth
translated: false
type: note
---

Question: What is the **Colorful BATTLE-AX B760M-K D5 V20** motherboard, and is this Xianyu listing worth considering?

Answer:

![Image](https://images.openai.com/static-rsc-4/5BwDEy-Kd1poixuqEkr09RyO88UNMBQOaS41MnqN9SdF1JHdV47p6HjwKkXPDHwcXD3eY_Kcy-J_30bw0rW1APL1MS-plOW8xrMi52iNiaEchM3VJ5jKAwUTliJp7BI-3TpDMM6FFwAjK7SWFVg_GKPpZ4qqAjivQGKvxFcQD80QkcHs9N4UT33WitbVdhT3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3E2XHQqgAwR45A_z_b9ECY6zAjw5eVCfU6xq_TeYVwDrohT0GUHeXuKGibRjRofsLrT1UntkVJvEBK2XeaUZXVac0QCjziEd9YCriWVkkZIyTePn2e7Yfn0ac2yjY_OOkOH2tN6V3rNAoaQYpeCFkMTmAny8daLkGyITKPtArSRd5L0UD66tHFml0No1iSJ1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/W6AJLWwl2opG6940Wh240HPdUsAer-9_G2dKOiYuPqQ8ounPoxJWIZbFsIUgMw-2Gcl1Gwj94jjPwp7Z5zjrGXAl1JkREmJPd5H-fdrayjNTk7OvHKjYM4ZENzDRwzIZvcmPHmOyX0MEvfocRakXaXWdAnWDsreGCFROkDCz_2mG5ljy4l8dB8Mn9Wiiesmv?purpose=fullsize)

The **Colorful BATTLE-AX B760M-K D5 V20** is a **budget Micro-ATX Intel B760 motherboard** using the **LGA1700 socket**.

### 1. Basic architecture

| Part                | BATTLE-AX B760M-K D5 V20          |
| ------------------- | --------------------------------- |
| Manufacturer        | Colorful / 七彩虹                    |
| Series              | BATTLE-AX                         |
| Form factor         | Micro-ATX                         |
| Socket              | **LGA1700**                       |
| CPU                 | Intel 12th / 13th / 14th Gen      |
| Chipset             | **B760**                          |
| RAM                 | **DDR5**                          |
| RAM slots           | 2                                 |
| M.2                 | **2 × M.2**                       |
| PCIe GPU            | 1 × PCIe x16                      |
| Networking          | Gigabit-class Ethernet            |
| Wi-Fi               | No onboard Wi-Fi                  |
| Typical positioning | Cheap gaming / office / DIY board |

The important distinction is **B760M-K D5**: this is a DDR5 board. You cannot use DDR4 DIMMs.

### 2. B760 is the important part

Think of the platform like:

```text
Intel CPU
   │
   │ LGA1700
   ▼
┌─────────────────────┐
│ B760 chipset        │
│                     │
│ PCIe / USB / SATA   │
│ M.2 / networking    │
└─────────────────────┘
```

B760 is Intel's mainstream 700-series chipset.

Compared with H610:

```text
H610  → entry level
B660  → previous generation mainstream
B760  → newer mainstream
Z690  → enthusiast
Z790  → enthusiast
```

For a normal **12400F / 12600K / 13400F / 13500 / 13600K / 14400F** type machine, B760 is a sensible platform.

The board itself does **not** give you CPU overclocking like a Z-series board.

---

### 3. Two DDR5 slots

This is a relatively cheap design:

```text
CPU
 │
 └── memory controller
       │
       ├── DDR5 DIMM 1
       └── DDR5 DIMM 2
```

So maximum memory depends on the board's supported DIMMs/capacity, but the practical configuration is usually:

```text
16 GB  = 8 + 8
32 GB  = 16 + 16
64 GB  = 32 + 32
```

For your kind of work, I'd use **2 × 16 GB or 2 × 32 GB**, rather than leaving one slot populated.

---

### 4. Two M.2 slots

This is actually quite useful for a cheap board.

You can do:

```text
M.2 #1 → system / Linux / Windows
M.2 #2 → datasets / models / scratch
```

For example:

```text
1 TB NVMe
   +
2 TB NVMe
```

That's much nicer for ML experimentation than a board with only one M.2 slot.

---

### 5. The broken DIMM-slot clip is the thing I'd investigate

The seller says:

> "one memory slot's clip is broken, tested and works normally"

This **can be perfectly usable**, depending on which part of the retention mechanism is broken.

Modern DIMM slots often have only one movable locking latch:

```text
        RAM
   ┌─────────────┐
   │             │
   └─────────────┘
     ▲         ▲
     │         │
 fixed       latch
 contact     / clip
```

If only the plastic locking clip is broken but:

* the DIMM can still be inserted correctly
* the contacts are undamaged
* the motherboard recognizes the RAM
* dual-channel works
* the RAM stays mechanically secure

then electrically the motherboard can be completely fine.

**But I would not blindly trust "亲测".**

If you're buying this for GPU experimentation, I'd specifically test:

```bash
sudo dmidecode -t memory
sudo lspci -nn
sudo lspci -vv
```

and run a memory test.

---

### 6. "无封码" is not necessarily a positive signal

In Chinese second-hand motherboard listings, **封码** can refer to various seller/platform/repair inspection markings or seals depending on the seller.

I'd care much more about:

```text
POST
 ↓
BIOS
 ↓
both DIMM slots
 ↓
M.2 #1
 ↓
M.2 #2
 ↓
PCIe x16
 ↓
USB
 ↓
LAN
```

For your GPU-repair/testing use case, **PCIe x16 stability matters much more than cosmetic condition**.

---

### 7. For your GPU testing bench

This board is actually potentially quite interesting **as a cheap GPU test platform**.

You don't need an expensive Z790 board just to do:

```text
PSU
 │
 ▼
B760M
 ├── CPU
 ├── DDR5
 ├── NVMe
 └── PCIe x16
       │
       ▼
     GPU under test
```

For testing something like:

```text
GT 630
Quadro 4000
GT 730
RTX 4070
RTX 4090
...
```

the B760 platform is sufficient from a basic PCIe perspective.

The limitation is that this is a **small budget board**, so I wouldn't choose it as the foundation for a serious multi-GPU workstation.

### My verdict

For a **cheap experimental/GPU-repair bench**:

**BATTLE-AX B760M-K D5 V20: 👍 reasonable**

Especially if the price is low.

I'd rank the important checks:

```text
PCIe x16 works       ★★★★★
Both DIMMs work      ★★★★★
M.2 works            ★★★★☆
VRM condition        ★★★★☆
BIOS condition       ★★★★☆
Broken RAM clip      ★★★☆☆
Cosmetics             ★☆☆☆☆
```

If you send me the **actual Xianyu photos**, I can inspect the PCB, VRM, PCIe slot, DIMM clip, M.2 area and rear I/O and tell you what I'd check before buying.

I can also compare this directly against your **MSI B760M Mortar WiFi** and explain exactly what you're giving up by buying this cheaper Colorful board.
