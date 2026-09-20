---
audio: false
generated: true
image: false
lang: en
layout: post
title: Easy BIOS Boards for ReBarUEFI
translated: false
type: note
---

**Question:** For boards where a BIOS image is easy to find (to use with ReBarUEFI), which ones does the working-board list point to?

**Answer:**

Looking at the ReBarUEFI [working motherboards list](https://github.com/xCuri0/ReBarUEFI/issues/11), the boards with the **easiest-to-obtain BIOS images** fall into these categories:

---

### ✅ Tier 1: Official download, no tricks needed

These manufacturers keep clean, publicly accessible BIOS archives:

| Board Family | Why Easy |
|---|---|
| **ASUS Z97 / Z170 / Z270 / X99** (e.g. Z170-A, Maximus VIII Hero, X99-DELUXE) | ASUS support site has direct BIOS downloads by model, no login |
| **MSI Z97 / B150M / Z170 / Z270** (e.g. Z97 Gaming 5, B150M Bazooka) | MSI download center, straightforward |
| **Gigabyte B75M / Z68 / Z170 / B450** | Gigabyte support, all BIOS revisions kept |
| **ASRock Z97 / Z170 / X99** | ASRock download center, stable |
| **Supermicro X9/X10/X11** | Official BIOS packages on supermicro.com, many users in the list succeeded with these |

---

### ✅ Tier 2: Chinese X99/X79 boards (Huananzhi, Machinist, Jingsha)

Multiple users confirmed success with boards like Huananzhi X99-QD4, X99-TF, X99-F8, and Machinist X99-MR9A Pro — and importantly, **these boards do NOT need UEFIPatch** in most cases. Their BIOS files are freely distributed on the seller's own pages, Taobao stores, or community mirrors. Easy to find via a search for the exact model + "BIOS download."

---

### ⚠️ Tier 3: Hard — your SY-B85N case

The B85-chipset boards in the list are absent — no B85 board appears in confirmed working entries, which matches the original finding: SOYO dropped support and the BIOS image simply isn't publicly mirrored anymore. The CH341A dump approach remains the only reliable path.

---

### Practical Recommendation

If you want a **B85-era board with an easily found BIOS**, consider switching to one of these confirmed-working alternatives that have public BIOS downloads:

- **MSI H97M-G43** — confirmed working, MSI download center
- **ASUS Z97-K / Z97-P / Z97-Pro** — confirmed working, ASUS support
- **ASRock Z97 Extreme4 / Z97 Anniversary** — confirmed working, ASRock support

All are LGA1150 like B85, so your existing Haswell CPU carries over. They also share the same `HswAbove4G.txt` patch requirement.

---

**References:**
- [ReBarUEFI GitHub — Working Motherboards List (Issue #11)](https://github.com/xCuri0/ReBarUEFI/issues/11)
- [ReBarUEFI Main Repository](https://github.com/xCuri0/ReBarUEFI)
