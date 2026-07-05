---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choosing WeChat for Ubuntu
translated: false
type: note
---

**Question:** Which Weixin for Linux package should I choose on Ubuntu?

**Answer:**

If you're using a normal PC running Ubuntu (Intel or AMD CPU), choose:

* ✅ **X86 → `.deb`** (`WeChatLinux_x86_64.deb`)

This is the native package format for Ubuntu and other Debian-based distributions.

### Which one should you choose?

| Your system                                                                         | Choose           |
| ----------------------------------------------------------------------------------- | ---------------- |
| Ubuntu on Intel/AMD (most laptops/desktops, e.g. Core i9, Ryzen)                    | ✅ **X86 `.deb`** |
| Ubuntu on ARM (e.g. Raspberry Pi, Apple M-series running Linux, Snapdragon X Elite) | ✅ **ARM `.deb`** |
| Fedora, RHEL, Rocky, CentOS, openSUSE                                               | `.rpm`           |
| Any Linux distro (portable, no installation)                                        | `AppImage`       |
| Loongson CPU                                                                        | `LoongArch .deb` |

### For your computer

From our previous conversations, your machine has an **Intel Core i9-13900KF** with an **RTX 4070**, so you should download:

> **X86 → `WeChatLinux_x86_64.deb`**

### Installation

After downloading:

```bash
cd ~/Downloads
sudo apt install ./WeChatLinux_x86_64.deb
```

or

```bash
sudo dpkg -i WeChatLinux_x86_64.deb
sudo apt --fix-broken install
```

The first command (`apt install ./...`) is generally preferred because it automatically installs any required dependencies.

### Should you use the AppImage instead?

For Ubuntu, I recommend **`.deb`** because:

* ✅ Integrates with the system menu
* ✅ Easier to update and remove
* ✅ Better desktop integration
* ✅ Standard installation method for Ubuntu

Use **AppImage** only if:

* you don't have administrator (`sudo`) access,
* you want a completely portable copy,
* or you're using a Linux distribution that doesn't use `.deb` or `.rpm`.

So, for your Ubuntu desktop with the i9-13900KF, **download the X86 `.deb` package**.