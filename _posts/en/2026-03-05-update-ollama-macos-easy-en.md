---
audio: false
generated: true
image: false
lang: en
layout: post
title: Update Ollama on macOS Easily
translated: false
type: note
---

**On macOS, updating Ollama is usually very straightforward** because the official installation includes automatic updates.

### Most common & recommended way (official .dmg / App install)

1. Look for the **Ollama icon** in your menu bar (top right of the screen, near the clock, Wi-Fi, battery icons etc.).
   It usually looks like a little blue Ollama logo or a stylized "O".

2. Click the Ollama menu bar icon

3. If an update is available you'll typically see something like:
   - "Update available"
   - "Restart to update"
   - "Install update"
   or similar wording

4. Click **"Restart to update"** (or the equivalent button)
   → Ollama will quit and relaunch with the new version automatically.

This is the method officially recommended in the Ollama docs (as of 2026).

### Alternative: Force a manual update / fresh install

- Go to → https://ollama.com/download
- Download the latest **Ollama.dmg** for macOS
- Open the .dmg file
- Drag the new Ollama.app → /Applications/ (replace the old one when asked)
- Launch Ollama again

Your models and configuration stay safe (they live in `~/Library/Application Support/Ollama` or `~/.ollama`).

### Quick version check

Open Terminal and run:

```bash
ollama --version
# or
ollama -v
```

After updating you should see a newer version number.

### Notes / less common cases

- **If you installed via Homebrew** (`brew install ollama` or `brew install --cask ollama`):
  → `brew upgrade ollama` or `brew upgrade --cask ollama`
  (most people use the official .dmg installer though, not Homebrew)

- No automatic update icon?
  → Make sure Ollama is running in the background
  → Or just do the manual .dmg reinstall (very safe)

That's basically it — macOS users usually get the easiest update experience among all platforms. 😄

Let me know if you don't see the menu bar icon or get any specific error!
