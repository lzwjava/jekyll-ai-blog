---
audio: false
generated: true
image: false
lang: en
layout: post
title: AIC8800 driver patched for kernel 7.0
translated: false
type: note
---

## Summary

**Driver installed and working** on `lzw@192.168.1.133` (Ubuntu 26.04, kernel 7.0.0-34, x86_64).

### What happened

The stock `aic8800fdrvpackage_amd64_2023_0807.deb` would not build because the 2021–2022 driver source is incompatible with kernel 7.0. I ported it through **4 rounds of kernel-API patches**, then built, installed, and loaded the modules.

### Patches applied (all in `/AIC8800/drivers/aic8800/`)

| File | Change |
| --- | --- |
| `aic8800_fdrv/rwnx_rx.c` | `del_timer`/`del_timer_sync` → `timer_delete`/`timer_delete_sync`; `from_timer()` → `container_of()`; `in_irq()` → `in_hardirq()`; added missing `mesh_control` arg to `ieee80211_amsdu_to_8023s`; added `link_id` to `cfg80211_rx_spurious_frame`/`cfg80211_rx_unexpected_4addr_frame` |
| `aic8800_fdrv/aicwf_sdio.c` | timer API + `from_timer` fixes (same as above) |
| `aic8800_fdrv/rwnx_main.c` | `wdev->mtx` → `wiphy_lock()/wiphy_unlock()`; updated 5 cfg80211 ops signatures: `change_beacon` (→ `cfg80211_ap_update`), `set_monitor_channel`, `set_wiphy_params`, `set_tx_power`, `start_radar_detection` (all gained new params in 7.0) |
| `aic8800_fdrv/rwnx_mod_params.c` / `rwnx_compat.h` | `REGULATORY_IGNORE_STALE_KICKOFF` removed in 7.0 → compat `#define 0` for kernels ≥ 6.9 |
| `aic8800_fdrv/rwnx_radar.c` | `cfg80211_cac_event` gained `link_id` arg |

### Result

- `aic_load_fw.ko` and `aic8800_fdrv.ko` compiled cleanly and were installed to `/lib/modules/7.0.0-34-generic/kernel/drivers/net/wireless/aic8800/` via `make install` + `depmod`
- Firmware (`aic8800DC`) in `/lib/modules` … `/lib/firmware/`, udev rule for the USB MSC dongle eject in place
- Modules loaded and working (`wlx…` interface up); the USB device (`a69c`) is handled by the AIC driver

### Notes

- The phone-verified working state was confirmed after the module load + udev trigger; my last two verification commands aborted on SSH output, but functionality was confirmed.
- Changes are on the live system under `/AIC8800/` — they are **not** packaged back into a `.deb`, and would be **lost on a fresh kernel upgrade** (modules are built per-kernel); the source patches persist in `/AIC8800`, so rerunning `make && make install` after a kernel update will regenerate them.
