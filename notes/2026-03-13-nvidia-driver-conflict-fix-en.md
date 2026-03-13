---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix NVIDIA Driver Package Conflict
translated: false
type: note
---

Question: How do I fix the conflict between `nvidia-compute-utils-535` and `nvidia-persistenced` during NVIDIA driver installation on Ubuntu?

Answer:

## Root Cause

`nvidia-compute-utils-535` **includes** `nvidia-persistenced` functionality built-in, but there is also a **separate standalone** `nvidia-persistenced` package installed on your system. They conflict because they both provide the same binary/service.

```
nvidia-compute-utils-535  ←  ships nvidia-persistenced binary internally
nvidia-persistenced        ←  standalone package, same binary = CONFLICT
```

---

## Fix: Remove the conflicting package first

### Step 1: Remove `nvidia-persistenced`

```bash
sudo apt remove --purge nvidia-persistenced
sudo apt remove --purge nvidia-persistenced:i386
```

### Step 2: Fix broken state

```bash
sudo dpkg --configure -a
sudo apt --fix-broken install
```

### Step 3: Now retry the installation

```bash
sudo apt install nvidia-compute-utils-535
```

---

## If Step 1 Fails (dependency holds it)

Force-remove it via dpkg directly:

```bash
sudo dpkg --remove --force-depends nvidia-persistenced
```

Then clean up:
```bash
sudo apt --fix-broken install
sudo apt autoremove --purge
```

---

## If You Still Have Held Packages

Check what is held:
```bash
sudo apt-mark showhold
dpkg -l | grep ^h
```

Unhold everything NVIDIA-related:
```bash
sudo apt-mark unhold nvidia-* libnvidia-* cuda-*
```

Then retry:
```bash
sudo apt --fix-broken install
sudo apt upgrade
```

---

## Full Picture of Your Current Situation

Based on all the errors you've hit so far, your system has accumulated conflicts from **3 sources mixed together**:

| Package Source | Version Suffix | Example |
|---|---|---|
| Ubuntu official repo | `-0ubuntu1` | `535.288.01-0ubuntu1` |
| NVIDIA CUDA repo | `-0ubuntu0.22.04.1` | `535.288.01-0ubuntu0.22.04.1` |
| Standalone old packages | varies | `nvidia-persistenced` |

The cleanest long-term fix remains a **full purge and reinstall** from a single source once you clear this conflict:

```bash
# Nuclear option - only if above steps fail
sudo apt purge nvidia-* libnvidia-* cuda-* --allow-remove-essential
sudo apt autoremove --purge
sudo apt clean
sudo apt update
sudo apt install nvidia-driver-535
```

References:

- [Ubuntu Manpage: apt-mark](https://manpages.ubuntu.com/manpages/focal/man8/apt-mark.8.html)
- [NVIDIA CUDA Toolkit Download](https://developer.nvidia.com/cuda-downloads)