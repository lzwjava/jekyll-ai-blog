---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Setup Failure Diagnosis
translated: false
type: note
---

Question: Check the Windows installation failure from `setuperr.log` screenshot.

Answer:

I checked the screenshot. The important lines are:

```
CUnattendManager::Initialize(90): Result = 0x80070490
CMOSetupOneSettingsHelper<...>::InitializeSettings(324): Result = 0x80072EE7
CSetupHost::InitializeOneSettings(1606): Result = 0x80072EE7

...
CSetupManager::ExecuteInstallMode(...)
CSetupHost::Execute(564): Result = 0xC19001F4
```

The final error:

```
0xC19001F4
```

is the real failure code. It means Windows Setup failed during the installation workflow, but the screenshot alone does **not** show the original trigger.

The earlier errors:

```
0x80070490
```

= `ERROR_NOT_FOUND` (something expected in setup configuration was missing)

```
0x80072EE7
```

= name resolution failure (DNS/network lookup failure)

These are usually **secondary**. The important part is that setup entered a failure path and rolled back.

From your previous context (Lenovo Xiaoxin + USB install + recovery environment message), the likely causes are:

### 1. Wrong USB install media method (most likely)

You created the USB on Mac using FAT32 + copied files. Windows 11 25H2 ISO has:

```
sources/install.wim
```

which is often >4GB.

If you split WIM incorrectly or the ISO copy was incomplete, setup can fail later.

Check USB:

Boot back to Windows PE command prompt:

```cmd
dir D:\sources
```

You should see:

```
install.swm
install2.swm
```

or:

```
install.wim
```

not a missing file.

---

### 2. Disk partition state problem

Earlier you had:

```
partition is of an unrecognized type
selected volume is offline
```

If the Lenovo SSD still has old metadata:

Open command prompt:

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

Then install again.

**Warning:** `clean` destroys all partitions.

---

### 3. Network-related setup failure

Because:

```
0x80072EE7
```

appears.

During Windows 11 setup, avoid online account setup.

At the OOBE stage:

Press:

```
Shift + F10
```

then:

```cmd
OOBE\BYPASSNRO
```

Reboot and choose:

```
I don't have internet
```

---

### What I need next

The screenshot is only the tail of `setuperr.log`. The most useful part is earlier.

Please send:

```
C:\$WINDOWS.~BT\Sources\Panther\setupact.log
```

around the first occurrence of:

```
Error
```

or run:

```cmd
findstr /i "error failed rollback 0xc190" setupact.log
```

Also tell me:

1. Did it fail during:

   * copying files %
   * installing features %
   * first reboot
   * final "getting ready" phase?

2. Is your USB created with:

   * `wimlib-imagex split install.wim`
   * Rufus
   * Etcher
   * manual copy?

My suspicion currently: **USB media / install.wim handling or old SSD partition metadata**, not the recovery-environment line itself.
