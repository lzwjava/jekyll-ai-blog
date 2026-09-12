---
audio: false
generated: true
image: false
lang: en
layout: post
title: UEFI/BIOS Beyond OS Installation
translated: false
type: note
---

Question: **What interesting things can you do with UEFI/BIOS beyond simply installing Windows/Linux?**

Answer: If you're interested in low-level systems, **UEFI/BIOS is a surprisingly good playground**. The fun starts when you stop thinking of it as "the screen before Windows" and treat it as the firmware/software boundary between hardware and the OS.

Here are projects I'd actually consider interesting.

### 1. Build your own UEFI application

Probably the best starting project.

Write a tiny `.efi` executable that runs directly from the UEFI firmware:

```text
Power on
   ↓
UEFI firmware
   ↓
BOOTX64.EFI
   ↓
your_program.efi
   ↓
UEFI services
   ↓
hardware / filesystem / framebuffer
```

Things to build:

* framebuffer graphics demo
* CPU information viewer
* PCI device enumerator
* memory map viewer
* NVMe/SATA device scanner
* SMBIOS/DMI inspector
* UEFI variable browser
* boot-entry manager
* hardware benchmark

For example:

```text
UEFI Hardware Inspector

CPU
  AMD Ryzen ...
  cores: 16
  TSC: ...

Memory
  usable: 31.7 GiB
  regions: 42

PCI
  00:01.0 AMD USB
  01:00.0 NVIDIA GPU
  02:00.0 NVMe

Firmware
  UEFI version: ...
  Secure Boot: ON
```

This gets you directly into firmware programming without writing a whole OS.

---

### 2. Make a GPU benchmark that runs before Linux/Windows

This is **much more interesting** than a normal benchmark.

Build a UEFI `.efi` program that:

1. discovers the GPU through PCI
2. initializes a display path
3. draws a framebuffer
4. measures CPU/memory performance
5. optionally talks to the GPU through its hardware interface
6. displays results

Even better: make a **GPU stress-test USB**.

```text
USB
 └── EFI/
      └── BOOT/
           └── BOOTX64.EFI

Boot
 ↓
GPU detection
 ↓
VRAM / PCIe information
 ↓
GPU test
 ↓
temperature / clocks / errors
 ↓
PASS / FAIL
```

The hard part is that UEFI itself doesn't magically give you a CUDA/ROCm-style GPU API. You'd be getting much closer to **PCIe + GPU driver bring-up**.

That's a very good rabbit hole.

---

### 3. Write a UEFI bootloader

Instead of GRUB/systemd-boot:

```text
UEFI
 ↓
myboot.efi
 ↓
detect CPUs
 ↓
find kernel
 ↓
load kernel ELF
 ↓
build memory map
 ↓
setup page tables
 ↓
setup framebuffer
 ↓
ExitBootServices()
 ↓
jump to kernel
```

Then your kernel can be something tiny like:

```c
void kernel_main(struct boot_info *boot)
{
    print("hello from kernel\n");

    for (;;) {
        asm volatile("hlt");
    }
}
```

This teaches you a *lot* about the actual boot boundary.

---

### 4. Make a custom Linux installer

You can make your own Rufus-like system:

```text
myinstaller.iso
       ↓
UEFI boot
       ↓
tiny installer
       ↓
detect disks
       ↓
partition NVMe
       ↓
create filesystem
       ↓
extract Linux rootfs
       ↓
install kernel
       ↓
install your EFI loader
       ↓
create NVRAM boot entry
```

Then boot into your own Linux.

You could make the installer completely keyboard-driven:

```text
╔══════════════════════════════════╗
║        MY LINUX INSTALLER        ║
╠══════════════════════════════════╣
║                                  ║
║  NVMe0  2TB                      ║
║                                  ║
║  [1] Wipe disk                   ║
║  [2] Manual partition            ║
║  [3] Install                     ║
║                                  ║
╚══════════════════════════════════╝
```

---

### 5. Build a "PC diagnostic OS"

This is one of the most commercially useful ideas.

Boot a USB and **don't install anything**.

Instead:

```text
BOOT
 ↓
CPU test
 ↓
RAM test
 ↓
PCIe enumeration
 ↓
GPU test
 ↓
NVMe SMART
 ↓
USB test
 ↓
network test
 ↓
ACPI inspection
 ↓
UEFI variables
 ↓
report
```

