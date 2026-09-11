---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multimeter Testing RTX Graphics Card
translated: false
type: note
---

Question: How do I use a multimeter to test an RTX graphics card using ground, power pin, and PCIe slot measurements?

Answer:

Testing an NVIDIA RTX graphics card with a multimeter is primarily done through **resistance-to-ground (continuity) checks** to identify short circuits before applying power, or **voltage checks** while the card is powered on.

### 1. Resistance Mode Setup (Unpowered Card)

Set your multimeter to **Resistance mode ($\Omega$)** or **Continuity/Diode mode**.

1. **Ground Connection:** Place the **black probe** on a clean, unpainted metallic ground point (such as the metal I/O bracket, PCIe ground pads, or the screw hole rings).
2. **Signal / Power Connection:** Place the **red probe** on the specific pin or rail you want to measure.

### 2. Primary Power Rail Checkpoints (PCIe Connector & Slot)

Measure the resistance between ground (black probe) and each of the primary power inputs using the red probe:

* **PCIe Slot 12V Rail:** Test pins 1, 2, and 3 on the top side of the PCIe connector (front edge, left side). Resistance should be in the **kilo-ohms ($k\Omega$) range or higher**. A reading close to $0\,\Omega$ indicates a shorted input MOSFET or capacitor.
* **PCIe Slot 3.3V Rail:** Test pin 10 on the top side of the PCIe connector. Resistance should be in the **hundreds of ohms to $k\Omega$ range**.
* **Auxiliary Power Connectors (8-Pin / 12VHPWR / 12V-2x6):** Test the top row pins of the 8-pin or 12VHPWR power connectors. These supply the main 12V input to the VCORE and VMEM VRMs. Resistance should be in the **$k\Omega$ range**.

### 3. Core, Memory, and Auxiliary Rail Resistances

Modern RTX GPUs have very low internal resistance on logic rails due to high current demands:

* **VCORE (GPU Core Rail):** Measure across the inductors/coils around the main GPU chip. Expect a very low reading, typically between **$0.2\,\Omega$ and $2.0\,\Omega$** depending on the specific RTX generation (RTX 30/40 series run very low).
* **VMEM (Memory Rail):** Measure across the memory power inductors. Expect roughly **$20\,\Omega$ to $100\,\Omega$**.
* **PEX / 1.8V Rail:** Measure near the display controllers or BIOS chip. Expect **hundreds of ohms ($100\,\Omega - 1000\,\Omega$)**.

*How to verify:* If any primary 12V input rail shows near $0\,\Omega$ (short to ground), do **not** plug the card into a system, as it will trigger your power supply's safety trip or destroy traces on the PCB.
