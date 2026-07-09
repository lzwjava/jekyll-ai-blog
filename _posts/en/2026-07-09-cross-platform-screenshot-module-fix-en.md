---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross-Platform Screenshot Module Fix
translated: false
type: note
---

Fixed. No `--linux` flag needed — the platform is auto-detected.

**What was changed in `ww/image/screenshot.py`:**

1. **Lazy Quartz import** — `import Quartz` moved inside `sys.platform == "darwin"` branch instead of module top-level. This was the crash: Python tries to import all top-level names when the module is loaded, and `Quartz` (pyobjc) doesn't exist on Linux.

2. **`capture_screenshot()` now works on Linux** — falls back to `_capture_linux()` which tries scrot → ImageMagick `import` → gnome-screenshot → spectacle → ffmpeg x11grab. Same tool search order as `screenshot_linux.py`.

3. **`main()` description updated** — now says "macOS / Linux" instead of just "macOS".

**Result:**
- `ww screenshot interact-note` → imports `capture_screenshot` without crashing
- `ww screenshot` (no subcommand) → also works on Linux now
- `ww screenshot-linux` (the separate command with `--no-save`/`--area`) kept as-is — it has extra clipboard/quadrant features

The test showed the screenshot capture working (ImageMagick `import` via DISPLAY=:1), and the LLM step only failed because `OPENROOTER_API_KEY` isn't set on this cloud box — not a code issue.

Want me to save this cross-platform pattern as a skill?