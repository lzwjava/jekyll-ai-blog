---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OpenWrt on Lenovo Laptop Router Guide
translated: false
type: note
---

Question: How to install OpenWrt on an old Lenovo laptop (with i5 processor, 8GB RAM, 500GB disk) that can recently run Linux Mint Cinnamon, to turn it into a soft router? (Possibly including ImmortalWrt option)

Answer: 

Yes — your Lenovo laptop (i5 + 8GB RAM + 500GB disk) is **perfectly suitable** for running OpenWrt as a high-performance soft router. It will outperform almost any consumer router, especially for VPN/proxy (Clash/OpenClash), SQM QoS, multi-gigabit routing, many packages, etc.

**Two main choices in 2026:**
- **Official OpenWrt** → More stable, upstream, very reliable (recommended for most people)
- **ImmortalWrt** → Fork popular in China, includes more proxy-related packages by default, some extra optimizations, but slightly less "vanilla"

For a beginner, start with **official OpenWrt 24.10.x** (stable) or latest snapshot if you want newest features.

### Step-by-step installation guide (most common & recommended method)

#### 1. Download the correct image
- Go to: https://downloads.openwrt.org/
- For stable → releases → 24.10.5 (or newest 24.10.x) → targets → x86 → 64
- Recommended file: **openwrt-x86-64-generic-ext4-combined-efi.img.gz**  
  (This is the EFI version — almost all laptops from ~2010+ use UEFI. Your recent Linux Mint install proves UEFI works.)

If your BIOS is legacy/CSM only (very rare on i5 laptops), use the non-efi version instead.

For ImmortalWrt (if you prefer Chinese-optimized builds with more proxy plugins pre-included):
- Go to: https://immortalwrt.org/ or their downloads page
- Choose x86_64 target → similar ext4-combined-efi image

#### 2. Prepare a USB flash drive (≥4GB, 8GB+ better)
You will write the image directly to USB — this becomes a "live/install" medium.

Tools (choose one):
- **Windows**: Use Rufus (https://rufus.ie/) — select DD Image mode
- **Linux** (you already have Linux Mint): Use balenaEtcher, GNOME Disks, or command line `dd`
- **Any OS**: Ventoy (multi-boot USB) also works if you just copy the .img file

Command line example in Linux Mint:
```bash
# First unzip if needed
gunzip openwrt-....img.gz

# Find your USB device (careful!!)
lsblk   # e.g. /dev/sdb  (NEVER /dev/sda which is your laptop disk!)

# Write image (replace sdb with your USB)
sudo dd if=openwrt-x86-64-generic-ext4-combined-efi.img of=/dev/sdb bs=4M status=progress conv=fsync
```

#### 3. Boot from the USB on your Lenovo laptop
- Insert USB
- Restart laptop
- Enter BIOS/BOOT menu (usually F2, F12, Fn+F2, Del, or Novo button on some Lenovos)
- Set USB as first boot device (or choose one-time boot menu)
- Disable Secure Boot if it blocks (most OpenWrt images are not signed — common on x86)
- Save & exit → should boot into OpenWrt console (black screen with white text)

#### 4. Install to internal 500GB disk
Once booted from USB (you see OpenWrt login prompt — login as root, no password):

Identify your internal disk:
```bash
lsblk   # usually /dev/sda  (500GB size)
# or use fdisk -l
```

Write (install) OpenWrt to internal disk — this **wipes everything** on the 500GB drive!
```bash
# Option A: Simple one-liner (most common)
zcat /dev/sr0/openwrt-*.img.gz | dd of=/dev/sda bs=4M status=progress   # if image still gzipped on USB

# Option B: If already unzipped on USB
dd if=/path/to/openwrt-....img of=/dev/sda bs=4M status=progress conv=fsync
```

After dd finishes:
```bash
sync
reboot
```

Remove USB before reboot.

#### 5. First boot & basic setup
- Laptop boots from internal disk into OpenWrt
- Connect Ethernet cable from laptop's LAN port to your main router/modem (this becomes WAN)
- Connect your PC/phone to **another** Ethernet port if available, or use Wi-Fi (if your laptop Wi-Fi card is supported)
- From another device, go to: http://192.168.1.1
- Set root password immediately (required for LuCI/web GUI)
- Install LuCI if missing (OpenWrt x86 images usually include it, but confirm):
  ```bash
  opkg update
  opkg install luci
  ```
- Now access full web interface at http://192.168.1.1

#### 6. Configure as router
- Network → Interfaces
  - WAN: set to DHCP client (or PPPoE if your ISP needs it)
  - LAN: keep 192.168.1.1/24
- Firewall: default is fine for start
- For Wi-Fi: install wireless driver if needed (most Intel Wi-Fi cards work with iwlwifi)
  ```bash
  opkg update
  opkg install kmod-iwlwifi luci-app-statistics  # example
  ```
- Then install your favorite packages (OpenClash, PassWall, AdGuard Home, SQM, etc.)

### Tips & Warnings
- Backup important data — installation wipes the 500GB disk!
- Use Ethernet for initial setup (more reliable than Wi-Fi)
- Laptop Wi-Fi usually becomes your 2.4/5GHz AP — very powerful coverage
- Power consumption higher than real router (~15-40W vs 5-12W), but ok for 24/7 if not concerned
- For better I/O, add multi-port Ethernet card via mini-PCIe or USB if needed
- ImmortalWrt install process is almost identical — just different download link

Your i5 + 8GB setup can easily handle gigabit+ speeds, heavy VPN/proxy for whole house, and many services.

References:  

- [OpenWrt Wiki - OpenWrt on x86 hardware (PC / VM / server)](https://openwrt.org/docs/guide-user/installation/openwrt_x86)
- [OpenWrt Downloads page](https://downloads.openwrt.org/)
- [Example guide using dd on x86](https://gist.github.com/pjobson/3584f36dadc8c349fac9abf1db22b5dc)
- [ImmortalWrt official site (for alternative builds)](https://immortalwrt.org/)