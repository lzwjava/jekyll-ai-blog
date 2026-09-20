---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCI MMIO Above 4GB for GPU
translated: false
type: note
---

Question: **What does this PCI/MMIO diagnosis actually mean, and why would `pci=nocrs` / `pci=realloc=on` help a Tesla M40?**

Answer:

The key concept is that **GPU VRAM is not mapped into CPU physical memory directly**. The GPU exposes its VRAM through a PCIe **BAR (Base Address Register)**, and Linux needs to assign that BAR a range in the CPU's physical address space.

For a Tesla M40 with 12/24 GB VRAM, one BAR is huge and normally needs a **64-bit PCI MMIO address**, typically somewhere above the 4 GB boundary.

### 1. Think of the PCI BAR as a window into VRAM

Suppose the M40 has 12 GB VRAM:

```text
GPU VRAM
┌──────────────────────────────┐
│                              │
│          12 GB VRAM          │
│                              │
└──────────────────────────────┘
             ▲
             │ PCIe BAR
             │
CPU physical address space
┌──────────────────────────────────────────────────┐
│ 0x00000000                                       │
│                                                  │
│ RAM                                              │
│                                                  │
│ 0xFFFFFFFF  = 4 GB - 1                           │
├──────────────────────────────────────────────────┤
│                                                  │
│ PCIe MMIO                                       │
│                                                  │
│       GPU BAR → M40 VRAM                        │
│                                                  │
└──────────────────────────────────────────────────┘
```

The important distinction is:

```text
VRAM size != CPU physical address space consumed by VRAM
```

The GPU doesn't need 12 GB of normal system RAM.

It needs a **12 GB addressable MMIO aperture** through which the CPU can access the GPU's resources.

---

## 2. Why `0xfeafffff` is suspicious

You have:

```text
PCI host bridge window:

[mem 0xdf200000-0xfeafffff]
```

Convert that to size:

```text
0xfeafffff - 0xdf200000 + 1
≈ 510 MB
```

So this particular PCI root bridge has roughly a **510 MB MMIO window**, and importantly:

```text
0xfeafffff < 0x100000000
```

where:

```text
0x100000000 = 4 GB
```

Therefore the OS is being told:

```text
PCI devices may use MMIO here:

0xdf200000 ─────────────── 0xfeafffff
             ~510 MB

PCI MMIO above 4 GB:

             ❌ apparently unavailable
```

That is the central problem.

---

# 3. Why 4 GB matters

PCI historically used 32-bit addresses:

```text
0x00000000
       ...
0xffffffff
```

Maximum:

```text
2^32 = 4 GB
```

A PCI device can therefore have a BAR like:

```text
BAR0 = 0xd0000000
size  = 256 MB
```

Everything fits below 4 GB.

Modern GPUs are different.

A GPU can expose something conceptually like:

```text
BAR:
    size = 16 GB
    64-bit capable
```

You cannot fit that into the 32-bit physical address space.

So the platform needs to give PCIe a 64-bit MMIO region:

```text
0x100000000              4 GB
      │
      ▼
┌─────────────────────────────────────┐
│ PCI MMIO above 4 GB                  │
│                                     │
│ M40 framebuffer BAR                 │
│                                     │
│ potentially many GB                 │
└─────────────────────────────────────┘
```

This is why people talk about:

> **Above 4G Decoding**

It is essentially the platform/PCIe configuration that allows large PCIe BARs/MMIO resources to be placed above the 4 GB physical-address boundary.

---

# 4. The confusing part: your machine DOES have addresses above 4 GB

This line is extremely important:

```text
0000000100000000-000000011fdfffff System RAM
```

Let's translate:

```text
0x100000000
```

is exactly:

```text
4 GB
```

and:

```text
0x11fdfffff
```

is around:

```text
4.5 GB
```

So your machine has some system RAM physically located above 4 GB.

Roughly:

```text
Physical address space

0x000000000
     │
     │ RAM / devices
     │
0x0FFFFFFFF
     │
     │ 4 GB
     ▼
0x100000000
     │
     │ ~500 MB System RAM
     │
0x11FDFFFFF
```

