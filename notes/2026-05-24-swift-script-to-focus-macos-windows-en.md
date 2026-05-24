---
audio: false
generated: true
image: false
lang: en
layout: post
title: Swift Script to Focus macOS Windows
translated: false
type: note
---

Here's how it works, step by step:

**1. Listing all Ghostty windows**

I wrote a Swift script that uses macOS's `CGWindowListCopyWindowInfo` API from CoreGraphics. This is the same API that Activity Monitor uses to list windows. It returns metadata for every on-screen window — owner name, window title, position, size, and a unique `CGWindowID`.

```
swift -e '
import Cocoa
import CoreGraphics
// CGWindowListCopyWindowInfo enumerates all on-screen windows
// Filter by owner name == "ghostty"
// Extract: window ID, title, position, size
'
```

No special permissions needed — this is a read-only public API.

**2. Focusing a specific window by ID**

This is the harder part. The compiled script lives at `/tmp/focus_window`. It does:

```
Step 1: Look up the target window's bounds (x, y, width, height)
        using CGWindowListCopyWindowInfo filtered by window ID

Step 2: Activate the Ghostty app via NSRunningApplication.activate()
        (brings the app to front, but only the last-focused window)

Step 3: Calculate the center point of the target window

Step 4: Convert coordinates — CGWindowList returns "top-left origin"
        coordinates, but CGEvent uses Quartz coordinates (bottom-left origin).
        So: quartzY = screenHeight - clickY

Step 5: Post synthetic mouse events via CGEvent:
        - mouseMoved to the center
        - leftMouseDown
        - leftMouseUp
        This "clicks" the target window, which tells macOS to focus it.
```

**Limitations:**

- `CGEvent.post(tap: .cghidEventTap)` injects events at the HID level. It works, but it's a synthetic click — it will interact with whatever is at that screen position. If a popup or overlay is in the way, it gets clicked instead.
- If you grant **Accessibility** permissions to the process running this (Terminal or Hermes), I could use AppleScript via System Events (`tell process "ghostty" to set frontmost to true, perform action "AXRaise" of window N`), which is more precise — no synthetic clicks, just an accessibility command to raise a specific window.
- The Swift script needs to be compiled once (`swiftc`), which I did in `/tmp`. It's ephemeral — survives until reboot.

**What's on disk:**

| File | Purpose |
|------|---------|
| `/tmp/focus_window.swift` | Source — lists window bounds, activates app, clicks center |
| `/tmp/focus_window` | Compiled binary (macOS arm64) |
| `/tmp/raise_window.swift` | Simpler variant — just activates app, no click |

If you want this to be more robust, I could:
1. Install `cliclick` (`brew install cliclick`) — a tiny CLI for synthetic mouse/keyboard events, simpler than compiling Swift
2. Grant accessibility access so I can use AppleScript for clean window raising without clicks