---
audio: false
generated: true
image: false
lang: en
layout: post
title: Measuring PEX Rail on GPUs
translated: false
type: note
---

Question: How do you measure the PEX power rail on a graphics card?

Answer:

To test the PEX rail on an NVIDIA GPU (like the RTX 3070 shown), repair technicians use a multimeter to measure both **Resistance to Ground** (unpowered) and **Voltage Output** (powered).

1. **Measure Resistance to Ground:** Unpowered Test.
Turn off power, unplug the card, and set your multimeter to Resistance ($\Omega$) or Diode mode. Place the black probe on a PCI slot ground pin or shield, and place the red probe on the output inductor/capacitor of the PEX power IC.


2. **Verify Resistance Value:** Diagnosis.
Compare your reading to target values. On Ampere GPUs like the RTX 3070, expected resistance for the PEX rail is typically around tens to hundreds of ohms (varies by controller). A reading close to $0\,\Omega$ indicates a short circuit, often caused by a shorted filter capacitor or damaged GPU die.


3. **Measure Voltage Output:** Powered Test.
If no short is present, connect the card to power/riser board, power on the system, and set your meter to DC Voltage ($V\dots$). Probe the PEX inductor or output pin while holding the black probe to ground. Verify the output voltage reaches the target nominal level (typically $\approx 1.0\text{V}$ or $1.8\text{V}$ depending on the generation).


* **How to verify success:** A normal resistance reading above $10\,\Omega$ confirms no dead short to ground; a stable voltage output matching spec during powered testing confirms the PEX power stage and controller are functioning properly.
