---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Disabling VS Code Overwrite Mode
translated: false
type: note
---

In Visual Studio Code, the default behavior is **Insert mode** (typing inserts text, pushing existing text forward).
The **Replace mode** (typing overwrites existing text) is activated when you press the **Insert** key on your keyboard — this toggles between Insert and Replace/Overwrite mode.

### How to switch back from Replace (Overwrite) to Insert mode

1. Simply press the **Insert** key once on your keyboard.
   → The status bar at the bottom-right will change from **OVR** (Overwrite) to **INS** (Insert).

### If you never want to accidentally enter Overwrite mode again

You can disable the Insert key toggle completely:

#### Method 1: Keyboard shortcut (recommended)

Press `Ctrl + Shift + P` → type **"Toggle Insert/Overwrite"** → you’ll see the command
`Preferences: Toggle Insert on Paste and Overtype` or similar.
More reliably, use this direct setting:

#### Method 2: Add this to your `settings.json`

```json
// Disable Insert key from toggling overwrite mode
"editor.occurencesHighlight": true,
"editor.overtypeMode": false,

// This is the key one:
"keyboard.dispatch": "keyCode"
```

Actually the best and most common solution:

```json
// Completely disable the Insert key in VS Code
{
    "key": "insert",
    "command": "-editor.action.toggleOverwrite",
    "when": "editorTextFocus"
}
```

Or simply turn off overwrite globally:

```json
"editor.occurrencesHighlight": true,
"editor.overwriteMode": false   // not a real setting, ignore

// Real setting to disable overwrite toggle:
"editor.insertSpaces": true,  // unrelated

// Correct way:
{
    "key": "insert",
    "command": "noop"   // or remove the default binding
}
```

#### Simplest permanent fix (most people use this)

1. Open Settings (`Ctrl + ,`)
2. Search for **"overwrite"**
3. Uncheck **Editor: Overtype** (if it exists) or better:
4. Add this line to your `settings.json` (Ctrl + Shift + P → "Preferences: Open Settings (JSON)"):

```json
// Disable Insert key toggling overwrite mode entirely
{
    "key": "insert",
    "command": "-editor.action.toggleOverwrite"
}
```

After adding that, the Insert key will do nothing in VS Code, and you’ll always stay in Insert mode.

That’s the most common and reliable solution used by developers who keep hitting Insert accidentally (especially on laptops with small keyboards in Taiwan/Asia where Insert is easy to hit).

Let me know if you’re on macOS (uses different key) or want a status bar click solution!
