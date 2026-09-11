---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3060 12GB Partial VRAM Normal
translated: false
type: note
---

Question: **RTX 3060 12GB has only 6 VRAM chips populated, with M2 and M5 empty — is that normal?**

Answer: **Yes, very likely normal.** This is actually the standard design for many RTX 3060 12GB boards.

The RTX 3060 12GB uses:

* **6 × 2GB GDDR6 chips = 12GB**
* **192-bit memory bus**
* Each chip corresponds to a **32-bit memory channel**
* Therefore: `6 × 32-bit = 192-bit`

For example, a teardown of the EVGA RTX 3060 XC shows **six Samsung GDDR6 chips**, while two additional memory positions on the PCB are unused. ([Tom's Hardware][1])

MSI's RTX 3060 12GB also officially specifies **12GB / 192-bit**, and PCB photos show unused memory positions. ([Notebookcheck][2])

So if your board looks like:

```text
M1  [VRAM]
M2  [EMPTY]   ← normal
M3  [VRAM]
M4  [VRAM]
M5  [EMPTY]   ← normal
M6  [VRAM]
M7  [VRAM]
M8  [VRAM]
```

and GPU-Z reports:

```text
Memory Size: 12288 MB
Memory Bus Width: 192 bit
```

then **there is probably nothing missing or broken**.

In fact, this is useful to know for GPU repair: **don't automatically interpret an empty VRAM footprint as a missing component.** Manufacturers frequently reuse PCBs across different products/configurations. The RTX 3060 PCB family can have additional unpopulated memory locations. ([Tom's Hardware][1])

If you send me a **clear photo of the RTX 3060 PCB around M1–M8**, I can identify whether **M2/M5 are intentionally unpopulated or whether they look like chips that were physically removed**.

References:

* [Nvidia GeForce RTX 3060 review / PCB teardown — Tom's Hardware](https://www.tomshardware.com/reviews/nvidia-geforce-rtx-3060-review/2?utm_source=chatgpt.com)
* [MSI RTX 3060 GAMING 12G specifications](https://www.msi.com/Graphics-Card/GeForce-RTX-3060-GAMING-12G/Specification?utm_source=chatgpt.com)
* [MSI RTX 3060 PCB analysis — Notebookcheck](https://www.notebookcheck.net/First-look-at-MSI-s-custom-RTX-3060-PCB-design-for-the-Gaming-X-series.523982.0.html?utm_source=chatgpt.com)

[1]: https://www.tomshardware.com/reviews/nvidia-geforce-rtx-3060-review/2?utm_source=chatgpt.com "EVGA GeForce RTX 3060 XC Teardown - Nvidia GeForce RTX 3060 12GB Review: Hope Springs Eternal - Page 2 | Tom's Hardware"
[2]: https://www.notebookcheck.net/First-look-at-MSI-s-custom-RTX-3060-PCB-design-for-the-Gaming-X-series.523982.0.html?utm_source=chatgpt.com "First look at MSI's custom RTX 3060 PCB design for the Gaming X series - Notebookcheck News"
