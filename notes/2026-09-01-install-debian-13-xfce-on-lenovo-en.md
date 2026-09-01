---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install Debian 13 XFCE on Lenovo
translated: false
type: note
---

Question: How do you install Debian 13 XFCE from `debian-live-13.6.0-amd64-xfce.iso` on the old Lenovo L-IG41M3 machine?

Answer: **Yes. That ISO is a good choice for this machine**, assuming the Celeron is 64-bit. Debian's Live Xfce image is specifically designed to boot from USB, let you test the hardware, and then install Debian to the hard disk using Calamares. ([Debian][1])

### 1. Create a bootable USB

Since you're probably preparing the USB from your Mac, plug in an **8 GB+ USB stick**.

On macOS:

```bash
diskutil list
```

Find the USB, for example:

```text
/dev/disk4
```

Unmount it:

```bash
diskutil unmountDisk /dev/disk4
```

Then write the ISO:

```bash
sudo dd if=debian-live-13.6.0-amd64-xfce.iso \
  of=/dev/rdisk4 \
  bs=4m \
  status=progress
```

Then:

```bash
diskutil eject /dev/disk4
```

**Be extremely careful with `/dev/disk4`.** `dd` destroys the target disk. Debian explicitly recommends writing the hybrid image to the **whole USB device**, not a partition such as `/dev/disk4s1`. ([Debian][2])

You can also use a GUI USB-writing utility if you prefer, but `dd` is the cleanest way to understand what is happening.

---

### 2. Put the USB into the Lenovo

Connect:

```text
USB stick
   ↓
L-IG41M3 USB port
```

Turn on the computer.

Immediately start pressing the BIOS/boot-menu key repeatedly.

On Lenovo machines this is commonly:

```text
F12
```

or sometimes:

```text
F2
Delete
```

You want to get into the **Boot Menu**.

Select something like:

```text
USB HDD
USB Storage
UEFI: <USB name>
```

For this very old G41 machine, **legacy BIOS boot is quite likely**, so don't worry if you don't see a UEFI entry.

---

### 3. Debian Live should boot

You'll get a Debian menu roughly like:

```text
Debian GNU/Linux Live

Debian GNU/Linux Live
Debian GNU/Linux Live (failsafe)
...
```

Choose:

```text
Debian GNU/Linux Live
```

It should boot XFCE entirely from the USB without touching the hard disk. That's one of the main purposes of the Live image. ([Debian][1])

You'll eventually get an XFCE desktop.

**This is great for your hardware-repair experiments** because you can test the machine before installing anything.

Open a terminal:

```bash
lscpu
free -h
lsblk
lspci
```

For the GPU slot:

```bash
lspci -vv
```

---

### 4. Check that the Celeron is actually 64-bit

This is important because you downloaded:

```text
amd64
```

`amd64` does **not** mean you need an AMD CPU. It means **64-bit x86**, and Intel 64-bit CPUs work with it too. Debian describes amd64 as the architecture for 64-bit PC-compatible systems. ([Debian][3])

Run:

```bash
lscpu | grep -E 'Architecture|Model name|CPU MHz'
```

You want:

```text
Architecture: x86_64
```

If you see:

```text
Architecture: i686
```

then the CPU is 32-bit and this particular ISO won't work.

---

### 5. Install it to the hard disk

Once you're inside Debian XFCE, look for:

```text
Install Debian
```

or the **Calamares installer**.

Debian's Live images include Calamares specifically for installing the Live system to the hard drive. ([Debian][1])

The basic flow is:

```text
Debian Live USB
       │
       ▼
   XFCE desktop
       │
       ▼
 Install Debian
       │
       ▼
 Select disk
       │
       ▼
 Partition disk
       │
       ▼
 Install bootloader
       │
       ▼
 Reboot
       │
       ▼
 Remove USB
       │
       ▼
 Debian XFCE on HDD/SSD
```

If the machine has an old HDD, I would **strongly recommend putting a cheap SATA SSD in it** instead.

Even something like:

```text
G41 + Celeron + 4 GB
        +
     SATA SSD
```

will feel dramatically better than:

```text
G41 + Celeron + 4 GB
        +
    7200 RPM HDD
```

### One thing I'd do first

**Don't install immediately.**

Boot the Live USB and run:

```bash
lscpu
free -h
lsblk
lspci
lspci -nn
```

Then send me the output.

Especially:

```bash
lscpu
lspci -nn
```

I can tell you exactly what CPU, chipset, PCIe controller, GPU slot, network controller, etc. that particular **L-IG41M3** has, and whether Debian 13 is going to be happy on it.

[1]: https://www.debian.org/CD//live/?utm_source=chatgpt.com "Debian -- Live install images"
[2]: https://www.debian.org/releases/bookworm/amd64/install.en.pdf?utm_source=chatgpt.com "Debian GNU/Linux Installation Guide"
[3]: https://www.debian.org/CD/?utm_source=chatgpt.com "Debian installation media for USB, CD, DVD"
