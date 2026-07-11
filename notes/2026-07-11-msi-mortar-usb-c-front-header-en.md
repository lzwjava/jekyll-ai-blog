---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Mortar USB-C Front Header
translated: false
type: note
---

**Question:** What is the black box component visible in the top-right corner of these MSI Mortar / Mortar II motherboard photos, near the SATA ports?

**Answer:**

That's the **internal USB Type-C front-panel header** (MSI labels it `JUSBC1` on Mortar-series boards).

Key identification points:

- **Shape** — unlike the pin-array headers for USB 2.0 (`JUSB1/2`) or USB 3.2 Gen1 Type-A (which are 2×10 pin headers with visible pins), the USB-C internal header is a **single molded plastic block** with an internal keyed slot. That's exactly what you're seeing — a solid black box, not rows of pins.
- **Position** — on Mortar/Mortar II boards this header sits right next to the SATA ports, close to `JTPM1` and `JFP1`, which matches both your screenshots (you can see `JTPM1` and `JFP1` labels right below it in image 1).
- **Function** — it lets you run a cable from this header to a **USB-C port on your case's front panel**, giving you a front USB-C connection at 10Gbps (USB 3.2 Gen 2) on most B650/B850 Mortar boards, or 5Gbps (Gen1) on older B450/B550 Mortar boards.

For confirmation on your exact board revision, check the MSI manual for whichever Mortar chipset you have — the MAG B850M Mortar WIFI user guide explicitly lists "JUSBC1: USB 10Gbps Type-C® Front Panel Connectors" in its connector table, right alongside the SATA and TPM headers, matching the layout in your photos.

If your case has a front-panel USB-C port with a matching keyed cable, that's exactly where it plugs in. If you don't have a USB-C front port, this header just goes unused — it's optional, not required for the board to boot.

References:

- [MAG B850M MORTAR WIFI User Guide (PDF)](https://download-2.msi.com/archive/mnu_exe/mb/MAGB850MMORTARWIFI_English.pdf)
- [MAG B550M MORTAR Specification](https://www.msi.com/Motherboard/MAG-B550M-MORTAR/Specification)
