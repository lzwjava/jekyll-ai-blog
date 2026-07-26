---
audio: false
generated: true
image: false
lang: en
layout: post
title: Force Shutdown During Windows 11 Update
translated: false
type: note
---

Question: **During “Windows 11 update in progress, please do not shut down”, can we force shutdown?**

Answer:

Technically **yes, you can force shutdown**, but it is **not recommended** while Windows is applying updates.

The risk depends on the update stage:

### 1. If it is downloading/installing inside Windows

Usually safe-ish:

```
Start menu → Shut down
```

Windows will normally finish or pause safely.

### 2. If the screen says

```
Windows 更新正在进行中
请不要关机
Working on updates
不要关闭计算机
```

and the percentage is moving (e.g. 30%, 75%, 100%), **do not force power off**.

Windows may be:

* replacing system files
* updating registry
* updating boot components
* migrating drivers

Interrupting here can cause:

* automatic repair loop
* failed boot
* corrupted update state

### 3. If it is stuck for a very long time

A practical rule:

* < 1 hour: wait
* 1–3 hours: still possible for large updates, especially SSD + slow CPU
* > 3 hours with **no percentage change / no disk activity**: consider forced shutdown

Forced shutdown:

Hold power button:

```
Press and hold power button ~5-10 seconds
```

Then boot again.

Windows 11 usually has recovery mechanisms:

```
Automatic Repair
→ Troubleshoot
→ Advanced options
→ Startup Repair
```

For your Lenovo Xiaoxin 14 situation (you were reinstalling Windows 11 recently), I would especially avoid interrupting the first update cycle after installation because it may still be installing chipset/VMD/storage drivers. Wait if possible.
