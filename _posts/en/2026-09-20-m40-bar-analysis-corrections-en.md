---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 BAR Analysis Corrections
translated: false
type: note
---

Question: **Is this M40 / BAR / Above-4G analysis correct?**

Answer: **Mostly, but there are two important corrections.**

1. **`BAR1 [size=16M]` does *not* mean the M40 only exposes 16 MB of its 24 GB VRAM.**
   That's a PCIe BAR mapping, not the physical VRAM capacity. The M40 does indeed have **24 GB GDDR5 VRAM**.

2. **The Resizable BAR claim is too categorical.**
   The Tesla M40/GM200 does not provide modern Resizable BAR support in the sense used by Ampere-era GPUs. So you should not expect a 24-GB resizable BAR on an M40. But saying *"Resizable BAR was introduced with RTX 30 / Ampere"* is historically oversimplified: the PCIe Resizable BAR capability predates Ampere; Ampere is when NVIDIA made it a prominent consumer feature.

3. **Above 4G Decoding is the important BIOS setting for a 24-GB M40.**
   This is about the host's PCIe MMIO address space, not directly about whether the GPU physically has 24 GB. With a large GPU BAR, the firmware needs to be able to allocate PCIe MMIO space above the 4-GB boundary. On a modern server/workstation, **Above 4G Decoding should generally be enabled**.

4. **The statement about the NVIDIA driver is a little misleading.**
   The driver cannot magically overcome a firmware resource-allocation failure. The sequence is roughly:

   ```text
   M40
     │
     ├── 24 GB physical VRAM
     │
     ├── PCIe BARs
     │     ├── BAR0: registers/control
     │     └── BAR1: VRAM aperture/mapping
     │
     ▼
   PCIe firmware resource allocation
     │
     ├── 32-bit MMIO space
     └── 64-bit MMIO space (>4 GB)
     │
     ▼
   Linux PCI subsystem
     │
     ▼
   NVIDIA driver
   ```

   The fact that you currently see:

   ```text
   Memory at f1000000 (32-bit, non-prefetchable) [size=16M]
   ```

   is **not sufficient to conclude that the 24 GB VRAM is incorrectly mapped**.

### The thing I'd check

Run:

```bash
sudo lspci -vv -s <M40_BDF>
```

and:

```bash
sudo lspci -vvv -s <M40_BDF> | grep -E \
  'Memory at|Prefetchable|Region|LnkCap|LnkSta|Resizable BAR|Physical Slot'
```

Also:

```bash
nvidia-smi
```

after the driver loads.

And the most useful check for the MMIO question:

```bash
sudo dmesg | grep -Ei 'pci|bar|mmio|resource|nvidia'
```

If the M40 is healthy, `nvidia-smi` should ultimately report something like:

```text
Memory-Usage
0MiB / 24576MiB
```

(or a small amount used by the driver).

### One subtle point

A **16-MB BAR1 shown by `lspci` does not necessarily mean BAR1 is permanently limited to 16 MB of VRAM access**. Maxwell Tesla cards use a relatively small BAR aperture and the driver can manage mappings into the larger VRAM space. So don't use:

```text
BAR1 = 16M
```

as evidence that your M40 cannot access its full 24 GB.

The more meaningful test is:

```bash
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv
```

If that reports approximately **24576 MiB total**, the full VRAM is available regardless of the `lspci` 16-MB BAR display.

**Bottom line:** the quoted analysis has the right operational recommendation—**enable Above 4G Decoding if the BIOS exposes it**—but the explanation that a 24-GB M40 *needs* a huge BAR to address all VRAM is incorrect/oversimplified. The 16-MB BAR1 output by itself is not a problem.

I can also walk through the actual `lspci -vv` output line-by-line and determine whether your M40's PCIe/MMIO configuration is healthy.
