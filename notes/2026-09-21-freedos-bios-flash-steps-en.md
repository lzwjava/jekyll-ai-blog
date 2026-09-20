---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeDOS BIOS Flash Steps
translated: false
type: note
---

You're at the FreeDOS prompt — that's exactly where you want to be. ("CD-ROM not configured" is harmless, ignore it.)

At the `C:\>` prompt:

**1. Confirm the files are there:**
```
dir
```
You should see `FLASH.BAT`, `FPT.EXE`, `FPARTS.TXT`, `NEWBIOS.BIN`, `OLDBIOS.BIN`.

**2. Run the flash:**
```
flash.bat
```

**3. Watch the output:**
- It first dumps your current BIOS → `BACKUP.BIN`
- Then flashes `NEWBIOS.BIN`

**4. Wait for:**
```
FLASH OK. Power off, then power on.
```

---

If `flash.bat` shows `FLASH FAILED` — **do not power off**, just run `fpt -f NEWBIOS.BIN` once more.

If `dir` does **not** show the files (e.g. the prompt is on the wrong drive), check `A:` and `B:` too:
```
dir a:\
dir b:\
```
and if they're there, run `a:\flash.bat`.

Tell me what `flash.bat` prints.