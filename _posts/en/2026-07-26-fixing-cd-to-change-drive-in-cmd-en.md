---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing cd to change drive in cmd
translated: false
type: note
---

Question: In Windows cmd, `cd E:\` only prints `E:\` but doesn't actually switch the current drive/directory — how to fix?

Answer: `cd` alone doesn't change drives in cmd.exe — it only changes directory *within* the current drive. To also switch drives, use `/d`:

```cmd
cd /d E:\
```

Or the two-step way (this is the classic trick):

```cmd
E:
cd \
```

Why: cmd tracks a separate "current directory" per drive letter. `cd E:\` sets what E:'s current dir would be, but since you're still on C:, nothing visibly changes — that's why it just echoes `E:\` back at you (that's actually `cd` with no dir arg after the drive letter, just confirming). `cd /d` forces both the drive switch and the directory change at once.

References:
- [CD command - Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cd)
