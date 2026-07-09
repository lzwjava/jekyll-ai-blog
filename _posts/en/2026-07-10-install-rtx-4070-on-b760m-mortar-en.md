---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install RTX 4070 on B760M Mortar
translated: false
type: note
---

Question: How do I physically install an MSI GeForce RTX 4070 graphics card into an MSI MAG B760M Mortar motherboard, and what are these two components?

Answer:

## What these two parts are

**MSI MAG B760M Mortar** — a micro-ATX motherboard, Intel B760 chipset, LGA1700 socket (12th/13th gen Core, Pentium Gold, Celeron). Relevant to your GPU install: it has a PCIe 5.0/4.0/3.0 x16 slot with steel armor reinforcement, and the top slot is reinforced, attaches through the CPU, and runs up to PCIe 5.0 x16 speeds, while a second full-length slot connects through the chipset at PCIe 4.0 x4. So you get exactly one true x16 electrical slot — that's the one you want the GPU in.

**MSI GeForce RTX 4070** — Ada Lovelace GPU, 12GB GDDR6X, PCIe Gen4 interface. Depending on which SKU you bought (Gaming X Trio, Ventus, etc.), power draw and connector differ slightly. The Gaming X Trio 12G variant: power consumption 215W, 16-pin power connector, recommended PSU 650W, card dimensions 338 x 141 x 52 mm. That 16-pin connector is the 12VHPWR/12V-2x6 style — your PSU either has a native 12VHPWR cable, or the card ships with an adapter that takes 2-3x 8-pin PCIe from your PSU.

## Physical installation steps

1. **Power off and unplug the PSU.** Ground yourself (touch the case chassis, or wear an anti-static wrist strap).

2. **Locate the correct slot.** On the B760M Mortar, use `PCI_E1` — the top, CPU-attached x16 slot with the metal "Steel Armor" shroud. Don't use the lower chipset-linked slot; it's electrically x4 and will bottleneck the 4070 hard.

3. **Remove the rear I/O slot covers** on your case corresponding to the card's height (the 4070 is a triple-slot card typically, so remove 2-3 brackets).

4. **Open the PCIe slot latch** at the end of `PCI_E1` (the reinforced clip — MSI's "enlarged PCI-E clip" is designed for easy insertion/removal without tools).

5. **Align and seat the card.** Line up the GPU's PCIe edge connector with the slot, hold the card level, and press straight down evenly at both ends until you hear/feel the latch click closed and the card sits flush against the slot.

6. **Screw the bracket into the case** at the rear (1-2 screws depending on how many slots it occupies).

7. **Connect the power cable(s).** Plug the 16-pin 12VHPWR cable directly from your PSU if it's ATX 3.0/3.1 native, or use the supplied adapter connecting 2-3x 8-pin PCIe from the PSU into the adapter, then the adapter's single 16-pin plug into the card. Make sure it's **fully seated** — a half-inserted 12VHPWR connector is the known failure mode (melting) people report.

8. **Physical support check.** At 338mm long and ~1.2kg, verify your case has clearance and consider a GPU support bracket/anti-sag brace since micro-ATX cases sometimes have shorter GPU clearance — measure before buying if you haven't already.

9. **Power on, enter BIOS (Del key), confirm the GPU is detected** under PCIe device list, then boot into your OS.

10. **Driver setup.** On Linux (given your workstation is Ubuntu-capable): install the NVIDIA proprietary driver via `ubuntu-drivers devices` then `sudo ubuntu-drivers autoinstall`, or grab CUDA toolkit directly if you're going to run training workloads on this card too:

```bash
# Ubuntu — check recommended driver
ubuntu-drivers devices

# Install
sudo ubuntu-drivers autoinstall
sudo reboot

# Verify
nvidia-smi
```

## One thing worth flagging for your setup

Your 192.168.1.36 workstation already lists RTX 4070 12GB — if this is a *second* GPU or an upgrade to that box, check your PSU headroom against whatever else is drawing power (CPU, other GPU if any). The bare minimum for an RTX 4070 is 3x 8-pin PCIe connectors or a 450W-capable PCIe Gen5 power cable, but MSI's own recommendation for the Gaming X Trio is 650W — different board partners recommend different PSU wattages, so always check the spec sheet for your exact card.

References:

- [MSI MAG B760M Mortar WIFI review — Tom's Hardware](https://www.tomshardware.com/reviews/msi-mag-b760m-mortar-wifi-review)
- [MSI MAG B760M MORTAR WIFI — Newegg spec sheet](https://www.newegg.com/msi-mag-b760m-mortar-wifi-micro-atx-motherboard-intel-b760-lga-1700/p/N82E16813144586)
- [MSI GeForce RTX 4070 GAMING X TRIO 12G specs](https://www.msi.com/Graphics-Card/GeForce-RTX-4070-GAMING-X-TRIO-12G/Specification)
- [Corsair — What PSU is best for RTX 4070](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/what-psu-is-best-for-rtx-4070/)
