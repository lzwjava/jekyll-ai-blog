---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install Ubuntu on MacBook Pro 2017
translated: false
type: note
---

Question: **How to install Ubuntu 24.04 / 26.04 on a MacBook Pro 2017?**

Answer:

MacBook Pro 2017 is an **Intel Mac**, so Ubuntu works. The easiest path is **clean install Ubuntu only** (remove macOS) or dual boot. Ubuntu 24.04 LTS is the safer choice; Ubuntu 26.04 is newer and may need more fixes. Ubuntu's installer supports booting from USB on Intel Macs by holding **Option (⌥)** during startup and selecting **EFI Boot**. ([Ubuntu Documentation][1])

## 1. Download Ubuntu ISO

Recommended:

* Ubuntu 24.04 LTS:

  * `ubuntu-24.04.x-desktop-amd64.iso`

Ubuntu 26.04 (if released for your target date):

* `ubuntu-26.04-desktop-amd64.iso`

Your MacBook Pro 2017 needs **amd64/x86_64**, not ARM.

---

## 2. Create bootable USB

From Ubuntu/Linux:

```bash
lsblk

# example USB = /dev/sdb
sudo dd if=ubuntu-24.04.x-desktop-amd64.iso \
  of=/dev/sdX \
  bs=4M \
  status=progress \
  oflag=sync
```

Or use Ventoy:

```bash
sudo ./Ventoy2Disk.sh -i /dev/sdX
```

Copy ISO to Ventoy USB.

---

## 3. Allow external boot (if blocked)

Restart Mac:

```
Command (⌘) + R
```

Enter Recovery.

Open:

```
Utilities
 → Startup Security Utility
 → Allow booting from external media
```

Some MacBook models with Apple security chips require this step. ([YouTube][2])

---

## 4. Boot Ubuntu USB

Insert USB.

Power on and hold:

```
Option (⌥)
```

You should see:

```
EFI Boot
```

Select it.

([Ubuntu][3])

---

## 5. Install Ubuntu

Choose:

```
Install Ubuntu
```

For full replacement:

```
Erase disk and install Ubuntu
```

For dual boot:

1. Open macOS Disk Utility first
2. Shrink APFS partition
3. Leave free space
4. Ubuntu installer:

   ```
   Something else
   ```

5. Create:

```
/boot/efi   512MB   FAT32

/           ext4    remaining
```

Ubuntu recommends "Erase disk and install Ubuntu" for a simple single-OS installation. ([Ubuntu Documentation][1])

---

## 6. After installation: MacBook Pro 2017 fixes

The 2017 MacBook Pro has some Apple-specific hardware:

### WiFi

Check:

```bash
lspci | grep -i network
```

Install Broadcom firmware:

```bash
sudo apt update
sudo apt install bcmwl-kernel-source
```

---

### Touch Bar

Check:

```bash
lsusb | grep Apple
```

Some users need additional kernel/support packages. Ubuntu 26.04 reports improved support on some 2017 models, but WiFi/audio/Touch Bar may still need manual fixes. ([Reddit][4])

---

### Audio

Check:

```bash
sudo dmesg | grep -i audio
```

---

### Trackpad

Usually works automatically with:

```bash
libinput
```

Test:

```bash
sudo libinput list-devices
```

---

## My recommendation for a 2017 MBP

Use:

```
Ubuntu 24.04 LTS
+
latest HWE kernel
```

because:

* stable
* long support
* better community fixes
* easier driver debugging

Then upgrade to 26.04 later.

References:

* Ubuntu Desktop installation guide ([Ubuntu Documentation][1])
* Ubuntu on MacBook Pro 2017-2019 wiki ([Ubuntu Wiki][5])
* Ubuntu try/install USB boot guide ([Ubuntu][3])

[1]: https://documentation.ubuntu.com/desktop/en/24.04/tutorial/install-ubuntu-desktop/?utm_source=chatgpt.com "Install Ubuntu Desktop - Ubuntu Desktop documentation"
[2]: https://www.youtube.com/watch?v=qjfBP4UYx9c&utm_source=chatgpt.com "How To Dual Boot Ubuntu 24.04 & MacOS On MAC || Install NEW Ubuntu On MAC (INTEL ONLY) - YouTube"
[3]: https://ubuntu.com/desktop/docs/en/latest/tutorial/try-ubuntu-desktop/?utm_source=chatgpt.com "Try Ubuntu Desktop - Ubuntu Desktop documentation"
[4]: https://www.reddit.com/r/linux_on_mac/comments/1v02681/macbook_pro_2017_macbookpro142_on_ubuntu_2604/?utm_source=chatgpt.com "MacBook Pro 2017 (MacBookPro14,2) on Ubuntu 26.04 — Wi-Fi, Touch Bar, and Audio Working"
[5]: https://wiki.ubuntu.com/Apple/MacBook%20Pro%2015%22%202017-2019?utm_source=chatgpt.com "Apple/MacBook Pro 15\" 2017-2019 - Ubuntu Wiki"
