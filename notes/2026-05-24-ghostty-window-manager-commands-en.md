---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ghostty Window Manager Commands
translated: false
type: note
---

Done. Two new commands added:

```
ww ghostty list         # List all open Ghostty windows with ID, title, position, size
ww ghostty focus <N>    # Focus window by index (e.g. 7) or title substring (e.g. "deepseek")
ww ghostty focus        # No arg = list windows + usage hint
```

Files created:
- /Users/lzwjava/projects/ww/ww/ghostty/list_windows.py — CGWindowList enumeration via Swift
- /Users/lzwjava/projects/ww/ww/ghostty/focus.py — CGEvent mouse click to raise a window

Files modified:
- /Users/lzwjava/projects/ww/ww/main.py — dispatch + help text

How it works:
- `list` uses `CGWindowListCopyWindowInfo` (no Accessibility permissions needed) to enumerate all Ghostty windows
- `focus` activates the Ghostty app, then posts a CGEvent mouse click at the center of the target window's bounds to raise it. Supports both 1-based index and case-insensitive title substring matching