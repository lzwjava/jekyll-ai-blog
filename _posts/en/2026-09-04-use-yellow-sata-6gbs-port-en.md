---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Yellow SATA 6Gb/s Port
translated: false
type: note
---

**Question:** Which SATA port on the ASUS H81M-K should I connect my WD 1TB (WD10EZEX) to — the yellow (SATA 6Gb/s) or the black/dark brown (SATA 3Gb/s)?

---

**Answer:**

**Use the Yellow port (SATA 6Gb/s).**

Here's why:

**Your drive supports SATA 6Gb/s.**
The WD10EZEX is a SATA 6Gb/s drive with a 64MB cache running at 7200 RPM. So it natively operates at the faster standard.

**Your board's port colors:**
The ASUS H81M-K has 2 × SATA 6Gb/s ports (yellow) and 2 × SATA 3Gb/s ports (dark brown/black).

So connect the WD10EZEX to one of the **two yellow ports** labeled **SATA6G**.

---

**Does it matter in practice for a mechanical HDD?**

Honestly, not much in real-world use. A 7200 RPM mechanical hard drive maxes out around 150–180 MB/s sequentially, which is well within what even SATA 3Gb/s (~300 MB/s) can handle. For a mechanical HDD it doesn't really matter which port you use — it only makes a noticeable difference for SATA SSDs.

But best practice is still to use the yellow SATA 6Gb/s port — it's the correct native speed for the drive, and it keeps your faster ports free for an SSD if you add one later.

---

**Summary table:**

| Port Color | Speed | Use for |
| --- | --- | --- |
| **Yellow** ✅ | SATA 6Gb/s | WD10EZEX (recommended) |
| Black/Dark Brown | SATA 3Gb/s | Optical drives, older HDDs |

---

**References:**

- [ASUS H81M-K Tech Specs](https://www.asus.com/rs-en/motherboards-components/motherboards/business/h81mk/techspec/)
- [WD10EZEX SATA-IO Certification](https://sata-io.org/product/8850)
- [Tom's Hardware – SATA port color discussion](https://forums.tomshardware.com/threads/asus-h81m-plus-sata-slots.3703153/)
