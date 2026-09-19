---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Diagnosis: Slow Machine, Three Fixes"
translated: false
type: note
---

I have a complete picture now. Here's the diagnosis.

## Hardware on 192.168.1.53 (`lzw-MS-7996`)

| Component | Spec | Verdict |
| --- | --- | --- |
| CPU | Intel Core i5-4460, 4 cores / 4 threads @ 3.2 GHz (Haswell, 2014) | Adequate, not the bottleneck |
| RAM | **3.2 GiB total** (`MemTotal: 3399592 kB`) | **Very low** |
| Swap | 3.7 GiB file, **578 MB already used 5 min after boot** | Thrashing |
| Disk | **WDC WD10EZEX — 1 TB 7200 RPM spinning HDD** (`rotational=1`) | **Primary bottleneck** |
| GPU | Intel iGPU + NVIDIA Tesla P100 16GB | Driver broken |
| OS | Ubuntu, kernel 7.0.0-31, GNOME/snap stack | Heavy for this box |

## Why it's slow — three compounding problems

**1. The NVIDIA P100 is in an endless driver-failure loop (biggest CPU culprit)**

```
journalctl -b | grep -c "probe with driver nvidia failed"        → 412
journalctl -b | grep -c "Failed to start nvidia-persistenced"    → 128
NVRM: BAR1 is 0M @ 0x0 (PCI:0000:01:00.0)
```

That's **128 failed service starts and 412 failed driver probes in ~6 minutes of uptime** — roughly one every 2–3 seconds. The P100 is a datacenter card that needs *Above 4G Decoding* enabled in BIOS; the MSI board isn't mapping its BAR1, so `nvidia` probe fails, udev retries, `nvidia-persistenced` restarts forever. This is why you saw `modprobe` pegged at 90% CPU, `%sy` at 18–28%, and `nvidia-persis` stuck in **D state**.

**2. Spinning HDD saturating on random I/O**

- `iowait` 22–38%, `%util` **61–99%**, `r_await` up to **99 ms**
- Requests are small/random (`rareq-sz` 6–65 KB) — the worst case for a 7200 RPM disk
- Live per-process I/O showed a `snap` process reading **~4 MB/s random** off `/dev/sda`
- Load average 3.4–4.05 on 4 cores with **71% wa** = the machine is *I/O-bound*, not CPU-bound

**3. Only 3.2 GiB RAM + 21 snap loop mounts, with no zram**

- `Committed_AS: 4.7 GB` against 3.4 GB physical → already swapping `so: 6696` at boot
- Top swap consumers: `gnome-shell` 69 MB, `ptyxis` 28 MB, `Xwayland` 24 MB
- **21 loop devices** = every snap (firefox, gnome-46-2404, mesa, snapd…) is a squashfs image read from the HDD. Snap refresh/seed is what's chewing the disk.
- GNOME desktop + snap Firefox on 3.2 GB / HDD is simply underspecced.

## Fixes, in impact order

```bash
# 1. Stop the NVIDIA retry storm (immediate, biggest win)
sudo systemctl disable --now nvidia-persistenced.service nvidia-persistenced.service
echo -e "blacklist nvidia\nblacklist nvidia_drm\nblacklist nvidia_modeset" | sudo tee /etc/modprobe.d/blacklist-nvidia.conf
sudo update-initramfs -u && sudo reboot
# Or properly fix it: enable "Above 4G Decoding" + "Resizable BAR" in BIOS for the P100

# 2. Add swap-friendly compression (helps 3.2 GB a lot)
sudo apt install zram-tools && echo -e "ALGO=zstd\nPERCENT=50" | sudo tee /etc/default/zramswap && sudo systemctl restart zramswap

# 3. Replace snaps with debs where possible + reduce disk pressure
sudo snap remove --purge snap-store firefox   # then apt install firefox-esr / flatpak on SSD
# Add an SSD for / (HDD only for bulk data) — the single biggest hardware upgrade

# 4. Confirm the disk is healthy (SMART needs sudo)
sudo smartctl -H -A /dev/sda | grep -iE "health|Reallocated|Pending|CRC"
```

**Summary:** the CPU/RAM specs are modest but usable; the slowness comes from (1) a broken NVIDIA P100 driver loop burning CPU and blocking processes, (2) a 7200 RPM HDD pinned at 99% utilization by snap squashfs random reads, and (3) 3.2 GB RAM swapping. Fix #1 is free and immediate; an SSD is the real cure.

Want me to apply the NVIDIA blacklist and zram fixes on that host?
