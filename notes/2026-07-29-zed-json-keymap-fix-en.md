---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed JSON Keymap Fix
translated: false
type: note
---

That was the problem — `// comments` are not valid in JSON. The file is now valid JSON and should work.

Here's the clean version:

**`~/.config/zed/keymap.json`**

```json
[
  {
    "context": "Editor && vim_mode == false",
    "bindings": {
      "ctrl-x ctrl-left": "editor::GoBack",
      "ctrl-x ctrl-right": "editor::GoForward",
      "ctrl-x left": "editor::GoBack",
      "ctrl-x right": "editor::GoForward",
      "alt-left": "editor::GoBack",
      "alt-right": "editor::GoForward"
    }
  }
]
```

Zed should pick it up immediately (no restart needed). After **Alt+click** to jump to a definition:

| Press | Action |
| --- | --- |
| `Ctrl+x ←` | Go Back (back to where you were) |
| `Ctrl+x →` | Go Forward |
| `Alt+←` | Go Back (alternative) |
| `Alt+→` | Go Forward (alternative) |

If you still see errors, try opening Zed's command palette (`Cmd+Shift+P`) and run **"zed: open default keymap"** to check the exact command names — they're case-sensitive.
