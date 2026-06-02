---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Warp's Windows Path Space Issue
translated: false
type: note
---

That's a Warp Windows validation issue — it doesn't accept paths with spaces directly in the shell command field.

**Fix: quote the path or use the short path form**

Try these in order:

**Option 1: Quoted path**
```
"C:\Program Files\Git\bin\bash.exe" --login -i
```

**Option 2: Use forward slashes (MSYS style)**
```
C:/Program Files/Git/bin/bash.exe --login -i
```

**Option 3: 8.3 short path (always works)**
```
C:\PROGRA~1\Git\bin\bash.exe --login -i
```

Verify your 8.3 path first — run this in PowerShell:
```powershell
cmd /c "for %I in ("C:\Program Files\Git\bin\bash.exe") do echo %~sI"
```

**Option 4: Use `cmd /c` as a wrapper**
```
cmd /c "C:\Program Files\Git\bin\bash.exe" --login -i
```

**Option 5: Point to `git-cmd.exe` shim**
```
C:\Program Files\Git\git-cmd.exe --command=usr/bin/bash.exe --login -i
```

---

Also worth checking: Warp on Windows is still relatively new and Git Bash support is rough. If none of these save, the practical move is **WSL2 as your default profile** — zero friction, full Linux, and Warp's shell integration works perfectly with it.
