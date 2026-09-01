---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choose Lenovo Debian XFCE Live
translated: false
type: note
---

Question: Which Debian 13.6 AMD64 download should you choose for the Lenovo L-IG41M3?

Answer: **Choose `iso-cd/` if you want the normal installer.** But if you specifically want the **XFCE Live desktop** you mentioned earlier, you're looking for a **Live ISO**, which is not in the `iso-cd/` directory.

For your machine, I'd use:

```text
debian-live-13.6.0-amd64-xfce.iso
```

That is the right choice because:

* `amd64` → works with 64-bit Intel CPUs too
* `xfce` → lightweight desktop, appropriate for 4 GB RAM
* `live` → boot from USB first, test hardware, then install
* ISO hybrid → directly write it to the USB with `dd`

The directory you pasted is the **standard Debian CD/DVD installation media**, so:

```text
iso-cd/       ← small network installer CDs
iso-dvd/      ← full DVD images
iso-bd/       ← Blu-ray
bt-*          ← BitTorrent
jigdo-*       ← jigdo download mechanism
list-*        ← package/file lists
log/          ← build logs
```

If you specifically want the XFCE Live image, use Debian's Live directory:

[Debian 13.6.0 AMD64 Live images](https://cdimage.debian.org/debian-cd/13.6.0-live/amd64/iso-hybrid/?utm_source=chatgpt.com)

Then download:

```text
debian-live-13.6.0-amd64-xfce.iso
```

### For your L-IG41M3

I'd choose this exact path:

```text
Mac
 │
 ├── download debian-live-13.6.0-amd64-xfce.iso
 │
 ▼
USB 8GB+
 │
 ▼
L-IG41M3
 │
 ▼
Boot from USB
 │
 ▼
Debian XFCE Live
 │
 ├── test CPU/RAM
 ├── test SATA
 ├── test Ethernet
 ├── test PCIe GPU
 │
 ▼
Install Debian
```

**Don't download the DVD/Blu-ray images.** They're unnecessarily large for what you're doing.
