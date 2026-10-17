---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enter Dell BIOS to Install Ubuntu
translated: false
type: note
---

**Question:** How do I restart a Dell laptop and enter BIOS in order to install Ubuntu?

---

**Answer:**

## Step 1 — Restart & Enter BIOS

| Method | Key | When to Press |
|--------|-----|---------------|
| **BIOS Setup** | `F2` | Immediately when Dell logo appears |
| **Boot Menu** (recommended for Ubuntu install) | `F12` | Immediately when Dell logo appears |

> **Tip:** Tap the key repeatedly right after pressing the power button — don't hold it, just tap it every half-second until the menu appears.

---

## Step 2 — Prepare Ubuntu USB Drive (do this first, on another machine)

1. Download Ubuntu ISO from [ubuntu.com](https://ubuntu.com/download)
2. Flash it to a USB drive (8 GB+) using:
   - **Windows:** [Rufus](https://rufus.ie) — select ISO, scheme: **GPT**, target: **UEFI**
   - **Mac/Linux:** [balenaEtcher](https://etcher.balena.io)

---

## Step 3 — BIOS Settings to Check (press F2)

Go into BIOS and verify these settings:

| Setting | Required Value |
|---------|----------------|
| **Secure Boot** | **Disabled** (or set to "Other OS") |
| **SATA Mode** | **AHCI** (not RAID) |
| **Boot Mode** | **UEFI** |

Save and exit with `F10`.

---

## Step 4 — Boot from USB (press F12)

1. Press **F12** at startup → **One Time Boot Menu** appears
2. Select your USB drive under **UEFI Boot** section
3. Ubuntu installer will launch
4. Follow the on-screen steps to install

---

## Quick Summary

```
Power on → tap F12 → select USB → install Ubuntu
             (or F2 to change BIOS settings first)
```

---

**References:**
- [Dell BIOS Setup Guide](https://www.dell.com/support/kbdoc/en-us/000126121/how-to-enter-system-bios-setup-on-a-dell-laptop-desktop-or-workstation)
- [Ubuntu Installation Tutorial](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- [Rufus – Bootable USB Creator](https://rufus.ie)