This is completely normal on machines with memory remapping.

The statement:

> "the machine has only 4 GB RAM"

does **not** mean:

> "the CPU can only address physical addresses below 4 GB."

Those are different things.

---

# 5. Then why can't Linux put the GPU above 4 GB?

Because there are actually multiple layers involved.

Think:

```text
CPU physical address space
        │
        ▼
Firmware / ACPI
        │
        ▼
PCI Host Bridge
        │
        ▼
PCIe bus
        │
        ▼
GPU BAR
```

The firmware describes what resources the PCI host bridge is allowed to use.

ACPI provides this through things such as:

```text
_CRS
```

Current Resource Settings.

The kernel sees something roughly equivalent to:

```text
PCI root bridge
    MMIO:
        0xdf200000 - 0xfeafffff
```

and therefore thinks:

> "This PCI hierarchy has this MMIO space available."

The kernel isn't necessarily free to simply say:

```text
I'll put this PCI BAR at 0x200000000.
```

because the platform hasn't told it that this PCI root complex owns that address range.

---

# 6. This is why `pci=nocrs` is being considered

Normally Linux gets PCI resource information from ACPI.

Conceptually:

```text
BIOS/UEFI
   │
   ├── ACPI _CRS
   │
   ▼
Linux PCI subsystem
   │
   └── "Root bridge owns 0xdf200000-0xfeafffff"
```

`pci=nocrs` tells Linux:

> Don't trust/use the ACPI `_CRS` PCI resource information.

Then Linux can use other information, including the firmware memory map, to construct PCI resource assignments.

So the experiment is:

```text
Normal:

ACPI _CRS
    ↓
PCI root window
    ↓
0xdf200000-0xfeafffff
    ↓
M40 BAR cannot fit


pci=nocrs:

ignore _CRS
    ↓
derive PCI resources differently
    ↓
possibly discover usable 64-bit MMIO
    ↓
M40 BAR might fit
```

**But `pci=nocrs` does not magically create hardware capability.**

That's an important caveat.

If the chipset/firmware genuinely cannot route PCIe MMIO above 4 GB, `pci=nocrs` won't fix it.

---

# 7. What `pci=realloc=on` does

This is a different mechanism.

Suppose firmware assigned PCI resources badly:

```text
Root bridge:

MMIO:
0xdf200000-0xfeafffff

GPU:

BAR:
needs 12 GB
```

Obviously:

```text
12 GB > 510 MB
```

Linux can potentially reallocate PCI resources:

```text
Firmware allocation
        │
        ▼
Linux notices conflict
        │
        ▼
Reallocate PCI BARs/windows
        │
        ▼
larger MMIO window
```

That's what the `pci=realloc` family of options is trying to enable.

But again:

```text
Linux can rearrange resources
```

is different from:

```text
hardware supports arbitrary 64-bit PCI MMIO
```

The former cannot compensate for the latter.

---

# 8. `assign-busses` is another layer

PCI has a hierarchy.

For example:

```text
Root Complex
│
├── Bus 00
│   │
│   └── PCIe Root Port
│       │
│       └── Bus 01
│           │
│           └── Tesla M40
```

Firmware normally assigns bus numbers and resources.

If that assignment is broken, Linux can potentially reassign bus numbers:

```text
pci=assign-busses
```

But this is **not the first thing I'd suspect from the information shown**.

Your obvious failure is MMIO resource space, not necessarily bus numbering.

---

# 9. The real question is whether the platform supports 64-bit PCI MMIO

The hierarchy is therefore:

```text
                 ┌─────────────────────┐
                 │ BIOS/UEFI           │
                 │                     │
                 │ Above 4G Decoding? │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ PCI Root Complex    │
                 │                     │
                 │ 64-bit MMIO?        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Linux PCI subsystem │
                 │                     │
                 │ resource allocator  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Tesla M40           │
                 │                     │
                 │ Huge 64-bit BAR     │
                 └─────────────────────┘
```

If BIOS says:

```text
PCI MMIO above 4G: no
```

then:

```text
pci=nocrs
```

probably won't save you.

If BIOS supports it but ACPI describes the root bridge incorrectly, then:

