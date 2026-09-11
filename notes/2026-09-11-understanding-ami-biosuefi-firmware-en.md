---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding AMI BIOS/UEFI Firmware
translated: false
type: note
---

Question: What is **American Megatrends (AMI) BIOS**?

Answer:

**American Megatrends (AMI)** is a company that develops **BIOS/UEFI firmware** used by motherboard manufacturers. You can think of AMI as the company providing the firmware platform, while ASUS, Huanan, MSI, Gigabyte, etc. configure/customize it for their boards.

### 1. What BIOS actually does

When you press the power button:

```text
Power ON
   ↓
CPU starts executing firmware
   ↓
AMI BIOS / UEFI
   ↓
POST
(Power-On Self Test)
   ↓
Initialize CPU / RAM / chipset / PCIe / USB / storage
   ↓
Find boot device
   ↓
Windows / Linux bootloader
```

So BIOS is the **first software running on the CPU** after power-on.

### 2. AMI BIOS vs UEFI

Historically:

```text
BIOS
 └── legacy firmware interface

UEFI
 └── modern replacement for traditional BIOS
```

People still commonly call the whole thing "BIOS", even when the firmware is actually UEFI.

Modern AMI firmware is generally **AMI UEFI**, commonly based on **AMI Aptio**.

You'll often see something like:

```text
American Megatrends
AMIBIOS
Aptio
UEFI
```

during POST.

### 3. What you can configure

The BIOS/UEFI is essentially the motherboard's hardware configuration layer.

For example:

```text
CPU
 ├── CPU settings
 ├── power management
 └── virtualization

RAM
 ├── frequency
 ├── timings
 └── XMP (if supported)

PCIe
 ├── PCIe generation
 ├── primary display
 └── PCIe devices

Storage
 ├── SATA
 ├── NVMe
 └── boot configuration

Boot
 ├── UEFI / Legacy
 ├── CSM
 └── boot order

Security
 ├── Secure Boot
 └── TPM
```

For your **Huanan B75**, the AMI firmware is especially useful when you're testing different CPUs, RAM, PCIe GPUs, SATA drives, etc.

### 4. AMI beep/error codes

AMI firmware can also report POST failures through **beep codes** or motherboard diagnostic indicators.

Conceptually:

```text
Power ON
   ↓
POST
   ├── CPU OK
   ├── RAM OK
   ├── GPU/display initialization
   ├── chipset OK
   └── boot device
```

If something fails before the system can display BIOS, you may get:

```text
beep
LED diagnostic code
no display
automatic reboot
```

This is why BIOS/POST knowledge is quite useful for **GPU and motherboard repair**: you can distinguish a problem in the power/POST path from a problem occurring later in Windows/Linux.

**One important distinction:** AMI isn't the motherboard. Your Huanan B75 is the motherboard; **AMI supplies the firmware technology that the motherboard uses**.
