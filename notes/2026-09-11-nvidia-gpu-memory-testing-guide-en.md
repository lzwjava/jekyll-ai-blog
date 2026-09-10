---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nvidia GPU Memory Testing Guide
translated: false
type: note
---

Question: Explain the Nvidia GPU memory testing guide from the YouTube video.

Answer:
This video by Fraser from **GPU Solutions** demonstrates a custom, menu-driven USB bootable tool designed for technicians to diagnose Nvidia GPU memory errors using **MODS**, **MATS**, and **NVMT**.

---

### Key Workflow Guidelines by VRAM Type

* **GDDR6 (RTX 20 Series, RTX 3050–3070)**
* **Setup:** Connect the monitor directly to the dedicated GPU and set the BIOS Primary Display to `Auto` or `PEG`/`PCIe`.
* **Primary Diagnostic Tool:** **MATS** [[12:16](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D736)].
* **Note:** MODS and NVMT are not required for standard GDDR6 diagnostics.

* **GDDR6X & GDDR7 (RTX 3070 Ti–3090 Ti, RTX 40 Series, RTX 50 Series)**
* **Setup:** Connect the monitor to the CPU's integrated graphics (**iGPU**) and set the BIOS Primary Display to `IGFX` [[04:58](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D298)].
* **Primary Diagnostic Tool:** **MODS** [[07:23](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D443)].
* **Note:** If a card with GDDR6X or GDDR7 outputs a functional display image, running MODS will return a `100021` error code, indicating there are no memory errors [[09:45](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D585)].

---

### Interpreting Diagnostic Test Results

1. **MODS Frame Buffer (FBPA) Reports:**
Look at the final digit of the hex value for each memory channel:

* **Ending in `0`:** No errors (Healthy) [[06:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D375)]
* **Ending in `2`:** Bank 0 is faulty [[06:25](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D385)]
* **Ending in `8`:** Bank 1 is faulty [[06:25](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D385)]
* **Ending in `A`:** Both Bank 0 and Bank 1 are faulty [[06:35](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D395)]

2. **Fault Patterns & Repair Paths:**

* **Localized Channel Failures:** Points to physical GDDR chip failure or broken solder joints [[06:47](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D407)].
* **Widespread Errors Across Multiple Channels:** Typically indicates a damaged GPU core memory controller rather than multiple individual VRAM chips dying simultaneously [[13:02](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D782), [16:16](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D976)].

3. **NVMT Warning:**

* **NVMT** can report false-positive errors on fully functional GPUs, so it should never be used as a standalone diagnostic tool [[10:43](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D643)].

---

References:

* [How to Test Nvidia GPU Memory Errors | MATS, MODS and GDDR6/GDDR6X Guide](http://www.youtube.com/watch?v=jh5V2onzAV4)
