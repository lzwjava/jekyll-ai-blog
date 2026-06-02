---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Setting Git Bash As VS Code Terminal
translated: false
type: note
---

**Question:** How to set VS Code terminal profile to use Git Bash in Windows?

**Answer:**

Here are the most reliable and up-to-date ways (2025) to set Git Bash as your default terminal in Visual Studio Code on Windows:

### Method 1: Recommended (via Terminal Profiles - easiest)

1. Press **Ctrl + ,** → open Settings
2. Search for: `terminal.integrated.profiles.windows`
3. Click **"Edit in settings.json"** (or click the {} icon on the right)
4. Add or modify the following content:

```json
"terminal.integrated.profiles.windows": {
  "Git Bash": {
    "source": "Git Bash",
    "icon": "terminal-bash"
  },
  "PowerShell": {
    "source": "PowerShell",
    "icon": "terminal-powershell"
  },
  "Command Prompt": {
    "path": [
      "${env:windir}\\Sysnative\\cmd.exe",
      "${env:windir}\\System32\\cmd.exe"
    ],
    "args": []
  }
},
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

5. Save the file → new terminals should open with Git Bash

### Method 2: Quick one-liner (if Git Bash is already detected)

Many recent VS Code versions auto-detect Git Bash. You can just do:

1. Open Command Palette (**Ctrl+Shift+P**)
2. Type → **Terminal: Select Default Profile**
3. Choose **Git Bash**

If you don't see Git Bash in the list → use Method 1 or Method 3.

### Method 3: Explicit path (most reliable when auto-detection fails)

```json
"terminal.integrated.profiles.windows": {
  "Git Bash": {
    "path": "C:\\Program Files\\Git\\bin\\bash.exe",
    "icon": "terminal-bash",
    "args": [
      "--login",
      "-i"
    ]
  }
},
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

Common alternative paths (choose the one that exists on your system):

```text
C:\Program Files\Git\bin\bash.exe
C:\Program Files\Git\git-bash.exe
C:\Program Files (x86)\Git\bin\bash.exe
C:\tools\Git\bin\bash.exe               ← common in Scoop / manual install
```

### Bonus: Make Git Bash feel more like a modern terminal

Add these optional but very popular settings:

```json
"terminal.integrated.shellArgs.windows": ["--login", "-i"],
"terminal.integrated.fontFamily": "Cascadia Code, Consolas, 'Courier New', monospace",
"terminal.integrated.cursorStyle": "line",
"terminal.integrated.cursorBlinking": true,
"terminal.integrated.scrollback": 10000,
```

### Quick Troubleshooting Checklist

- Git is **not** installed → install from https://git-scm.com
- Git Bash still not appearing → restart VS Code
- Using portable Git? → use full path in `path` field
- Using Scoop/Chocolatey custom location? → find real path with `where bash`

Most common winning combination in 2025:

```json
"terminal.integrated.defaultProfile.windows": "Git Bash",
"terminal.integrated.profiles.windows": {
  "Git Bash": {
    "path": "C:\\Program Files\\Git\\bin\\bash.exe",
    "icon": "terminal-bash"
  }
}
```

Good luck!

**References:**

- None needed (this is based on current VS Code + Git for Windows behavior)
