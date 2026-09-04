---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX 12V Connector Is Required
translated: false
type: note
---

**Question:** What is the ATX 12V connector used for on a motherboard, and is it required to plug it in?

**Answer:**

**What ATX 12V is used for:**

The 4-pin ATX 12V connector supplies **dedicated 12V power specifically to the CPU**. It feeds the **VRM (Voltage Regulator Module)**, which then steps the voltage down to the precise level the CPU needs to operate. Without it, the CPU has no power source regardless of whether the 24-pin main connector is plugged in.

**Do you need to plug it in?**

**Yes — absolutely required.** If you forget to connect the 4-pin ATX 12V power plug, the system will not boot up.

Here's a quick summary of both main power connectors:

| Connector | Pins | Powers |
| --- | --- | --- |
| EATXPWR | 24-pin | Motherboard, RAM, PCIe slots, storage |
| ATX12V | 4-pin | CPU only (via VRM) |

**Common symptoms if ATX 12V is not plugged in:**

- System powers on (fans spin, LEDs light) but **no POST / no display**
- Immediate shutdown after pressing power
- Continuous reboot loop

ASUS recommends using an ATX 12V Specification 2.0-compliant power supply unit (PSU) with a minimum of 300W power rating for the H81M-K.

So in short — **never skip it**. It is just as critical as the 24-pin connector.

---

**References:**

- [ASUS H81M-K User Manual – ATX Power Connectors (Page 25)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=25)
- [ASUS H81M-K Layout Contents (Page 12)](https://www.manualowl.com/m/Asus/H81M-K/Manual/372249?page=12)
