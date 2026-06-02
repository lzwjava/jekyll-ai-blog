---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix GRUB Boot From USB First
translated: false
type: note
---

Question: How to proceed when entering GRUB mode during OpenWrt installation from a bootable USB on a Lenovo laptop?

Answer:

You're currently seeing a GRUB prompt (likely `grub>` or `grub rescue>`) instead of booting directly into the OpenWrt console. This is a common issue when trying to boot the OpenWrt x86 combined image from USB, especially on Lenovo laptops or UEFI systems.

Here are the most likely causes and fixes (in order of probability and ease):

### Most common reason: The laptop is not actually booting from the USB stick

- Your internal disk still has an old GRUB bootloader (from Linux Mint or previous OS), and the BIOS/UEFI is trying to boot from the internal drive first → falls back to its (now broken/missing) GRUB.
- **Fix** (do this first):
  1. Restart the laptop with the USB still plugged in.
  2. Immediately enter the **boot menu** (usually **F12** on Lenovo, sometimes **F10**, **Fn+F12**, or **Novo button** — small pinhole/button next to power on some models).
  3. In the one-time boot menu, explicitly select the **USB device** (it may show as "USB HDD", "UEFI: SanDisk", "Kingston", etc. — choose the UEFI version if both appear).
  4. If it still fails → go into full **BIOS setup** (usually **F2** or **Fn+F2** at startup):
     - Set **Boot Mode** → UEFI (not Legacy/CSM unless you specifically used the non-efi image).
     - Disable **Secure Boot** completely (set to Disabled).
     - In Boot Priority / Boot Order → move USB/Removable Device to the very top.
     - Disable **Fast Boot** / **Quick Boot** if present.
     - Save (F10) → Exit → reboot.
- After this change, it should boot directly into the OpenWrt GRUB menu (shows "OpenWrt" entry) → then kernel messages → login prompt (root, no password).

### If it really boots from USB but still drops to GRUB prompt / rescue

- Rare with official combined-efi.img, but can happen with write errors, bad USB stick, or image corruption.
- **Quick checks**:
  - Re-create the USB stick (very important):
    - Use **Rufus** in Windows → DD Image mode (not ISO mode).
    - Or in Linux Mint: `gunzip` the .gz file first → then `sudo dd if=image.img of=/dev/sdX bs=4M status=progress conv=fsync`
    - Try a different (high-quality) USB stick if possible.
- At the `grub>` prompt you can try manual boot (only if you're comfortable; usually not needed):

  ```
  ls               # lists devices like (hd0,gpt1) (hd0) (hd1) etc.
  ```

  Find the USB partition with OpenWrt files (usually has /boot/grub or vmlinuz).
  Example (adjust based on your ls output):

  ```
  set root=(hd1,gpt2)          # or (hd0,msdos1) etc. — try the one with ext4
  linux /boot/vmlinuz root=PARTUUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  initrd /boot/initrd (if present — combined images usually don't need it)
  boot
  ```

  But honestly — 95% of the time this isn't necessary. Fixing the boot order is enough.

### Summary – what to do right now

1. Remove USB → reboot → enter boot menu (F12) → select USB explicitly.
2. If no change → enter BIOS (F2) → disable Secure Boot + set USB first + UEFI mode.
3. If still GRUB prompt after confirmed USB boot → remake the USB stick carefully (verify checksum of downloaded .img.gz if possible).
4. Once it boots correctly → you should see OpenWrt GRUB menu (hit Enter if it pauses) → then console login: `root` (no password).

After successful boot from USB → proceed with the `dd` install to `/dev/sda` (internal disk) as described earlier.

Let me know exactly what the GRUB screen shows (grub> or grub rescue> or just "GRUB _") and whether you see any error messages — that helps narrow it down further.

References:

- <https://forum.openwrt.org/t/openwrt-x86-on-usb-stick/142430>
- <https://openwrt.org/docs/guide-user/installation/openwrt_x86>
- <https://www.reddit.com/r/openwrt/comments/1r3wruz/trouble_booting_openwrt_x86_on_anything_other>
