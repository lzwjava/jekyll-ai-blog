---
audio: false
generated: true
image: false
lang: en
layout: post
title: Is Manual Setup for WSL 2 Required?
translated: false
type: note
---

Question: **Do we need to manually enable the Windows Linux features before installing WSL 2?**

Answer:

Yes, conceptually **WSL 2 requires enabling Windows features**, but on modern Windows the command:

```powershell
wsl --install
```

does this automatically:

* Enable **Windows Subsystem for Linux**
* Enable **Virtual Machine Platform**
* Install the WSL 2 Linux kernel
* Set WSL 2 as default
* Install Ubuntu

So you usually **do not need to open the Windows Features GUI**.

---

If you want to do it manually:

1. Press:

```
Win + R
```

2. Run:

```
optionalfeatures.exe
```

3. Enable:

✅ **Windows Subsystem for Linux**

✅ **Virtual Machine Platform**

Like this:

```
[✓] Windows Subsystem for Linux
[✓] Virtual Machine Platform
```

Then reboot.

---

After reboot:

Open **PowerShell as Administrator**:

```powershell
wsl --set-default-version 2
```

Then install Linux:

```powershell
wsl --install -d Ubuntu
```

---

For Windows 11, also make sure CPU virtualization is enabled:

Task Manager → Performance → CPU:

```
Virtualization: Enabled
```

If it says Disabled, enable:

* Intel VT-x / Intel Virtualization Technology
* AMD SVM

in BIOS.

For your Lenovo Xiaoxin 14, this is usually already enabled, but worth checking if WSL2 complains about virtualization.