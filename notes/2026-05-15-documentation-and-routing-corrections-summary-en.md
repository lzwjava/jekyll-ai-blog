---
audio: false
generated: true
image: false
lang: en
layout: post
title: Documentation and Routing Corrections Summary
translated: false
type: note
---

All working. Here's a summary of what was wrong and what was fixed:

**Issues found (documentation issue, not code bug):**

1. `ww image screenshot` was a duplicate of the top-level `ww screenshot` — same module, same functionality. Per your preference for top-level commands, the `image screenshot` route was redundant.

2. `ww image screenshot-linux` had no top-level shortcut, but should have one (`ww screenshot-linux`).

3. The help text said `--delay` (implying a flag), but the code uses `delay` as a **positional argument** `[DELAY]`.

**Changes made:**

- **main.py help text**: Removed `ww image screenshot` and `ww image screenshot-linux` from the Image section. Added `ww screenshot-linux` to the Screenshot section.
- **main.py routing**: Removed `screenshot` and `screenshot-linux` from the `image` group handler. Added top-level `screenshot-linux` route (next to existing `screenshot`).
- **README.md**: Moved screenshot entries out of the Image table into the Screenshot table as `ww screenshot [DELAY]` and `ww screenshot-linux`.