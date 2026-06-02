---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo B490 BIOS Guide Overview
translated: false
type: note
---

**Question: Introduction to the Lenovo G490 product and its InsydeH2O Setup Utility BIOS**

**Answer:**

The **Lenovo G490** does not appear to be an official or widely documented Lenovo laptop model based on available information. It is very likely a typo or misremembering of the **Lenovo B490**, which was a real budget/business-oriented laptop released around 2012–2013 as part of Lenovo's Essential B Series (similar to models like B480/B490/B590). There is no evidence of a "G490" product in Lenovo's lineup from that era or later; Lenovo's G series included models like G400/G500/G40, but no G490 matches the description. The following introduction is therefore based on the closely related and well-documented **Lenovo B490**.

### Lenovo B490 (likely intended as G490) Overview

The Lenovo B490 was a 14-inch entry-level/business notebook designed for home and office use, emphasizing reliable performance, security features, and affordability.

**Key specifications** (varied by configuration):

- **Display**: 14.0-inch HD (1366×768 resolution), high-glossy finish
- **Processor**: 3rd-generation Intel options, including:
  - Intel Core i3 or i5 (HM77 chipset models)
  - Intel Pentium or Celeron (HM70 chipset models)
- **Graphics**: Integrated Intel HD Graphics; some models had switchable discrete NVIDIA GeForce GT 635M (1GB) or GeForce 610M (1GB) via NVIDIA Optimus technology
- **Memory**: Up to 8GB DDR3-1600 MHz (2 slots on higher models; 1 slot/4GB max on lower models)
- **Storage**: 2.5-inch HDD (320GB–1TB, 5400 or 7200 RPM); some supported performance booster features
- **Optical Drive**: DVD/CD multi-burner (on most models)
- **Connectivity**: USB 3.0 (1–2 ports), USB 2.0 (2 ports), HDMI, VGA, RJ-45 Ethernet, 4-in-1 card reader, combo audio jack
- **Wireless**: Integrated Wi-Fi (802.11b/g/n), optional Bluetooth combo; Gigabit Ethernet
- **Other features**: Webcam (0.3MP or 720p HD), stereo speakers, AccuType keyboard, optional fingerprint reader, one-key recovery button
- **Battery**: 6-cell Li-Ion (up to ~5–6 hours depending on configuration)
- **Weight and dimensions**: ~2.2 kg (4.9 lbs), 340 × 234.6 × 33.1 mm
- **Operating systems**: Originally shipped with Windows 7 (various editions), Windows 8, or FreeDOS/Ubuntu in some regions

It was positioned as a durable, practical machine with good build quality for its class (e.g., "stone crush" finish in some descriptions) and business-friendly features like enhanced security.

### InsydeH2O Setup Utility (BIOS)

The Lenovo B490 (and many other Lenovo laptops from that generation, especially B/E/G/IdeaPad series) used **InsydeH2O** as its BIOS/UEFI firmware. InsydeH2O (Hardware-2-Operating System) was a common BIOS provider for OEM laptops in the early 2010s, including many Lenovo models.

**How to access the BIOS Setup Utility**:

- Power on or restart the laptop.
- Immediately and repeatedly press **F2** (or sometimes **Fn + F2**) during the Lenovo logo screen.
- For older Lenovo B-series models like the B490, you could also use the small **Novo Button** (a pinhole/recovery button usually on the side or near the power button): Press it while the laptop is off to bring up a menu, then select "BIOS Setup".

**Typical InsydeH2O BIOS interface on such models**:

- It features tabs like **Information**, **Configuration**, **Security**, **Boot**, and **Exit**.
- You can view system info (CPU, memory, etc.), adjust boot order, enable/disable devices (e.g., USB boot, webcam), set supervisor/user passwords, configure date/time, and restore defaults.
- Navigation uses arrow keys, Enter to select, Esc to go back, and often **F9** for defaults + **F10** to save and exit.
- Some Lenovo InsydeH2O versions had limited/hidden advanced options unless unlocked via specific key combinations (not standard on B490-era models).

**Notes**:

- This BIOS is legacy (pre-full UEFI on many units), though some configurations supported UEFI mode.
- Common issues included boot loops into BIOS (often due to dead CMOS battery, wrong boot order, or HDD failure).
- For modern use (e.g., installing newer OS like Windows 10/11), users often needed to enable Legacy/CSM boot if UEFI was problematic, or replace the old HDD with an SSD.

If this does not match your exact laptop (e.g., if it is actually a different model like G400/G410 or ThinkPad T490), provide more details such as the exact model number from the bottom sticker or processor generation for more accurate information.

**References:**

- [Lenovo B490/B590 Datasheet (PDF)](https://marmaxcomputers.com/img/171020014731b490_b590_ds_en-1-.pdf)
- [Lenovo B490 User Guide (PDF)](https://download.lenovo.com/pccbbs/mobiles_pdf/b490_b590_ug_en.pdf)
- [Lenovo Support - B490 Product Page](https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/lenovo-b-series-laptops/lenovo-b490-notebook/20205)
