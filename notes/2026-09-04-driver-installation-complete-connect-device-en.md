---
audio: false
generated: true
image: false
lang: en
layout: post
title: Driver Installation Complete, Connect Device
translated: false
type: note
---

Installation is complete for the driver package. Here's a summary of what was done:

## What the manual says (usb-vendor-class-driver_im_en.pdf, Rev 1.2)

For Windows 10, the procedure is: run `pnputil -a <path>\SMJUSBCOM.INF` from an elevated prompt → connect the Star printer/card reader via USB → Windows binds the driver via Plug & Play → verify **"SMJ USB Device (COM*)"** appears under **Ports (COM & LPT)** in Device Manager.

## Actions performed

1. **Verified environment** — Windows 11 Pro 64-bit (build 26100), shell running elevated.
2. **Verified driver signature** — `smjusbcom.cat` is validly signed by **Microsoft Windows Hardware Compatibility Publisher** (WHQL, cross-certified chain), so it's acceptable for x64 kernel loading. The `.sys` files are catalog-signed (no embedded signature), which is normal for PnP drivers.
3. **Installed the driver package into the driver store** (manual step 1):

   ```
   pnputil /add-driver SMJUSBCOM.INF /install
   → Driver package added successfully.
   Published Name:  oem152.inf
   ```

   Confirmed in driver store: Provider **Star Micronics**, Class **Ports**, Version **02/19/2019 5.0.0.0**, Signer **Microsoft WHQL**.

## Remaining step — device connection (manual step 2)

**No Star USB device (VID_0519) is currently attached to this machine** (verified via `pnputil /scan-devices` and PnP enumeration). The driver is staged and will auto-install the moment a compatible device is plugged in.

To finish:

1. Connect the Star printer / Visual Card-Reader/Writer (TSP100/650/700II/800II, FVP10, HSP7000, SP500/700, TUP500/900, TCP300II/400) with a USB cable and power it on.
   - **HSP7000**: set DIP switch 1-5 to **ON**; other printers: **OFF**.
2. Wait for PnP to finish (a virtual COM port will be created).
3. Verify in **Device Manager → Ports (COM & LPT)** that **"SMJ USB Device (COM*)"** appears.

⚠️ One note: this driver officially targets Windows 7/8.1/10 (per the readme), but this machine runs **Windows 11 24H2**. The WHQL-signed package staged successfully, and it should load once the device is attached. If the device shows an error (e.g., code 52 / signed-driver block), let me know and I can check event logs to help troubleshoot.
