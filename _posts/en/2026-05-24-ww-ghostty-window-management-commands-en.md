---
audio: false
generated: true
image: false
lang: en
layout: post
title: WW Ghostty Window Management Commands
translated: false
type: note
---

## Comprehensive Summary

### What was built

Added two new commands to `ww ghostty`:

| Command | Description |
|---------|-------------|
| `ww ghostty list` | List all open Ghostty windows with ID, title, position, size |
| `ww ghostty focus <N\|title>` | Scale a Ghostty window to near-full-screen by index or title substring |
| `ww ghostty focus reset` | Reset all window transforms back to original size/position |

### Files created

- `/Users/lzwjava/projects/ww/ww/ghostty/list_windows.py` — CGWindowList enumeration via Swift inline code
- `/Users/lzwjava/projects/ww/ww/ghostty/focus.py` — CGSSetWindowTransform to scale+reposition windows

### Files modified

- `/Users/lzwjava/projects/ww/ww/main.py` — added `list` and `focus` dispatch in the ghostty section + help text

### How `list` works

Uses `CGWindowListCopyWindowInfo` (CoreGraphics, no permissions needed) to enumerate on-screen Ghostty windows. Swift code runs via `swift -e`, parses tab-separated output, formats a table:

```
#      Window ID  Title                                    Position         Size
    1. [6419]  hermes                                   (220,203)        760x533
    2. [3932]  lzw@to: /mnt/data/deepseek-v4-inference  (43,177)         995x699
```

### How `focus` works (final version)

Uses `CGSSetWindowTransform` from the SkyLight private framework. This applies a 2D affine transform to the window — scaling it up and translating it to fill the primary display (with small padding and menu bar offset). No keyboard focus is stolen; the current terminal keeps input focus.

### Approaches tried and discarded

1. **CGEvent mouse click** — unreliable when windows overlap (click hits the wrong window). Also requires Screen Recording permission on macOS Sequoia+.

2. **AXUIElement (Accessibility API)** — returns error -25211 ("not trusted"). Requires the terminal app to be granted Accessibility permission in System Settings > Privacy & Security > Accessibility.

3. **AppleScript / System Events** — same -25211 error without Accessibility.

4. **CGEvent keyboard (Cmd+\`)** — events post without error but don't reach Ghostty (silent drop on macOS 26.5, likely Sequoia security restriction).

5. **CGSOrderWindow** — didn't crash but CGWindowList z-order didn't update, and no way to verify visual result.

6. **SLSMoveWindow / SLSGetWindowBounds / CGSMoveWindow** — all segfault on macOS 26.5. The SkyLight internal signatures have changed or require entitlements that aren't available without SIP modification.

7. **SLSSetWindowShape** — crashes (expects CGSRegionRef, not CGRect).

### What works on macOS 26.5

| API | Status | Purpose |
|-----|--------|---------|
| `CGWindowListCopyWindowInfo` | ✅ works | List/enumerate windows |
| `CGSSetWindowTransform` | ✅ works | Scale + translate window visually |
| `CGSOrderWindow` | ✅ works (no visual z-order change in CGWindowList) | Raise window to front |
| `SLSSetWindowLevel` | ✅ works | Change window level |
| `NSWorkspace.shared.runningApplications` | ✅ works | Find/activate apps |

### Limitations of current approach

- `CGSSetWindowTransform` is a **visual transform** — the window's backing store stays the same size, but it's rendered scaled. Text appears larger.
- Cannot programmatically resize the actual window bounds without Accessibility permissions or working CGS move/resize APIs.
- The `reset` command resets the transform but won't restore the window if it was manually resized after scaling.