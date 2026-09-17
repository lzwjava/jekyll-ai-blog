---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kenao X99-D4 P100 PCI Error Possible
translated: false
type: note
---

Question: Will the **Kenao X99-D4 + NVIDIA Tesla P100** setup hit the **“PCI OUT OF RESOURCES CONDITION”** error?

Answer: **It can, but a single P100 should normally be fine.** The risk increases substantially with multiple GPUs / PCIe cards.

For a typical build:

```text
Kenao X99-D4
Xeon E5 v3/v4
DDR4
1× Tesla P100 PCIe 16GB
1× NVMe
```

I would **not expect PCI resource exhaustion** simply from adding one P100.

The important BIOS setting is:

```text
Above 4G Decoding = Enabled
```

Especially if you eventually want:

```text
2× P100
4× P100
+ NVMe
+ 10/25/40GbE NIC
```

### Why P100 can trigger it

The P100 has substantial PCIe BAR/MMIO requirements. On an older X99 firmware, the problem isn't necessarily that the CPU lacks PCIe lanes; it's that the **BIOS may fail to allocate enough PCI address space**.

Think of two separate limits:

```text
PCIe lanes                         PCI resource address space
───────────                        ───────────────────────────
Xeon provides many lanes           BIOS must map device BARs
        │                                    │
        ▼                                    ▼
Can devices electrically connect?  Can firmware assign addresses?
```

So even though an E5 Xeon may have **40 PCIe 3.0 lanes**, you can still get a resource-allocation error.

### For your proposed cheap P100 box

I'd configure the BIOS approximately:

```text
Above 4G Decoding     Enabled
CSM                   Disabled*
UEFI Boot             Enabled
Resizable BAR         Disabled
```

`CSM` depends on the exact Kenao BIOS/GPU combination, so I wouldn't blindly change it if your existing system boots correctly.

Then verify:

```bash
lspci -nn
nvidia-smi
```

You want the P100 to appear in both.

**The bigger concern with this Kenao board is not the P100 itself—it's the quality/firmware consistency of a cheap X99 board.** If you're considering buying the whole 200-board lot, I'd first buy/test **one board with your exact P100**, then scale up.

If you tell me **which P100 you have (PCIe 12GB/16GB, or SXM2)** and the **exact X99-D4 listing/photos**, I can check the slot layout and tell you whether 1/2/4 P100s are realistic.
