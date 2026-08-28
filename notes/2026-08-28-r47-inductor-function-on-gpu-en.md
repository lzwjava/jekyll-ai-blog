---
audio: false
generated: true
image: false
lang: en
layout: post
title: R47 Inductor Function on GPU
translated: false
type: note
---

**Question:** What does the **R47** component do on a GPU (like the NVIDIA Quadro 410)?

**Answer:**

"R47" on a GPU PCB is most commonly a **power inductor (coil/choke)** — not a resistor, despite the "R" prefix being confusing.

The "R" in "R47" is used as a **decimal point** in SMD inductor marking convention. So **R47 = 0.47 µH** (microhenries). This is a standard notation for inductance values below 1 µH.

**What does it do?**

The R47 labeled component is a **storage inductor**, and it is part of the circuit used to convert 12V (from the PCIe power input) down into the lower regulated voltage needed by the GPU core or memory — for example, turning 12V into the memory voltage.

On some cards, the R47 inductor is part of the voltage regulator for memory (like HBM) internal voltage — typically around 0.8V on the output.

**In the context of APM8720 + VP57F (your previous question):**

The R47 inductor works **together** with those components as part of the **VRM (Voltage Regulator Module)** buck converter circuit:

- **APM8720** = PWM controller (brain)
- **VP57F MOSFETs** = switching transistors (muscle)
- **R47 (0.47 µH inductor)** = energy storage coil (smooths the switched power into clean DC)
- Capacitors alongside it = filter out ripple voltage

On GPU cards, you typically find several R22 (0.22 µH) and one or two R47 (0.47 µH) inductors. For the R47, the spec is typically around 0.0033 Ω DC resistance and 10A current rating.

**In short:** R47 is a **0.47 µH power inductor** — a critical part of the GPU's voltage regulation circuit that ensures stable, clean power delivery to the GPU core or VRAM.

**References:**

- [SMD Inductor Marking Guide — Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/smd-inductor-identification-reading-markings-testing-guide)
- [Burned R47 on GPU — iFixit](https://www.ifixit.com/Answers/View/232421/Burned+resistor+on+GPU)
- [Fried R47 on GTX 1080 — AnandTech Forums](https://forums.anandtech.com/threads/fried-resistor-and-vrm-on-gtx-1080.2543963/)
- [GTX 770 R47 Inductor — HardForum](https://hardforum.com/threads/gtx-770-series-need-inductor-update-fixed-it.1953238/)