Generate:

```text
PC DIAGNOSTIC REPORT

CPU       PASS
RAM       PASS  32 GB
GPU       PASS
PCIe      PASS  x16 Gen4
NVMe      PASS
USB       PASS
NETWORK   PASS

RESULT: HEALTHY
```

This is basically a tiny **hardware testing OS**.

---

### 6. Explore ACPI

This gets *very* deep.

UEFI exposes ACPI tables describing the machine:

```text
RSDP
 ↓
XSDT
 ├── FADT
 ├── DSDT
 ├── SSDT
 ├── MADT
 ├── MCFG
 └── ...
```

Write a tool that dumps and parses them.

Then you can explore:

* CPU topology
* APIC
* PCIe configuration space
* power management
* sleep states
* thermal zones
* embedded controller interfaces

Linux already has tools for much of this, but implementing your own parser is an excellent systems project.

---

### 7. Make your own BIOS/UEFI "demo scene"

This could be genuinely fun.

Boot directly into:

```text
UEFI Demo

████████████████████
█                  █
█   3D-ish demo    █
█                  █
█  CPU: 4.8 GHz    █
█  GPU: detected   █
█                  █
████████████████████
```

Then implement:

* plasma effects
* Mandelbrot
* ray marching
* software 3D
* particle simulation
* audio
* keyboard input

No Linux.

No Windows.

Just firmware → your `.efi`.

---

### 8. Experiment with UEFI variables / boot entries

UEFI maintains persistent NVRAM variables.

For example, conceptually:

```text
Boot0000 → Windows Boot Manager
Boot0001 → Linux
Boot0002 → MyOS
```

Build:

```bash
uefi-tool list
uefi-tool inspect Boot0002
uefi-tool create MyOS ./BOOTX64.EFI
uefi-tool delete Boot0002
```

This teaches you how firmware boot management actually works.

**Be careful here:** malformed or destructive NVRAM operations can make machines annoying to recover.

---

### 9. Make a multi-boot "Swiss Army knife"

This is probably the project I'd build if I wanted something immediately useful.

One USB:

```text
UEFI Toolkit
│
├── Hardware information
├── CPU benchmark
├── RAM test
├── GPU test
├── PCI inspector
├── NVMe tester
├── Network tester
├── Linux installer
├── Windows installer
├── Firmware tools
├── Secure Boot inspector
├── ACPI explorer
└── UEFI shell
```

Boot menu:

```text
┌─────────────────────────────┐
│       ZHIWEI BOOT TOOL      │
├─────────────────────────────┤
│ > Hardware Diagnostic       │
│   CPU Benchmark             │
│   GPU Benchmark             │
│   Memory Test               │
│   PCI Explorer              │
│   NVMe Explorer             │
│   Linux Installer           │
│   Windows Installer         │
│   UEFI Shell                │
│   Reboot                    │
└─────────────────────────────┘
```

That's essentially **your own tiny pre-OS environment**.

---

### 10. Go one level deeper: write a tiny kernel

The progression I'd recommend is:

```text
Rufus
  ↓
UEFI application
  ↓
UEFI hardware inspector
  ↓
UEFI bootloader
  ↓
ExitBootServices()
  ↓
x86_64 kernel
  ↓
paging
  ↓
interrupts
  ↓
APIC
  ↓
SMP
  ↓
PCI
  ↓
NVMe
  ↓
USB
  ↓
GPU
```

At that point you're no longer really "doing BIOS stuff."

You're building an **OS from the firmware boundary upward**.

And the especially interesting split is:

```text
                Firmware
                   │
             UEFI services
                   │
          ┌────────┴────────┐
          │                 │
      UEFI app          Bootloader
                            │
                     ExitBootServices
                            │
                          Kernel
                            │
             ┌──────────────┼──────────────┐
             │              │              │
            CPU            PCIe           RAM
                            │
                     ┌──────┴──────┐
                    NVMe           GPU
```

If your goal is **"I want something fun to hack on this weekend"**, I'd pick **#1 → #2 → #5**: write a UEFI hardware inspector, then turn it into a bootable CPU/RAM/GPU diagnostic environment. That's a much more interesting project than just making another Windows installer.
