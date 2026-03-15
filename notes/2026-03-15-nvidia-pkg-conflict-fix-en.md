---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix NVIDIA Package Conflict Steps
translated: false
type: note
---

Here's how I'd fix that NVIDIA package conflict:

**1. Diagnose the conflict**
```bash
dpkg -l | grep -E "nvidia-compute-utils|nvidia-persistenced"
apt-cache show nvidia-compute-utils-535 | grep -i persistenced
```

**2. Remove the standalone package**
```bash
sudo apt remove --purge nvidia-persistenced
```
This removes the old standalone package that conflicts with the built-in one in nvidia-compute-utils-535.

**3. Clean up and reconfigure**
```bash
sudo apt autoremove
sudo apt --fix-broken install
sudo dpkg --configure -a
```

**4. Retry the driver installation**
```bash
sudo apt install nvidia-driver-535
```

**Why this works:** nvidia-compute-utils-535 already includes the persistenced binary and service. Having the separate package means two files trying to occupy the same path, which dpkg refuses. Removing the standalone one lets the newer package take over cleanly.

I'd also disable any old nvidia-persistenced service if it's still in systemd:
```bash
sudo systemctl disable nvidia-persistenced
sudo systemctl daemon-reload
```

That's the full fix.