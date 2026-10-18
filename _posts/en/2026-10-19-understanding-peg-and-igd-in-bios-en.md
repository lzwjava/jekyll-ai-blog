---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding PEG and IGD in BIOS
translated: false
type: note
---

Question: In BIOS, what do **PEG** and **IGD** mean under the "Initiate Graphic Adapter" setting?

---

Answer:

**"Initiate Graphic Adapter"** (also called *Primary Display*, *Init Display First*, or *Initial Display Output* depending on the motherboard brand) is a BIOS/UEFI setting that controls **which graphics adapter the system initializes first during boot**.

The two main options are:

| Option | Full Name | What It Means |
|--------|-----------|---------------|
| **PEG** | PCI Express Graphics | Use the **discrete (dedicated) GPU** plugged into the PCIe slot (e.g., NVIDIA GeForce, AMD Radeon) |
| **IGD** | Integrated Graphics Device | Use the **built-in graphics** inside the CPU or motherboard chipset (e.g., Intel UHD Graphics, AMD Radeon integrated) |

**When to choose which:**

- **PEG** — select this when you have a dedicated graphics card installed and want it to handle the display output from the very beginning of boot. On MSI firmware, for example, this setting path is: *Settings → Advanced → Integrated Graphics Configuration → Initiate Graphic Adapter → PEG*.

- **IGD** — select this when you want the integrated graphics to be initialized first. If the priority is set to PEG (Offboard), the system will skip IGD initialization, which means the integrated GPU may not even appear in Device Manager.

**Practical tip:** If you set IGD as primary but your monitor is plugged into the discrete GPU, you'll get no display during boot — only after the OS loads does the dedicated card take over. Always connect your monitor to whichever adapter is set as primary.

---

References:

- [Initiate Graphic Adapter – PEG vs IGD (cloudspress.com)](https://www.cloudspress.com/?p=813460)
- [How to Change Default Display Adapter in BIOS (freedom251.com)](https://freedom251.com/?p=456)
- [MSI BIOS – Initiate Graphic Adapter setting (yomotherboard.com)](https://yomotherboard.com/question/how-can-i-stop-my-bios-from-using-onboard-graphics/)
- [Supermicro FAQ – IGD initialization priority](https://www.supermicro.com/zh_tw/support/faqs/faq.php?faq=16307)
