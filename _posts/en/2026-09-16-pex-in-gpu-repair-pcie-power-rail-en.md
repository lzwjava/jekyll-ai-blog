---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PEX in GPU Repair: PCIe Power Rail"
translated: false
type: note
---

Question: What does PEX mean in this context?

Answer:
In graphics card (GPU) repair and hardware engineering, **PEX** stands for **PCI Express (PCIe)**, specifically referring to the **PCIe main power domain / rail** (often labeled as `NVVDD_PEX`, `PEX_VDD`, or `1.8V PEX` on NVIDIA schematics).

In the video frame, the technician is measuring components on a Gigabyte RTX 3070 board using a multimeter/probe. In board repair terminology, "PEX" usually refers to one of the following:

* **PEX Power Rail (`PEX_VDD` / `1.8V_PEX`):** The dedicated power supply voltage required by the GPU core's PCIe interface logic to communicate with the motherboard. Technicians frequently check this rail for shorts, correct resistance to ground, or proper voltage output when diagnosing a card that is not detected or fails to post.
* **PCI Express Interface (PCIe):** NVIDIA often uses the "PEX" abbreviation in board silkscreen labels, schematics, and signal names (e.g., PEX_RESET, PEX_CLK) to designate PCIe-related circuits.
