---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSD Detected Correctly
translated: false
type: note
---

Question: **If Windows Setup shows Disk 0 512 GB on Lenovo Xiaoxin 14, does that mean the SSD is detected correctly?**

Answer: **Yes.** If Windows Installer shows:

```
Disk 0   512 GB
```

then the SSD is already detected. ✅

That means:

* ✅ UEFI boot from USB works
* ✅ Windows PE loaded
* ✅ Storage controller driver is loaded
* ✅ NVMe SSD is visible
* ❌ Intel VMD/RST is probably **not** the problem

The SSD is likely the internal NVMe drive.

The remaining installation failures are usually caused by:

### 1. Bad partition layout / old metadata

Open command prompt in Windows Setup:

```
Shift + F10
```

Run:

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

Then refresh the disk list and install.

⚠️ `clean` deletes all partitions on Disk 0.

For a fresh Windows install this is usually the correct approach.

---

### 2. Wrong Windows edition / corrupted ISO

Your ISO:

```
Win11_25H2_English_x64_v2.iso
```

is okay if it came from Microsoft.

---

### 3. BIOS Secure Boot / TPM settings

For Xiaoxin 14:

BIOS:

```
Security
  Secure Boot: Enabled

TPM:
  Enabled
```

Windows 11 expects these.

---

Since your SSD appears as **Disk 0 512GB**, I would stop investigating VMD/RST. The next thing I would do is:

```
diskpart
select disk 0
clean
convert gpt
```

and reinstall.

The key question now is: **what exact error appears after you select Disk 0 and click Next?** That will tell us the real issue.