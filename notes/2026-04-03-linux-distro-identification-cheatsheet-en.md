---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Distro Identification Cheatsheet
translated: false
type: note
---

Simple — I ran one command over SSH:

```
cat /etc/os-release
```

Every Linux distro has this file. It gives you the OS name, version, codename, all in a standard format. I also ran `uname -a` for the kernel version, but `os-release` is the main one for identifying the distro.

Quick cheat sheet for other checks:
- **`cat /etc/os-release`** — distro info (works on almost everything)
- **`lsb_release -a`** — another way, but needs `lsb-release` package
- **`uname -a`** — kernel version and architecture
- **`hostnamectl`** — combines hostname + OS + kernel (needs systemd)
