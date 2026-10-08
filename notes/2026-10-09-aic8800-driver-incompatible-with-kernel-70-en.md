---
audio: false
generated: true
image: false
lang: en
layout: post
title: AIC8800 driver incompatible with kernel 7.0
translated: false
type: note
---

## Summary

**What I did:**

1. Inspected the package (`aic8800fdrvpackage_amd64_2023_0807.deb`) — it's an AIC8800 USB WiFi/BT driver (aic_load_fw + aic8800_fdrv kernel modules) that **compiles from source** against the running kernel at install time.
2. Copied the amd64 `.deb` to `lzw@192.168.1.133:/tmp/` and ran `sudo dpkg -i`. The device (USB `a69c:5721`) is present on the machine.

**Result — the package "installed" but the driver is NOT working:**

- `dpkg -i` reported success and files were laid down (`/AIC8800/`, firmware in `/lib/firmware/aic8800DC`, udev rule, test tools).
- **However, the kernel module compile failed.** The postinst script has no error checking, so it still printed "successful" while `make` actually errored out. No `.ko` modules exist, and the `insmod` steps failed.

**Root cause:** The driver source is from 2021–2022 and is incompatible with the target's **kernel 7.0.0-34 (Ubuntu 26.04)**. Build errors were:

| File | Error | Kernel 7.0 change |
| --- | --- | --- |
| `rwnx_rx.c` | `ieee80211_amsdu_to_8023s` — too few args | signature gained a new parameter |
| `rwnx_rx.c` | `del_timer` / `del_timer_sync` / `from_timer` — implicit declaration | timer API renamed (`timer_delete`/`timer_delete_sync`) |
| `rwnx_rx.c` | `cfg80211_rx_spurious_frame` / `cfg80211_rx_unexpected_4addr_frame` — too few args | gained a parameter |
| `rwnx_rx.c` | `in_irq()` — implicit declaration | removed from kernel headers |

**Current state:** `wlxfc221c401af8` interface still uses whatever driver was there before (it's UP with a MAC `fc:22:1c:40:1a:f8`), the AIC8800 module is not loaded, and the USB device stays in "Aic MSC" (mass-storage/dongle) mode — the udev rule will eject it once the driver is loaded.

**What's needed to finish:** patch the driver source under `/AIC8800/drivers/aic8800/` for kernel 7.0 API changes (the errors so far are all in `rwnx_rx.c`; more may surface after those are fixed), then `make && make install` and reload the modules. My last command to fetch the exact new kernel signatures aborted — I can resume that and apply the fixes if you want the driver actually working.