```text
pci=nocrs
```

or:

```text
pci=realloc=on
```

can potentially fix the Linux-side allocation.

---

# 10. There's an even more important distinction with the M40

For NVIDIA GPUs, you should inspect the actual BARs.

Run:

```bash
lspci -vv -s 01:00.0
```

Look for:

```text
Region 0:
Region 1:
Region 2:
...
Memory at ...
```

and especially something like:

```text
Memory at <64-bit address> [size=...]
```

Also:

```bash
lspci -xxxx -s 01:00.0
```

and:

```bash
dmesg | grep -Ei \
  '01:00|BAR|resource|MMIO|pci.*assign|no space|failed'
```

The smoking gun would be something along the lines of:

```text
BAR X: no space for ...
BAR X: failed to assign ...
```

or:

```text
can't assign mem resource
```

Then we know we're actually dealing with PCI BAR allocation rather than some later NVIDIA driver problem.

---

# 11. One subtle correction to the quoted reasoning

This sentence:

> "The M40 needs a BAR above 4GB for its framebuffer (12GB or 24GB)."

is directionally correct, but slightly too simplistic.

The GPU does **not necessarily need one BAR equal to exactly the entire physical VRAM capacity** in every configuration.

Modern NVIDIA GPUs expose multiple BARs, and the exact BAR layout/size depends on the device and configuration.

The important invariant is:

```text
M40 has a large PCIe MMIO resource requirement
```

and your available PCI root MMIO window appears to be only:

```text
~510 MB below 4 GB
```

That's clearly suspicious for a large-memory GPU.

---

# 12. What I would check next

Don't start randomly adding kernel parameters yet.

First establish the hardware topology:

```bash
sudo lspci -nn
```

Then:

```bash
sudo lspci -vv -s 01:00.0
```

Then:

```bash
sudo lspci -tv
```

Then:

```bash
sudo dmesg | grep -Ei \
  'pci|BAR|resource|MMIO|above 4G|no space|failed to assign'
```

And specifically:

```bash
cat /proc/iomem
```

The last one is particularly useful because you'll see the actual physical address map:

```text
00000000-...
System RAM

...

df200000-feafffff
PCI Bus 0000:00

100000000-11fdfffff
System RAM
```

If there is **no PCI MMIO region above `0x100000000`**, despite RAM existing there, that's strong evidence that the PCI hierarchy wasn't given a 64-bit MMIO aperture.

---

## The mental model

The whole issue can be reduced to this:

```text
                  CPU physical address space

0 GB                                              4 GB
 │                                                  │
 ▼                                                  ▼
┌────────────────────────────────────────────────────┐
│                    System RAM                      │
├───────────────────────────────┬────────────────────┤
│ PCI MMIO                      │                    │
│ df200000-feafffff             │                    │
│ ~510 MB                       │                    │
└───────────────────────────────┴────────────────────┘
                                │
                                │
                                ▼
                         0x100000000
                              4 GB
                                │
                                ▼
                     ┌────────────────────┐
                     │ ~500 MB System RAM │
                     └────────────────────┘

                     ❌ no PCI MMIO here
```

But the M40 wants something conceptually like:

```text
0x100000000
      │
      ▼
┌──────────────────────────────────────────┐
│                                          │
│       Large M40 PCI MMIO BAR             │
│                                          │
│       potentially many GB                │
│                                          │
└──────────────────────────────────────────┘
```

So the real question isn't:

> **"Does the machine have more than 4 GB RAM?"**

It's:

> **"Does the PCI root complex have a sufficiently large 64-bit MMIO aperture above 4 GB, and does Linux know about it?"**

That's the thing I'd verify before touching `pci=nocrs`.

### References

* Linux kernel PCI documentation: [PCI support and kernel parameters](https://docs.kernel.org/PCI/?utm_source=chatgpt.com)
* Linux kernel boot parameters: [PCI kernel parameters](https://docs.kernel.org/admin-guide/kernel-parameters.html?utm_source=chatgpt.com)
* `lspci` documentation: [pciutils lspci documentation](https://man7.org/linux/man-pages/man8/lspci.8.html?utm_source=chatgpt.com)
