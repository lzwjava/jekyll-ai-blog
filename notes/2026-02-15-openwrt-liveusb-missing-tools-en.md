---
audio: false
generated: true
image: false
lang: en
layout: post
title: Missing Tools in OpenWrt Live USB
translated: false
type: note
---

Question: Both commands (zcat and dd) not found when trying to install OpenWrt to internal disk from USB boot

Answer:

You're booted into the OpenWrt live system from USB (root login, no password), but basic commands like `lsblk`, `dd`, or `zcat` are reporting "command not found". This happens because the **combined .img** boot environment in recent OpenWrt versions (especially snapshots or some stable builds) is very minimal — it uses busybox with only essential applets, and many common utilities (including `dd`, `lsblk`, `zcat`, `gzip`, etc.) are **not included** by default to keep the image small.

### Quick checks first

Run these to confirm your situation:

```
which dd
which lsblk
which zcat
busybox
```

- If `which` says not found or empty → those commands aren't there.
- `busybox` should show a list of supported commands (usually includes things like `cat`, `echo`, `mount`, but **not** `dd` or `lsblk` in minimal initramfs).

### Correct & recommended way in 2026 (current official method)

The official OpenWrt x86 guide no longer recommends installing *from* the booted OpenWrt USB image itself for most users, because of exactly this minimal-tool issue. Instead:

**Best & easiest method: Use a normal Linux live USB (e.g. your existing Linux Mint Cinnamon USB or Ubuntu/Fedora live) to write the image**

1. **Reboot** the laptop and remove the OpenWrt USB for now.
2. Boot from your **Linux Mint live USB** (or download a fresh Ubuntu live ISO and make one with Rufus/Etcher/dd).
3. Once in the live desktop (try without installing):
   - Open terminal.
   - Download the OpenWrt image again if needed (or copy it to USB beforehand):

     ```
     wget https://downloads.openwrt.org/releases/24.10.5/targets/x86/64/openwrt-24.10.5-x86-64-generic-ext4-combined-efi.img.gz
     gunzip openwrt-24.10.5-x86-64-generic-ext4-combined-efi.img.gz
     ```

     (or use the ImmortalWrt equivalent if preferred)
4. Identify your **internal** 500GB disk (careful — wrong choice wipes data!):

   ```
   lsblk -o NAME,SIZE,TYPE,MODEL
   sudo fdisk -l
   ```

   - Internal disk is usually `/dev/sda` (or `/dev/nvme0n1` if NVMe SSD).
   - USB live stick is smaller, e.g. `/dev/sdb`.
5. Write the image (this wipes & installs OpenWrt):

   ```
   sudo dd if=openwrt-....img of=/dev/sda bs=4M status=progress conv=fsync
   ```

   - Replace `/dev/sda` with your internal disk.
   - Wait for it to finish (may take 5–20 minutes).
6.

   ```
   sync
   ```

7. Shut down, remove the live USB, reboot → laptop should now boot directly into OpenWrt (console login: root, no password initially).

After first boot:

- Set password: `passwd`
- Connect to network (Ethernet to modem as WAN usually works by default)
- Access LuCI: <http://192.168.1.1> → set password again if prompted
- Run `opkg update && opkg install luci` if web GUI not there yet

### If you insist on using the OpenWrt USB live (advanced, not recommended)

You need to install the missing tools first — but the live system has **no opkg** / package manager by default, and usually no internet (unless you manually configure Ethernet/Wi-Fi via `ifconfig`/`wpa_supplicant` — complicated).

Some older forum posts suggest:

- If `/bin/dd` exists somehow → use it.
- Or fetch image via `wget` (if network works) then pipe to `cat > /dev/sda` — but unreliable and dangerous.

Most people abandon this and switch to a full Linux live USB — it's faster and has all tools (`dd`, `lsblk`, `wget`, `gunzip`, etc.).

### Summary – what to do right now

- Reboot → boot your Linux Mint live USB instead.
- Use `dd` from there to write the .img to `/dev/sda` (internal disk).
- This is the standard, reliable way used by almost everyone installing OpenWrt on x86 hardware (laptops, mini-PCs, etc.) in recent years.

Backup any data first (though you mentioned it can run Linux Mint, so presumably nothing critical left). If you tell me exactly what `ls` or `busybox` shows, or the full error, I can refine further.

References:

- [https://openwrt.org/docs/guide-user/installation/openwrt_x86](https://openwrt.org/docs/guide-user/installation/openwrt_x86)
- [https://forum.openwrt.org/t/openwrt-x86-on-usb-stick/142430](https://forum.openwrt.org/t/openwrt-x86-on-usb-stick/142430)
- [https://teklager.se/en/knowledge-base/openwrt-installation-instructions](https://teklager.se/en/knowledge-base/openwrt-installation-instructions)
