---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ghostty Commands and AXDocument Access
translated: false
type: note
---

## Summary

### What was built

Added `ww ghostty list` and `ww ghostty focus` commands to the `ww` CLI tool.

### `ww ghostty list`

Lists all Ghostty windows with ID, title, position, and size. Now also shows **hermes project names** using the `AXDocument` accessibility attribute — each Ghostty window exposes its working directory via `kAXDocumentAttribute`, which we read through AXUIElement (requires Accessibility permissions).

Current output:

```
 #      Window ID  Title                                    Position         Size
    2. [1605]  hermes [openwrt]                         (28,224)         760x533
    3. [3172]  hermes [ww]                              (503,90)         760x533
    5. [3790]  hermes [jekyll-ai-blog]                  (682,119)        760x533
    6. [6313]  hermes [hermes-agent]                    (260,132)        995x699
    ...
```

### `ww ghostty focus <N|title>`

Scales a Ghostty window to near-full-screen using `CGSSetWindowTransform` (SkyLight private API). Also supports `ww ghostty focus reset` to restore all windows.

### Key discovery: `AXDocument`

The breakthrough was finding that Ghostty exposes each terminal tab's working directory as the `kAXDocumentAttribute` on its AXUIElement window. This lets us match "hermes" windows to their project directories without any process tree matching.

### Minor issues to clean up

1. **Window 1** (`[1544]` at 84x77) is a small popup/notification — should be filtered out
2. **Windows 17-18** (position 526,139) don't show projects — they appear to be off-screen or minimized, so AXUIElement doesn't return their `AXDocument`
3. **Window 7** shows `hermes  [ww]` with an extra space (original title is "hermes " with trailing space)

### Files changed

- `/Users/lzwjava/projects/ww/ww/ghostty/list_windows.py` — CGWindowList + AXUIElement AXDocument
- `/Users/lzwjava/projects/ww/ww/ghostty/focus.py` — CGSSetWindowTransform scaling
- `/Users/lzwjava/projects/ww/ww/main.py` — dispatch + help text

### Approaches tried and discarded

| Approach | Why it failed |
| ---------- | -------------- |
| CGEvent mouse click | Unreliable with overlapping windows |
| CGEvent keyboard (Cmd+`) | Silent drop on macOS 26.5 |
| CGSOrderWindow | CGWindowList z-order doesn't update |
| SLSMoveWindow / SLSGetWindowBounds | Segfault on macOS 26.5 |
| Process tree TTY matching | Can't map TTY to window ID |
| Idle time / atime detection | Too coarse, doesn't change on focus |
| S+ foreground marker | Per-terminal, not global focus |

Want me to clean up the minor issues and commit?
