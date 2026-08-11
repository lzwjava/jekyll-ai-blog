---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clipboard Fix and Code Robustness
translated: false
type: note
---

Fixed. Both a system-level root cause fix and a code-level robustness fix:

## Root cause
The machine (Linux, Wayland/GNOME) had **no clipboard tool installed at all** — no `xclip`, `xsel`, or `wl-paste`. `pyperclip.paste()` failed, and the fallback in `note_queue.py` called `xclip`, which also doesn't exist → raw `FileNotFoundError` traceback.

## Fixes

**1. System fix — installed `wl-clipboard` without sudo** (root cause):
- Extracted `wl-clipboard` from an apt package into `~/.local/wl-clipboard`, symlinked `wl-paste`/`wl-copy` into `~/.local/bin` (already in your PATH, and `libwayland-client` was present).
- This fixes clipboard for the **entire project**, since pyperclip 1.11 supports `wl-paste` — all the other modules relying on `pyperclip.paste()` (`ww/main.py`, `create_note_utils.py`, `canvas_card.py`, `maps.py`, etc.) now work too. Verified round-trip copy/paste.

**2. Code fix — `ww/note/note_queue.py` `_get_clipboard()`**:
- Now tries native tools first in order: `wl-paste` (Wayland) → `xclip`/`xsel` (X11) → `pyperclip` as last resort, each with a 5s timeout.
- On total failure it raises a clear, actionable `RuntimeError` with install instructions instead of a `FileNotFoundError` traceback.

## Verified
- `uv run ww note` → `[ok] Queued (id=5c6306d7debc, 254 chars, ...)` ✅
- No-clipboard-tool scenario → clean `RuntimeError` with fix suggestions ✅
- Test queue entries cleaned up ✅

If you want `wl-clipboard` installed system-wide instead (survives regardless of PATH), run `sudo apt install wl-clipboard` — the current setup in `~/.local` works just fine though.