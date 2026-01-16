---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Automate Python Scripts via Keyboard Shortcuts
translated: false
type: note
---

**Question:** Can I create a browser extension or use another method to run the `python scripts/create/create_note.py grok-fast` script with a keyboard shortcut, without needing to switch to the terminal each time?

**Answer:**

Yes — several practical approaches exist. Here are the most realistic ones in 2025–2026, ordered from **easiest/fastest to set up** to **most customizable**:

### Recommended options (ranked by ease + reliability)

1. **macOS – Use Shortcuts.app + global keyboard shortcut** (easiest if you're on macOS)  
   - Open Shortcuts app  
   - Create new shortcut  
   - Add action **Run Shell Script**  
   - Set “Shell” = `/bin/zsh` or `/bin/bash`  
   - Paste:

     ```bash
     cd ~/path/to/your/blog-repo
     python3 scripts/create/create_note.py grok-fast
     ```

   - (optional) Add **Open URLs** → `github.com/lzwjava/blog-source/…` if you usually want to see the file  
   - Give the shortcut a name e.g. “New Grok Note”  
   - Menu bar → Shortcuts → Settings → Keyboard Shortcuts → Services → assign e.g. `⌃⌥⌘ N`

   → Global shortcut, no terminal window appears (if you turn off “Show terminal”)

2. **Windows – PowerToys + Run command / .bat wrapper**  
   - Install Microsoft PowerToys (free)  
   - Enable **Keyboard Manager** or **PowerToys Run**  
   - Create small `.bat` or `.cmd` file next to the repo:

     ```bat
     @echo off
     cd /d "C:\path\to\your\blog-repo"
     python scripts\create\create_note.py grok-fast
     ```

   - In PowerToys Keyboard Manager → remap an unused key combo (e.g. `Ctrl+Alt+N`) → run program → point to that `.bat`

   Alternative: use **AutoHotkey v2** (very powerful, small learning curve)

     ```autohotkey
     ^!n::  ; Ctrl+Alt+N
     {
         Run 'cmd.exe /c cd /d "C:\path\to\repo" && python scripts\create\create_note.py grok-fast'
         ; or Run 'wt.exe -w 0 nt --title "Note" -- cd ...'  if you want Windows Terminal
     }
     ```

3. **Linux – xbindkeys / sxhkd / AutoKey / custom .desktop shortcut**  
   Most popular quick solutions:

   - **sxhkd** (if you use bspwm/sway/awesome/xmonad)

     ```bash
     # ~/.config/sxhkd/sxhkdrc
     super + n
         ~/bin/new-grok-note
     ```

     and `~/bin/new-grok-note`:

     ```bash
     #!/usr/bin/env bash
     cd ~/projects/blog-source
     python3 scripts/create/create_note.py grok-fast
     ```

   - **AutoKey** (GUI, works on any X11/Wayland desktop)

4. **Cross-platform – Raycast / Alfred / Ulauncher extension** (very convenient if you already use them)

   - **Raycast** (macOS, very popular in 2025)  
     Create a new script command → type the cd + python line → assign hotkey  
     Bonus: you can make it accept arguments later (`grok-fast`, `claude`, etc.)

   - **Alfred** (macOS) – same idea, Workflow → Run Script

5. **Browser extension – only realistic for very specific cases**

   A browser extension alone **cannot** directly run a local Python script (security restriction).

   Workarounds people actually use:

   - Extension sends POST request to localhost:port  
   - You run a tiny HTTP server in background (FastAPI / Flask / http.server) that executes the command when it receives the request

     ```python
     # run in background: python local_note_server.py
     from fastapi import FastAPI
     import subprocess
     app = FastAPI()

     @app.post("/new-grok-note")
     async def create():
         subprocess.run(["python", "scripts/create/create_note.py", "grok-fast"], cwd="/path/to/repo")
         return {"status": "ok"}
     ```

     → Chrome/Firefox extension only does `fetch("http://localhost:8765/new-grok-note", {method:"POST"})`

     → You still need something running locally → complexity ↑

   → Usually **not worth it** unless you want the trigger to come from inside a webpage.

### Quick recommendation table (2026 reality)

| OS          | Easiest path right now                              | Global shortcut possible? | Terminal window visible? | Learning cost |
|-------------|------------------------------------------------------|----------------------------|---------------------------|---------------|
| macOS       | Shortcuts.app                                        | Yes                        | No                        | Very low      |
| macOS       | Raycast / Alfred                                     | Yes                        | No                        | Low           |
| Windows     | PowerToys + .bat                                     | Yes                        | Usually no                | Low           |
| Windows     | AutoHotkey                                           | Yes                        | Configurable              | Medium        |
| Linux       | sxhkd / AutoKey                                      | Yes                        | No                        | Medium        |
| Any         | Tiny localhost server + browser extension            | Yes (via extension hotkey) | No                        | High          |

**Most people in similar situations (2024–2026) end up using option 1 or 2 + Raycast / PowerToys.**

If you tell me which operating system you're using (and whether you already use Raycast / Alfred / PowerToys / AutoHotkey), I can give you the exact 5–8 steps.

References:

- None required for this answer