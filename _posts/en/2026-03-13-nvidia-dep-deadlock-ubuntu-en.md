---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix NVIDIA Dependency Deadlock Ubuntu
translated: false
type: note
---

Question: How do I fix the NVIDIA package dependency deadlock on Ubuntu where `apt --fix-broken install` and `apt autoremove` both fail with unmet dependencies in a loop?

Answer:

## Diagnosis

You're stuck in a circular dependency hell caused by **mixed NVIDIA package versions**:
- Some packages are at `535.288.01-0ubuntu1` (Ubuntu repo)
- Some are still at `535.274.02-0ubuntu1` or `535.288.01-0ubuntu0.22.04.1` (NVIDIA repo)

The only reliable escape is a **full NVIDIA purge and clean reinstall**.

---

## Step-by-Step Fix

### Step 1: Force-overwrite the two originally failing packages first

```bash
sudo dpkg -i --force-overwrite \
  /var/cache/apt/archives/nvidia-kernel-common-535_535.288.01-0ubuntu1_amd64.deb
```

If those `.deb` files are gone from cache, re-download them:
```bash
sudo apt-get download nvidia-kernel-common-535 libnvidia-extra-535
sudo dpkg -i --force-overwrite nvidia-kernel-common-535_*.deb
sudo dpkg -i --force-overwrite libnvidia-extra-535_*.deb
```

---

### Step 2: Force-remove ALL NVIDIA and CUDA packages

```bash
sudo dpkg --remove --force-remove-reinstreq \
  $(dpkg -l | grep -E 'nvidia|cuda|libnvidia' | awk '{print $2}' | tr '\n' ' ')
```

Or more conservatively, list them first:
```bash
dpkg -l | grep -E 'nvidia|cuda|libnvidia' | awk '{print $2}'
```

Then remove everything listed:
```bash
sudo apt purge --allow-remove-essential \
  nvidia-* libnvidia-* cuda-* nvidia-dkms-535 nvidia-kernel-common-535 \
  nvidia-firmware-535-535.288.01 -y
```

---

### Step 3: Clean up broken state

```bash
sudo dpkg --configure -a
sudo apt --fix-broken install
sudo apt autoremove --purge
sudo apt clean
sudo apt autoclean
```

---

### Step 4: Remove any leftover NVIDIA apt sources causing version conflicts

```bash
# List all NVIDIA-related sources
grep -r nvidia /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null
```

If you see entries from **both** `ppa:graphics-drivers` AND `developer.download.nvidia.com`, **remove one** to avoid future conflicts:
```bash
sudo rm /etc/apt/sources.list.d/cuda*.list
# or
sudo add-apt-repository --remove ppa:graphics-drivers/ppa
```

Then update:
```bash
sudo apt update
```

---

### Step 5: Reinstall cleanly from ONE source only

```bash
sudo apt install nvidia-driver-535 nvidia-dkms-535
```

Or if you need CUDA:
```bash
sudo apt install cuda-12-2
```

---

### Step 6: Reboot and verify

```bash
sudo reboot
# After reboot:
nvidia-smi
```

---

## Key Principle

| Rule | Detail |
|------|--------|
| Never mix sources | Pick Ubuntu repo OR NVIDIA repo, not both |
| Version suffix `-0ubuntu1` | Comes from Ubuntu's official repo |
| Version suffix `-0ubuntu0.22.04.1` | Comes from NVIDIA's own CUDA repo |
| These **conflict** when they share firmware files | Always purge before switching sources |

References:

- [NVIDIA CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
- [Ubuntu help: broken packages](https://help.ubuntu.com/community/BrokenPackages)
