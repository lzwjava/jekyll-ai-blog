---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install WSL 2 on Windows
translated: false
type: note
---

Installing **WSL 2 (Windows Subsystem for Linux 2)** is straightforward on modern Windows 10 and Windows 11.

### Option 1: One-command installation (recommended)

1. Open **PowerShell** or **Command Prompt** as **Administrator**.
2. Run:

```powershell
wsl --install
```

This command will:

* Enable WSL
* Install WSL 2
* Download the Linux kernel
* Install Ubuntu (by default)
* Configure everything automatically

Restart your computer if prompted. ([Microsoft Learn][1])

---

### Verify the installation

After restarting, open PowerShell and run:

```powershell
wsl --status
```

To see installed distributions:

```powershell
wsl --list --verbose
```

You should see something like:

```text
NAME      STATE    VERSION
Ubuntu    Running  2
```

If the version is `2`, you're using WSL 2. ([Microsoft Learn][1])

---

### Install a different Linux distribution

To see available distributions:

```powershell
wsl --list --online
```

Install one, for example:

```powershell
wsl --install -d Ubuntu
```

or

```powershell
wsl --install -d Debian
```

---

### If you already have WSL 1

Convert an existing distribution to WSL 2:

```powershell
wsl --set-version Ubuntu 2
```

Replace `Ubuntu` with your distribution name if necessary. ([Microsoft Learn][1])

---

### Check Windows version

WSL 2 requires:

* Windows 11, or
* Windows 10 version 1903 or later (with the required build updates). ([Microsoft Learn][2])

---

### Official Microsoft guide

For detailed instructions and troubleshooting, see:

[Install WSL on Windows (Microsoft Learn)](https://learn.microsoft.com/en-us/windows/wsl/install?utm_source=chatgpt.com)

If you tell me:

* your **Windows version** (Windows 10 or 11), and
* the output of `winver`

I can provide instructions specific to your system.

[1]: https://learn.microsoft.com/en-us/windows/wsl/install?utm_source=chatgpt.com "How to install Linux on Windows with WSL"
[2]: https://learn.microsoft.com/en-us/windows/wsl/install-manual?utm_source=chatgpt.com "Manual installation steps for older versions of WSL"