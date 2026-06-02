---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu Upgrade Removed Git NVIDIA Fix
translated: false
type: note
---

**Question:** After running `do-release-upgrade` from Ubuntu 22.04 to 24.04, should I have chosen to remove old/obsolete packages in the final step? Now both `git` and my NVIDIA driver are gone — how do I fix this?

---

**Answer:**

## Understanding the "Remove Obsolete Packages" Step

After all packages are updated during `do-release-upgrade`, you are prompted to remove any obsolete packages that are no longer needed, with a message like: "Remove obsolete packages? 30 packages are going to be removed. Continue [y/N] Details [d]"

You can press `d` to view details about such packages before deciding. Outdated packages do not receive security updates, so removing them is generally reasonable — but you may wish to keep them so that the system keeps working with older apps.

**The short answer: you should always press `d` first and review the list before saying yes.** The problem is that `do-release-upgrade` sometimes incorrectly marks packages like `git` or NVIDIA drivers as "obsolete" — particularly if they came from PPAs, third-party repos (like NVIDIA's own CUDA repo), or if the upgrader lost track of them during the process.

---

## Why Git and NVIDIA Drivers Got Removed

There are two common causes:

**1. Third-party / PPA sources**
The upgrader marks packages as "obsolete" if it cannot find them in the new Ubuntu 24.04 repositories. If your NVIDIA driver was installed from a third-party source (e.g., `ppa:graphics-drivers/ppa` or NVIDIA's CUDA repo), it may not be recognized as a valid 24.04 package and gets flagged for removal.

**2. The NVIDIA upgrader logic failed silently**
The upgrader's internal log can show messages like `INFO no old nvidia driver installed, installing no new` — meaning the tool detected no recognized NVIDIA driver and skipped reinstalling one automatically, leaving you without a driver after the upgrade.

---

## Fix: Reinstall Git

This is straightforward — git is available in Ubuntu 24.04's default repositories:

```bash
sudo apt update
sudo apt install git
```

Verify with:

```bash
git --version
```

---

## Fix: Reinstall NVIDIA Driver on Ubuntu 24.04

**Step 1: Check your GPU**

```bash
lspci | grep -i nvidia
```

**Step 2: Let Ubuntu detect and recommend the right driver**

```bash
sudo ubuntu-drivers list
```

**Step 3: Auto-install the recommended driver**

```bash
sudo ubuntu-drivers autoinstall
```

Or install a specific version manually (replace `550` with your preferred version):

```bash
sudo apt install nvidia-driver-550
```

**Step 4: Make sure kernel headers are installed (required for DKMS)**

```bash
sudo apt install linux-headers-$(uname -r) build-essential
```

**Step 5: Reboot**

```bash
sudo reboot
```

**Step 6: Verify**

```bash
nvidia-smi
```

If `nvidia-smi` is missing after installation, the `nvidia-smi` command is provided by NVIDIA utilities packages. Install the matching utilities package for your branch, such as `nvidia-utils-<version>`, then run `nvidia-smi` again.

---

## If You Have Broken Packages

If `apt install` gives errors about broken packages, clean up first:

```bash
sudo apt purge 'nvidia-*' 'libnvidia-*'
sudo apt clean
sudo apt update
sudo apt -f install
sudo ubuntu-drivers autoinstall
```

---

## Best Practice for Future Upgrades

Before running `do-release-upgrade` next time:

1. **Always press `d`** at the "Remove obsolete packages?" prompt and review what will be removed.
2. **Note down any important packages** you want to reinstall afterward (especially NVIDIA drivers, git, etc.).
3. For NVIDIA users specifically, a safer approach is to switch to the open-source `nouveau` driver before the upgrade, then reinstall the proprietary NVIDIA driver after a successful boot into the new release.

---

References:

- [Ubuntu Server Docs - How to upgrade your release](https://documentation.ubuntu.com/server/how-to/software/upgrade-your-release/)
- [How to Install NVIDIA Drivers on Ubuntu 24.04 - Cherry Servers](https://www.cherryservers.com/blog/install-nvidia-drivers-ubuntu)
- [Ubuntu 24.04 + Nvidia Drivers - projectable.me](https://projectable.me/ubuntu-24-04-nvidia-drivers-ollama/)
- [How to Install NVIDIA Drivers on Ubuntu - LinuxCapable](https://linuxcapable.com/install-nvidia-drivers-on-ubuntu-linux/)
- [do-release-upgrade 22.04 to 24.04 - Launchpad Q&A](https://answers.launchpad.net/ubuntu/+source/ubuntu-release-upgrader/+question/822286)
