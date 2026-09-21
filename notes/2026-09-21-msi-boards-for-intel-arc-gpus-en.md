---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Boards for Intel Arc GPUs
translated: false
type: note
---

**Question:** Which MSI motherboards in the ReBarUEFI working-board list are known to work with Intel Arc GPUs?

**Answer:** Yes. From the MSI boards you listed, these are the relevant ones:

| MSI board             | Intel Arc / ReBarUEFI relevance             |
| --------------------- | ------------------------------------------- |
| **Z170-A PRO**        | ✅ Confirmed in ReBarUEFI working-board list |
| **Z170A Gaming M5**   | ✅ Confirmed                                 |
| **Z270-A PRO**        | ✅ Confirmed                                 |
| **Z270 GAMING M5**    | ✅ Confirmed                                 |
| **Z97 Gaming 3**      | ✅ Confirmed                                 |
| **Z97 Gaming 5**      | ✅ Confirmed                                 |
| **B150M Bazooka**     | ✅ Confirmed                                 |
| **B150M Plus**        | ✅ Confirmed                                 |
| **H110M Gaming**      | ✅ Confirmed                                 |
| **C236M WORKSTATION** | ✅ Confirmed                                 |
| **H97M-G43**          | ✅ Confirmed                                 |

The important distinction is that **ReBarUEFI working ≠ Intel Arc officially supported by MSI**. ReBarUEFI is specifically enabling the PCIe Resizable BAR capability that Arc GPUs benefit heavily from.

For an Intel Arc GPU, I'd pay particular attention to the **Z170/Z270 MSI boards**:

* **Z170-A PRO**
* **Z170A Gaming M5**
* **Z270-A PRO**
* **Z270 GAMING M5**

These are newer than the Z97/H97 options and use Intel 100/200-series platforms, so they're generally a more straightforward starting point for an Arc + ReBarUEFI experiment.

One caveat: **Arc itself has platform requirements beyond ReBAR**. Intel's modern Arc cards expect **UEFI boot + Above 4G Decoding + ReBAR**, and older platforms can additionally run into PCIe/firmware/CSM quirks. So the exact CPU + Arc model matters.

If you're choosing a board specifically for something like **Arc A770/A750/B580**, I can cross-reference the ReBarUEFI reports against Intel's Arc requirements and identify the MSI boards that are most practical rather than merely appearing in the working-board list.