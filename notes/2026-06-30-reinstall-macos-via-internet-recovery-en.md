---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reinstall macOS via Internet Recovery
translated: false
type: note
---

Question: How do I reinstall macOS on my own on a 2017 MacBook Pro that I recently wiped to install Fedora?

Answer:

Since you replaced macOS with Fedora, the recovery partition is gone. You need **Internet Recovery**, which pulls the installer from Apple's servers over the network.

## Method 1: Internet Recovery (simplest)

1. Shut down fully.
2. Power on and immediately hold **Cmd + Option (Alt) + R** until you see a spinning globe (not the Apple logo). This boots Internet Recovery and installs the **latest** macOS your Mac supports.
   - Use **Cmd + R** instead to get the version that *originally shipped* — but that won't work here since your recovery partition is wiped, so use the globe variant.
3. Connect to Wi-Fi (or Ethernet — more reliable for the multi-GB download).
4. In macOS Utilities, open **Disk Utility** first:
   - Select the internal disk (top-level, not the Fedora volume).
   - **Erase** → Format **APFS**, Scheme **GUID Partition Map**. This nukes the Fedora/ext4/LUKS layout.
5. Quit Disk Utility → **Reinstall macOS** → follow prompts.

A 2017 MacBook Pro (model `MacBookPro14,x`) supports up to **macOS Ventura 13** officially (Sonoma/Sequoia dropped it). Internet Recovery may offer Ventura or fall back to the factory version (Sierra 10.12), which you can then upgrade via the App Store.

## Method 2: Bootable USB installer (more control, faster reuse)

If you have access to *another working Mac*, this is the better path — but note you only have the one Mac, so Method 1 is your realistic route unless you borrow one.

On a working Mac, with a 16GB+ USB stick:

```bash
# Download installer from App Store (e.g. "Install macOS Ventura"), then:
sudo /Applications/Install\ macOS\ Ventura.app/Contents/Resources/createinstallmedia \
  --volume /Volumes/MyUSB
```

Then boot the target Mac holding **Option (Alt)** at startup, select the USB, erase the disk in Disk Utility (APFS/GUID), and install.

## Gotchas for your situation

- **Firmware password**: if you ever set one, you'll need it to boot recovery.
- **T2 chip**: the 2017 model has **no T2**, so no Secure Boot restrictions — booting external/recovery media is unrestricted. Good for you.
- **Internet Recovery needs specific Wi-Fi**: it only supports WPA/WPA2 personal networks, not captive portals or enterprise auth. If your network has a login page, use a phone hotspot or Ethernet adapter.
- **Disk wiped by Fedora**: Fedora likely converted the partition table or used LUKS — the full **Erase** in Disk Utility handles this cleanly.

Realistic plan for you: hold **Cmd+Option+R**, erase to APFS, reinstall. If Internet Recovery serves you an ancient version, upgrade to Ventura afterward via the App Store.