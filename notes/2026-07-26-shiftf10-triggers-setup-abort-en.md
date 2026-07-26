---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shift+F10 Triggers Setup Abort
translated: false
type: note
---

Question: What does setupact.log actually reveal — is this a real failure or something else?

Answer: Found it — this isn't a disk, driver, or media problem. Look at this line right before everything cascades:

```
MOUPG    User has requested to launch the recovery environment
MOUPG    CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4
```

Then every subsequent operation returns that same `0xC19001F4` and Setup force-quits. **This means something during the install progress triggered a "launch recovery environment" request**, and Setup aborted itself in response — it wasn't a crash, it was Setup reacting to an interrupt signal.

This almost certainly happened because you pressed **Shift+F10 while the install was actively copying files/progressing** (trying to get to command prompt to check the log, per our last few messages) — instead of at the static "Select location to install" screen. During the active copy/apply-image phase, certain key combos get intercepted differently and can trigger this recovery-launch abort instead of opening cmd cleanly.

**Good news: your disk and partition setup (GPT, unallocated Disk 0) is fine — this was an interruption, not a real fault.**

Fix: just run Setup again, and this time **don't press any keys once it hits the "Installing Windows" progress screen** — let it run completely uninterrupted through all reboots until you reach OOBE (region/account setup). If you need to check something mid-install in the future, don't touch the keyboard during the copying/progress phase at all.

Go back to:
1. Boot USB installer
2. Select Disk 0 unallocated → Next
3. Let it run fully, hands off, until it finishes.
