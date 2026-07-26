---
audio: false
generated: true
image: false
lang: en
layout: post
title: Create Windows 11 USB on Ubuntu
translated: false
type: note
---

Question: **In Linux/Ubuntu, how to create a Windows 11 installable bootable USB disk from an ISO?**

Answer:

On Ubuntu, the most reliable method for Windows 11 is **Ventoy**. Unlike `dd`, it handles Windows ISO files correctly (Windows ISOs often have files >4GB and special UEFI requirements).

## Method 1 (recommended): Ventoy

### 1. Download Ventoy

```bash
wget https://github.com/ventoy/Ventoy/releases/latest/download/ventoy-1.0.xx-linux.tar.gz
```

Extract:

```bash
tar xzf ventoy-*.tar.gz
cd ventoy-*
```

### 2. Find your USB device

Plug USB in:

```bash
lsblk
```

Example:

```
sda      500G  SSD
sdb       32G  USB
```

Assume USB is `/dev/sdb`.

⚠️ This erases the USB.

### 3. Install Ventoy

```bash
sudo ./Ventoy2Disk.sh -i /dev/sdb
```

Confirm.

### 4. Copy Windows 11 ISO

After Ventoy finishes, the USB appears as a normal disk.

Just copy:

```bash
cp Win11_25H2_English_x64_v2.iso /media/$USER/Ventoy/
```

Safely eject:

```bash
sync
```

Boot from USB → Ventoy menu → select ISO → Windows installer starts.

---

## Method 2: WoeUSB-ng (Windows-specific USB writer)

Install:

```bash
sudo apt update
sudo apt install woeusb-ng
```

Create USB:

```bash
sudo woeusb \
  --device \
  Win11_25H2_English_x64_v2.iso \
  /dev/sdb
```

---

## Method 3: Manual FAT32 + split install.wim

Useful if BIOS is picky (some Lenovo Xiaoxin machines).

### Partition USB

```bash
sudo parted /dev/sdb --script mklabel gpt
sudo parted /dev/sdb --script mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sdb1
```

Mount ISO:

```bash
sudo mount -o loop Win11.iso /mnt/iso
```

Mount USB:

```bash
sudo mount /dev/sdb1 /mnt/usb
```

Copy everything except `install.wim`:

```bash
rsync -av --exclude=sources/install.wim /mnt/iso/ /mnt/usb/
```

Install wimlib:

```bash
sudo apt install wimtools
```

Split Windows image:

```bash
wimsplit \
 /mnt/iso/sources/install.wim \
 /mnt/usb/sources/install.swm \
 3800
```

Result:

```
sources/
 ├── boot.wim
 ├── install.swm
 ├── install2.swm
```

Windows Setup understands `.swm`.

---

## Avoid this

Do **not** do:

```bash
sudo dd if=Win11.iso of=/dev/sdb bs=4M
```

for Windows 11.

`dd` works great for Linux ISOs, but Windows ISOs frequently fail because:

* FAT32 cannot store `install.wim` >4GB
* UEFI boot layout differs
* some firmware does not accept the hybrid ISO layout

---

For your Lenovo Xiaoxin case, I would use:

1. **Ventoy first** (fastest)
2. If Lenovo BIOS refuses → **manual FAT32 + wimlib split**
3. If Windows installer sees no SSD → check Intel VMD/RST driver issue

References:

* Ventoy project: [https://www.ventoy.net/](https://www.ventoy.net/)
* WoeUSB-ng: [https://github.com/WoeUSB/WoeUSB-ng](https://github.com/WoeUSB/WoeUSB-ng)
* wimlib: [https://wimlib.net/](https://wimlib.net/)
