---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagerr.xml Setup Failure Analysis
translated: false
type: note
---

Question: Analyze `diagerr.xml` from Windows Setup failure.

Answer:

I checked the screenshot. `diagerr.xml` confirms the same thing, but it **does not contain the root cause**.

The important entries are:

```xml
CUnattendManager::Initialize(90):
Result = 0x80070490

CMOSetupOneSettingsHelper::InitializeSettings(324):
Result = 0x80072EE7

CSetupHost::InitializeOneSettings(1606):
Result = 0x80072EE7

CSetupManager::OnFinishLaunchChoiceAction(8149):
Result = 0xC19001F4
```

Interpretation:

| Code         | Meaning                                | Importance   |
| ------------ | -------------------------------------- | ------------ |
| `0x80070490` | Element/not found                      | Secondary    |
| `0x80072EE7` | Name resolution/network lookup failure | Secondary    |
| `0xC19001F4` | Setup failure wrapper                  | Final result |

`diagerr.xml` is basically a **summary of the failure**, not the detailed failure log.

The real error should be in:

```
C:\$WINDOWS.~BT\Sources\Panther\setuperr.log
```

or more importantly:

```
C:\$WINDOWS.~BT\Sources\Rollback\setupact.log
```

---

One clue from your screenshot:

```xml
Exe="X:\Sources\SetupHost.exe"
```

This is still running from WinPE (`X:`), and failure happens very early in SetupHost initialization.

So I now suspect:

### Possibility 1: Unattend/settings issue (higher than before)

The log mentions:

```
CUnattendManager
CMOSetupOneSettingsHelper
```

Check if your USB contains:

```
\autounattend.xml
```

or:

```
\sources\PID.txt
```

Run:

```cmd
dir D:\autounattend.xml
dir D:\sources\PID.txt
```

If present, remove them and retry.

---

### Possibility 2: Windows ISO / USB creation issue

Because SetupHost cannot initialize settings correctly.

Check USB:

```cmd
dir D:\sources
```

Expected:

```
boot.wim
install.wim
```

or:

```
install.swm
install2.swm
```

---

### Possibility 3: Existing disk metadata

Still possible because of your earlier offline/unrecognized volume problem.

The clean install test:

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

Then reinstall.

---

Next, please capture:

```
C:\$WINDOWS.~BT\Sources\Panther\setuperr.log
```

especially the **top 30 lines**.

`diagerr.xml` only tells us "Setup failed"; `setuperr.log` tells us "why".
