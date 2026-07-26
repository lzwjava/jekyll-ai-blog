---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding the Windows Install Failure
translated: false
type: note
---

Question: Check the new `setupact.log` screenshots and identify the Windows install failure point.

Answer:

I checked both screenshots. They actually reveal something important:

**The log you captured is still not the failure point.**

The visible part shows a normal setup flow:

```
CInstallUI::SwitchToProgressPage
Next button clicked
LanguageSelection...
KeyboardSelection...
ProgressHandlerAction...
Task progress: [46%]
```

and earlier:

```
Action progress: [100%]
Overall progress: [11%]
Setup Phase: [4]
Setup SubPhase: [54]
```

This means:

* USB boot works ✅
* Windows PE works ✅
* Setup UI works ✅
* Language selection works ✅
* Installation process starts ✅

The failure happens later, after this part.

The line:

```
User has requested to launch the recovery environment
```

is still only the **rollback/recovery path**, not the cause.

---

## Important clue: Setup Phase [4]

Windows setup phases:

```
Phase 1: Downlevel
Phase 2: SafeOS
Phase 3: First boot
Phase 4: Second boot / OOBE transition
```

Your failure appears around:

```
Setup Phase: [4]
```

So this is probably **after the image was applied**.

That makes these less likely:

* ❌ corrupted ISO
* ❌ missing install.wim
* ❌ USB copy problem

because setup already progressed.

More likely:

1. Boot configuration problem
2. Storage controller / VMD driver
3. Driver conflict
4. Existing EFI partition issue

---

## Next check: find the real error

From the command prompt:

```cmd
cd C:\$WINDOWS.~BT\Sources\Panther

findstr /i "error 0xc190 0x8007 failed" setuperr.log
```

Then:

```cmd
notepad setuperr.log
```

Scroll to the **first Error**, not the bottom.

---

## Also check setup rollback log

Windows keeps the real reason here:

```cmd
notepad C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

This file is often much more useful.

Search:

```
Error
Failed
0x
```

---

## My updated guess

Based on the screenshots:

### Most likely: old disk layout / EFI issue

You previously had:

```
partition is of an unrecognized type
volume is offline
```

I would do a completely clean GPT install:

Boot USB → Shift+F10:

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

Back to installer → refresh → install.

This removes:

* old Lenovo recovery partitions
* broken EFI entries
* dynamic disk metadata
* stale RAID signatures

---

Before wiping, send me:

```
C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

or the output of:

```cmd
findstr /i "error failed 0xc190" C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

That should contain the real root cause.
