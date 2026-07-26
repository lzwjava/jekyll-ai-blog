---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo amd64 for Lenovo Xiaoxin
translated: false
type: note
---

Question: **Which Mihomo release should I download for Windows 11 on Lenovo Xiaoxin 14?**

Answer:

For **Lenovo Xiaoxin 14 + Windows 11**, almost certainly choose:

```
mihomo-windows-amd64-alpha-3a779dd.zip
```

Reason:

* Lenovo Xiaoxin 14 uses Intel/AMD x86-64 CPUs (Core i5/i7, Ryzen, etc.)
* Windows 11 on these laptops is **64-bit x86**
* `amd64` means **x86-64 architecture**, not AMD-only

So:

✅ Recommended:

```
mihomo-windows-amd64-alpha-3a779dd.zip
```

---

Avoid these:

### ❌ arm64

```
mihomo-windows-arm64-alpha-3a779dd.zip
```

Only for:

* Snapdragon Windows laptops
* Microsoft Surface Pro X
* ARM-based Windows devices

Your Lenovo Xiaoxin is not ARM.

---

### ❌ 386

```
mihomo-windows-386-alpha-3a779dd.zip
```

Old 32-bit Windows.

Windows 11 does not normally run 32-bit-only systems.

---

### What about amd64-v1/v2/v3?

Examples:

```
mihomo-windows-amd64-v1-alpha.zip
mihomo-windows-amd64-v2-alpha.zip
mihomo-windows-amd64-v3-alpha.zip
```

These are optimized builds based on newer x86 CPU instruction sets.

For maximum compatibility:

```
mihomo-windows-amd64-alpha-3a779dd.zip
```

is the safe choice.

If you want to optimize:

* Intel 10th gen+ / Ryzen 3000+ usually supports v3
* Older CPUs may not

Check:

```powershell
wmic cpu get name
```

or:

```powershell
Get-CimInstance Win32_Processor | Select Name
```

---

After download:

```powershell
Expand-Archive mihomo-windows-amd64-alpha-3a779dd.zip
cd mihomo-windows-amd64-alpha-3a779dd
.\mihomo.exe -v
```

Expected:

```
Mihomo Meta version ...
```

Then put your config:

```
config.yaml
```

next to:

```
mihomo.exe
```

Run:

```powershell
.\mihomo.exe -d .
```

For a Lenovo Xiaoxin 14, the normal choice is simply:

```
✅ mihomo-windows-amd64-alpha-3a779dd.zip
```
