---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASM1083 PCIe-to-PCI Bridge
translated: false
type: note
---

**Question:** What is the ASMedia ASM1083 chip on the MSI B85M-E45 motherboard?

**Answer:**

The ASMedia ASM1083 on the MSI B85M-E45 is a **PCIe-to-PCI bridge controller** — essentially a compatibility chip that allows the modern motherboard to still offer legacy PCI slots.

Here's what it does and why it's there:

**Role on the MSI B85M-E45**

The Intel B85 chipset is a modern platform that natively supports PCIe (PCI Express) but no longer has built-in support for old-style PCI slots. MSI added the ASM1083 chip to bridge that gap, so the board could include one or more traditional PCI expansion slots alongside the native PCIe slots.

**How it works**

The ASM1083 is an x1 PCI Express to 32-bit PCI bridge, enabling users to connect legacy parallel bus devices to the advanced serial PCI Express interface. In other words, it converts one PCIe lane from the chipset into a PCI bus that your older expansion cards can use.

The ASM1083 is a PCI Express-to-PCI forward bridge, fully compliant with the PCI-SIG PCI Express-to-PCI Bridge Specification 1.0.

**Key specs**

- Bridges: x1 PCIe → 32-bit PCI bus
- Supports up to 3 PCI slots from one bridge chip
- Features include I²C Serial EEPROM support, extensive PME (Power Management Events) support, 3.3V/1.2V power supply, and legacy mode support

**Do you need drivers?**

This chip requires no additional drivers to function — however, the devices bridged by this chip (i.e., cards you plug into the PCI slot) will require their own drivers.

**In plain terms:** The ASM1083 is what makes the old PCI slots on your B85M-E45 work on a modern motherboard. Without it, the board would only have PCIe slots.

---

**References:**

- [ASM1083 Product Page – ASMedia Technology](https://www.asmedia.com.tw/product/E8AyQ44sX3zPbruF/2f2yq89xz7URBZqD.html)
- [ASM1083 Datasheet Summary – Datasheetcafe](https://www.datasheetcafe.com/asm1083-datasheet-controller/)
- [ASM1083 Chip Info – TheRetroWeb](https://theretroweb.com/chips/5897)
- [ASM1083 Driver Info – OEMDrivers](https://oemdrivers.com/pcie-asmedia-asm1083-pcie-to-pci-bridge)
