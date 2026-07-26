---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install x64 PowerToys on Xiaoxin 14
translated: false
type: note
---

Question: **For Lenovo Xiaoxin 14, should I install PowerToys x64.exe or ARM64.exe?**

Answer:

Install **x64.exe**.

Lenovo Xiaoxin 14 laptops use **Intel or AMD x86-64 CPUs**, not ARM processors. The correct architecture is:

```
PowerToysSetup-x64.exe
```

Do **not** install:

```
PowerToysSetup-arm64.exe
```

ARM64 is for devices like:

* Microsoft Surface Pro X
* Snapdragon Windows laptops
* Windows on ARM machines

You can confirm your CPU:

1. Press `Win + R`
2. Run:

```cmd
msinfo32
```

Check:

```
System Type: x64-based PC
```

or:

```cmd
wmic cpu get name
```

Typical Xiaoxin 14 CPUs:

* Intel Core i5/i7 → x64 ✅
* AMD Ryzen → x64 ✅
* Snapdragon/ARM → ARM64 ❌

So for your Windows installation on Lenovo Xiaoxin 14:

```
Windows 10/11 x64
+
PowerToys x64
```

is the correct stack.
