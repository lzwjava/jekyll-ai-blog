---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Lenovo BIOS and USB Boot Guide
translated: false
type: note
---

Question: In a Lenovo 2011 laptop, what is the typical command/key to enter BIOS, and how to choose a bootable USB disk with Linux Mint?

Answer:

For Lenovo laptops from around 2011, the keys depend on whether it's a **ThinkPad** series or an **IdeaPad** / consumer series model. Here are the most common options:

### 1. Entering BIOS Setup

- **Most common for ThinkPad models** (very typical for 2010–2012 business laptops like T410, T420, X220, L420, etc.):
  Power off the laptop completely.
  Press the power button → immediately and repeatedly tap **F1** (or sometimes Fn + F1).
  → This almost always enters the BIOS Setup Utility on 2011-era ThinkPads.

- **Most common for IdeaPad / consumer models** (G560, Z570, Y560, etc.):
  Power off → press power button → immediately and repeatedly tap **F2** (or Fn + F2).
  Some older IdeaPad models may show "Press F2 to Setup" briefly on screen.

- **Fallback / alternative methods** (try if the above fail):
  - Repeatedly tap **Enter** during power-on (some ThinkPads show "Startup Interrupt Menu" → then press F1 for BIOS).
  - Repeatedly tap **Esc** right after power-on (rare, but works on some models).

Tip: Watch the screen carefully during boot — many Lenovo laptops briefly display "Press [key] to enter Setup" (usually F1 or F2).

### 2. Booting from USB (Linux Mint)

There are two main ways:

**Way A — Use the one-time Boot Menu (recommended and easiest)**

- Insert your Linux Mint USB (properly created, e.g., with Rufus or dd).
- Power on the laptop and immediately start tapping one of these keys:
  - **F12** — most common boot menu key on Lenovo laptops (both ThinkPad and IdeaPad) around 2011
  - **F10** or **Fn + F10** — works on some models
  - **Esc** — occasional alternative
- When the **Boot Menu** appears, select the USB device (it may say "USB HDD", "UEFI: USB", "Kingston", etc.).
  Press Enter → it should start booting Linux Mint.

**Way B — Change boot order permanently in BIOS**

- Enter BIOS (F1 or F2 as above).
- Go to the **Startup** or **Boot** tab (use arrow keys).
- Find the boot priority / boot order list.
- Move the USB device (often listed as "USB HDD", "Removable Device", or the brand name) to the top using + / – keys or F5 / F6.
- If you see **UEFI/Legacy Boot** or **Boot Mode**, set it to **Legacy** (or "Both"/"CSM") — most 2011 Lenovo laptops work better with Legacy/CSM mode for Linux Mint USBs.
- Press **F10** → Yes to **Save and Exit**.

After saving, the laptop should boot from the USB automatically on the next restart.

**Quick summary for 2011 Lenovo laptop**

- BIOS → try **F1** first (ThinkPad style), then **F2**
- Boot from USB → tap **F12** at startup for the boot menu (fastest way)

References:

- <https://support.lenovo.com/us/en/solutions/ht500222-recommended-ways-to-enter-bios-boot-menu-thinkpad-thinkcentre-thinkstation>
- <https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad>
- <https://www.wikihow.com/Enter-the-BIOS-on-a-Lenovo-Laptop>
