---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Missing SSH After Debian Live Install
translated: false
type: note
---

Question: You installed Debian from `debian-live-13.6.0-amd64-xfce.iso`, and `openssh-server` isn't available.

Answer: Yes — that explains it. The **Live XFCE ISO can install a working desktop without having a configured APT network mirror**, especially if you skipped the mirror configuration during installation.

First check:

```bash
cat /etc/apt/sources.list
```

On modern Debian 13, also check:

```bash
ls -l /etc/apt/sources.list.d/
cat /etc/apt/sources.list.d/* 2>/dev/null
```

### Easiest fix

If your machine has Internet access, create a Debian 13 repository configuration:

```bash
sudo tee /etc/apt/sources.list.d/debian.sources >/dev/null <<'EOF'
Types: deb
URIs: https://deb.debian.org/debian
Suites: trixie trixie-updates
Components: main

Types: deb
URIs: https://security.debian.org/debian-security
Suites: trixie-security
Components: main
EOF
```

Then:

```bash
sudo apt update
sudo apt install openssh-server
```

Start SSH:

```bash
sudo systemctl enable --now ssh
```

Verify:

```bash
systemctl status ssh
```

Then from another computer on your LAN:

```bash
ssh your_user@DEBIAN_LAN_IP
```

Find the IP with:

```bash
hostname -I
```

For example:

```bash
ssh zhiwei@192.168.1.123
```

**Important:** Debian 13 uses the newer `.sources` repository format by default, so don't worry if `/etc/apt/sources.list` is empty. The real configuration may be under `/etc/apt/sources.list.d/`.

If you paste the output of:

```bash
cat /etc/apt/sources.list
ls -l /etc/apt/sources.list.d/
```

I can tell you exactly what your installation currently has.
