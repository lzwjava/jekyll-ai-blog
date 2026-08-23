---
audio: false
generated: true
image: false
lang: en
layout: post
title: F_USB2 Front Panel USB Header
translated: false
type: note
---

**Question:** What is the F_USB2 port/header on the GA-H81M-DS2 motherboard?

**Answer:**

**F_USB2** is an internal **front panel USB 2.0 header** on the motherboard — it is **not** a port you plug a USB device into directly. It's a **pin header (connector block)** on the PCB that connects to your **PC case's front USB ports** via a cable.

---

### Physical Details

- It is a **9-pin header** (2×5 grid, with 1 pin missing as a key/guide)
- Provides **2 USB 2.0 ports** when connected to the case front panel cable
- Supports speeds up to **480 Mbps** (USB 2.0 standard)

---

### Pin Layout

```
Pin 1  - VCC (Power +5V)    | Pin 2  - VCC (Power +5V)
Pin 3  - USB0-             | Pin 4  - USB1-
Pin 5  - USB0+             | Pin 6  - USB1+
Pin 7  - GND               | Pin 8  - GND
Pin 9  - No Pin (key)      | Pin 10 - NC
```

---

### The GA-H81M-DS2 Has Two Such Headers

| Header | Label | What it connects to |
|---|---|---|
| First | **F_USB1** | Front panel USB (ports 1–2) |
| Second | **F_USB2** | Front panel USB (ports 3–4) |

So **F_USB2** is simply the **second front USB 2.0 header**, giving your case extra front USB ports if the case cable supports it.

---

### Common Uses / Notes

- If your **case only has one front USB 2.0 cable**, F_USB2 is left unpopulated — that's completely normal
- You can also plug **internal USB devices** into it (e.g., Bluetooth adapter dongle, USB fan controller, front card readers)
- Do **not** connect a USB 3.0 cable to it — the connector is physically different and incompatible
- The board also has a separate **F_USB30** header for USB 3.0 front panel connections

---

**References:**
- [GA-H81M-DS2 User's Manual — Chapter 1 Hardware Installation (Gigabyte PDF)](https://download.gigabyte.com/FileList/Manual/mb_manual_ga-h81m-ds2_4001_e.pdf)
