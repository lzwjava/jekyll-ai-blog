---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recovery environment not root cause
translated: false
type: note
---

Question: Analyze this `setupact.log` screenshot — is "User has requested to launch the recovery environment" the root cause?

Answer:

This screenshot gives a clearer picture. The important sequence is:

```
CInstallUI::SwitchToProgressPage
CSetupResponseTemplate<class IDlpResponse>::ExecuteRoutine: Next button clicked.

...

User has requested to launch the recovery environment

Error
CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4
```

The key point:

**"User has requested to launch the recovery environment" is not the root cause. It is the action Windows Setup takes after the installation fails.**

The flow is:

```
Install fails
    |
    v
Setup shows failure/recovery choice
    |
    v
Recovery environment selected
    |
    v
0xC19001F4 logged
```

So my previous suspicion about keyboard/recovery trigger is less likely. This log actually shows:

```
Next button clicked
```

meaning Setup UI moved forward normally.

The actual failure happened **before this section**.

---

## Need the earlier error

Run this in WinPE command prompt:

```cmd
cd C:\$WINDOWS.~BT\Sources\Panther

findstr /i "error failed failure rollback 0xc190" setupact.log > errors.txt

notepad errors.txt
```

Send the `errors.txt` content.

---

## Also check these two files

### 1. Setup error log

```cmd
notepad C:\$WINDOWS.~BT\Sources\Panther\setuperr.log
```

Look for the **first error**, not the last.

---

### 2. Installation phase

Find:

```cmd
findstr /i "InstallImage ApplyImage ApplyOS" setupact.log
```

This tells us whether failure happened during:

* applying Windows image
* driver injection
* boot configuration
* OOBE phase

---

## My current probability estimate from your previous history

Given:

* Lenovo Xiaoxin
* Windows 11 25H2 ISO
* USB prepared on Mac
* previous disk "offline/unrecognized type" issue

I would rank:

### 1. SSD partition metadata problem — 40%

Fix:

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

Then install.

---

### 2. USB media / WIM issue — 35%

Check:

```cmd
dir D:\sources
```

Need either:

```
install.wim
```

or:

```
install.swm
install2.swm
...
```

---

### 3. Driver/storage controller issue — 20%

Lenovo machines often use Intel VMD/RST.

BIOS check:

```
Storage Controller Mode
```

If enabled:

* either load Intel RST driver during setup
* or disable VMD and use AHCI

---

### 4. Actual recovery environment trigger — <5%

This screenshot basically rules that out.

The next useful screenshot is **the first 50 lines around the first "Error" entry in setupact.log**, not the ending. That will contain the real cause.
