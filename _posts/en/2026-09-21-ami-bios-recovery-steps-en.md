---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMI BIOS Recovery Steps
translated: false
type: note
---

I've prepared the recovery files. Here's the full recovery path:

## 1. Tell me the triage results first
(Fans? Beeps? Monitor on GPU vs motherboard? HDD activity?)

## 2. AMI forced recovery (most likely to work without hardware)

Many AMI boards have a **boot-block recovery**: if you power on while holding **Ctrl + Home**, it ignores the main BIOS and loads a recovery file from a USB.

1. Get a **FAT32 USB stick** (any small one, or bring the FreeDOS one back to this machine and I'll rewrite it).
2. Put the **original BIOS** on its root with these two names (I've already created both):
   - `AMIBOOT.ROM`
   - `B75V101.bin`
   (both = your untouched `B75V101_original.bin`, md5 `74f486f6…`)
3. Insert into the B75, **hold `Ctrl` + `Home`**, then press power. Keep holding for ~10 s.
4. Listen: **4 beeps** = it's reading the recovery file. Then it may beep/re-flash and reboot itself. Wait several minutes.

If you bring a USB back to this machine, I'll write the recovery USB for you in one command.

## 3. If recovery fails — hardware programmer (guaranteed fix)

The SPI flash chip on the B75 is a small 8-pin chip (likely Winbond `W25Q32`/`W25Q64`, 4 MB). You reflash it directly:

1. Buy a **CH341A programmer + SOIC8 test clip** (a few dollars, AliExpress/Amazon).
2. Clip onto the BIOS chip (board powered off), connect to **this MSI machine** via USB.
3. I'll install `flashrom` here and we write `B75V101_original.bin` back — board is then 100% restored to stock.

---

**Don't worry** — this is recoverable either way. The most likely culprit (which I'll fix for the next attempt) is that the rebuilt DSDT came out **104 bytes larger** than the original, and the AmiBoardInfo PE had to be expanded. I'll shrink the DSDT next time so it stays within the original size, and we'll flash again.

First: tell me the triage answers, and whether you can try the **Ctrl+Home** recovery with a USB.