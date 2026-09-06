---
audio: false
generated: true
image: false
lang: en
layout: post
title: Camera Driver Fix Requires Reboot
translated: false
type: note
---

## Summary

**What was wrong:** Your "GL USB2.0 UVC Camera Device" (GenesysLogic chip, `VID_A16F&PID_0304`) had two competing driver bindings on this PC:

| Node | Driver | Result |
|------|--------|--------|
| `…\7&2f50fd3d&0&0000` | **`glavcam.sys`** (`oem153.inf`) | ❌ Problem 39 — driver failed to load |
| `…\6&349b1f0b&0&0000` | **Microsoft `usbvideo.sys`** (inbox) | ✅ works |

The vendor's `glavcam.sys` is an **unsigned, Vista-era "Longhorn DDK" driver**, and your system has **Memory Integrity (HVCI) enabled**. Code Integrity (Event 3111, status `0xC0000220`) refuses to load it, which surfaced as `0xC000026C` (STATUS_DRIVER_UNABLE_TO_LOAD) → "A driver cannot load on this device." Windows correctly blocks it — it should never have been used on Win10 24H2.

**What I did:**
1. `pnputil /delete-driver oem153.inf /uninstall /force` — removed the bad driver package from the DriverStore and uninstalled its device ✅
2. Deleted the leftover `glavcam` kernel service (`sc delete glavcam`) ✅
3. Removed the broken device node and rescanned ✅

**Current state:** No devices have problems anymore, `glavcam` is fully gone, and Memory Integrity stays ON (no security was weakened). The camera's USB composite is connected, but Windows reports **a reboot is needed** to complete re-enumeration of the webcam interface — after reboot it will automatically bind to the signed inbox **`usbvideo.sys`** (the "USB2.0 UVC PC Camera" driver that already worked on this same camera model).

**Next step:** Reboot the machine. Want me to trigger `shutdown /r /t 0` now, or will you reboot when convenient? After boot, verify with:
```
pnputil /enum-devices /deviceid "USB\VID_A16F&PID_0304"
```
— you should see a `Camera`-class "USB2.0 UVC PC Camera" node with `Driver Name: usbvideo.inf`, Status `Started`, and the webcam will appear in apps (Camera, Teams, etc.).