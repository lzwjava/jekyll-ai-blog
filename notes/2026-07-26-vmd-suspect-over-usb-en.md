---
audio: false
generated: true
image: false
lang: en
layout: post
title: VMD Suspect Over USB
translated: false
type: note
---

Question: Another agent says the USB is valid and the real problem is Lenovo VMD/RST. Is that conclusion correct?

Answer:

Yes — **the other agent's conclusion is now much stronger than my earlier USB suspicion**.

The new information changes the diagnosis:

Your USB has:

```
sources/boot.wim       ✅
sources/install.swm    ✅
sources/install2.swm   ✅
sources/install3.swm   ✅
```

That means:

* Windows PE boots ✅
* Setup environment loads ✅
* Windows image exists ✅
* Split WIM is correct ✅

So **do not rebuild the USB**.

The failure is probably after image deployment, and VMD/RST becomes a top suspect.

---

## Why VMD can cause exactly this pattern

Modern Lenovo laptops often ship with:

```
BIOS
 |
Intel VMD Controller
 |
NVMe SSD
```

Windows installer WinPE can sometimes see the disk because it has extra drivers.

But after the first reboot:

```
Windows installed
 |
Boot from NVMe
 |
No Intel VMD driver loaded
 |
NVMe disappears
 |
Boot failure
 |
Recovery / rollback
 |
0xC19001F4
```

The log sequence matches:

```
Setup Phase [4]
...
User has requested to launch the recovery environment
...
0xC19001F4
```

The failure is not during copying. It is during transition to the installed OS.

---

## Check BIOS first

On Lenovo Xiaoxin:

Enter BIOS:

```
F2
```

Look for:

```
Configuration
    Storage
        Intel VMD Controller
```

Change:

```
Enabled -> Disabled
```

or:

```
RST Premium -> AHCI
```

Names vary by model.

Save:

```
F10
```

Then reinstall using the same USB.

---

## But one caveat

Before changing VMD, check one thing:

When Windows Setup shows the disk list:

Press:

```
Shift + F10
```

Run:

```cmd
diskpart

list disk
```

If you see:

```
Disk 0   512 GB
```

then WinPE sees the NVMe.

After installation failure, check:

```cmd
diskpart

list disk
```

again.

If the SSD disappears, that is almost a VMD driver issue.

---

## My updated probability

After seeing the valid USB:

| Cause                      | Probability |
| -------------------------- | ----------: |
| Intel VMD/RST mode         |         60% |
| EFI/old partition metadata |         25% |
| Driver issue               |         10% |
| USB/ISO                    |         <5% |

The other agent's argument is better at this point.

I would **not touch the USB**. Change BIOS VMD/AHCI first. This is the fastest experiment and does not destroy data.
