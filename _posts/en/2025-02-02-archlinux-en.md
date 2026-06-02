---
audio: true
generated: false
image: false
lang: en
layout: post
title: Installing Arch Linux
translated: false
type: post
---

Lenovo Xiaoxing 14IAH8 Laptop.

```bash
diskutil list
```

> /dev/disk6 (external, physical):
> #:                       TYPE NAME                    SIZE       IDENTIFIER
> 0:     FDisk_partition_scheme                        *30.8 GB    disk6
> 1:             Windows_FAT_32 NO NAME                 30.8 GB    disk6s1

```bash
% diskutil unmountDisk /dev/disk6
```

> Unmount of disk6 failed: at least one volume could not be unmounted.
> Unmount was dissented by PID 319 (/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds_stores).
> Dissenter parent PPID 1 (/sbin/launchd).

```bash
% diskutil unmountDisk force /dev/disk6
```

```bash
sudo dd if=archlinux-2025.02.01-x86_64.iso of=/dev/rdisk6 bs=1m

1179+1 records in
1179+1 records out
1236303872 bytes transferred in 46.777995 secs (26429176 bytes/sec)
```

The USB drive is locked by the current security policy.

Press F2 to enter the BIOS and disable Secure Boot.

```bash
ip link
iwctl
device list
station wlan0 scan
station wlan0 get-networks
station wlan0 connect SSID
ping archlinux.org
timedatectl
```

For some reason, I decided to install Ubuntu instead.
