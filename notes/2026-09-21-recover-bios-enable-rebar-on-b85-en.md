---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recover BIOS, Enable ReBAR on B85
translated: false
type: note
---

Here's what I found and what I'd do for your specific board.

## What the SOYO official site says

The current official site is **`soyocn.net`** (the old `soyo.com.cn` is dead — returns 502). Its download section is:

- 驱动/BIOS下载: `https://www.soyocn.net/down/zbdrv/INTEL/` (only 2 pages, ~39 boards, oldest entries are 2014 H81 models)
- B85 category: `https://www.soyocn.net/list.php?catid=469` → **only 1 product remains: SY-B85-BTC**

So **SY-B85N 全固版 is no longer listed on the current official site** — it was a ~2013/2014 budget board and SOYO dropped it. That's typical for these boards.

## How to actually get the BIOS image

### Option 1 (recommended): dump it from the flash chip

Since this is an old budget board with no official download, the most reliable way is to read the BIOS straight off the SPI flash chip:

1. Buy a **CH341A** programmer (~$5) + SOP8 test clip (so you don't need to desolder)
2. Identify the flash chip on the board (usually a 25-series SPI NOR, e.g. Winbond W25Q64/GD25Q64, SOP8 package)
3. Dump with `flashrom`:

   ```bash
   # Linux
   flashrom -p ch341a_spi -r soyo_b85n_backup.bin
   # read it 2-3 times and verify checksums match
   ```

This gives you both a **working backup (critical for recovery)** and the exact image to mod. I'd do this *before* any BIOS modding even if an official image existed.

### Option 2: Wayback Machine / archives

Try snapshots of the old SOYO sites and third-party mirrors:

- `https://web.archive.org/web/*/soyo.com.cn/*`
- `https://web.archive.org/web/*/soyocn.net/*`
- Search terms: `梅捷 SY-B85N BIOS`, `SY-B85N 全固版 驱动`

### Option 3: third-party Chinese driver sites / forums

- `drivers.mydrivers.com` (Soyo category: `s-4-878`)
- `drv5.cn`, `160.com`, `pcpop.com`
- Baidu Tieba (图拉丁吧 / 主板吧) — people archive these BIOS files

⚠️ If you find a "BIOS" from a random download site, verify the file is a real flash image (correct size, e.g. 8MB, and starts with a recognizable UEFI/Aptio header) before flashing.

## Important ReBarUEFI notes for this exact board

`SY-B85N` = **Intel B85 chipset = 8 Series (Haswell/Broadwell, LGA1150)**. Per the ReBarUEFI wiki this means:

1. **`HswAbove4G.txt` patch is REQUIRED** — on Intel 8/9 series, 4G decoding / resizable BAR won't function correctly without it. Append it to `patches.txt` before running UEFIPatch.
2. It's a Haswell board, so the relevant `patches.txt` entries are:
   - PciBus: `<16GB BAR size limit` removal
   - PciBus: `Don't downgrade 64-bit BARs to 32-bit` (Haswell/Broadwell)
   - PciHostBridge / MMIO space increase (Haswell/Broadwell variant)
3. This board almost certainly uses an **AMI Aptio** BIOS, so you may also need the NVRAM whitelist unlock patches if `ReBarState` later fails with `GetLastError: 5`.
4. Expect to use **MMTool 4.50.0.23** (pre-Skylake boards) if UEFITool's insert-after causes the pad-file corruption bug (common on these boards).

## Suggested order of operations

1. Dump the chip with CH341A + flashrom → save `soyo_b85n_backup.bin` (do this first!)
2. Insert `ReBarDxe.ffs` into the dumped image (UEFITool 0.28)
3. Apply UEFIPatch with `patches.txt` + `HswAbove4G.txt` appended
4. Check for pad-file corruption; if present, use MMTool 4.50 workaround
5. Flash back with CH341A + flashrom (or the board's own flasher)
6. In BIOS: enable 4G decoding (may be hidden → apply hidden 4G decode per wiki), disable CSM
7. Boot Linux/Windows, run `ReBarState`, set `32`, reboot

Want me to fetch the `HswAbove4G.txt` content and the full `patches.txt` (with the Haswell/8-series lines I already have) so you have a ready-to-use `patches.txt` for this board? I can also help you walk through the flashrom dump/flash commands if you tell me which flash chip is on the board.
