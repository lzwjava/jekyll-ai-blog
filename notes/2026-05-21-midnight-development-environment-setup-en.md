---
audio: false
generated: true
image: false
lang: en
layout: post
title: Midnight Development Environment Setup
translated: false
type: note
---

Here's a full picture of what you've been up to over the last ~2 hours (midnight to 1am) on this Linux Mint 22.3 machine:

---

## Software Installed

**Ghostty 1.3.1** — terminal emulator, installed from `ppa:mkasberg/ghostty-ubuntu` via apt. GPU-accelerated GTK4 terminal with 350+ built-in themes. Auto-updates via apt going forward.

**VS Code 1.121.0** — added Microsoft's official apt repo, installed via apt. ~726 MB on disk. Already came with 54 pre-installed extensions including full Python, Java, C/C++, Rust, Go, Kotlin, PHP support plus Raspberry Pi Pico / embedded MCU toolchains.

**GitHub Desktop 3.4.13-linux1** — installed via `dpkg -i` from the shiftkey fork's `.deb`. This is the de facto Linux port since there's no official GitHub Desktop for Linux. Binary at `/usr/bin/github-desktop`.

---

## System Configurations

**Caps Lock ↔ Left Ctrl swap** — cleaned up from a broken `~/.Xmodmap` (keysym-based, didn't work). Rewrote it with keycode-based rules. Added `~/.xprofile` as a fallback with `setxkbmap -option ctrl:swapcaps`. Both methods now agree.

**Hermes YOLO mode** — set `approvals.mode: off` in `~/.hermes/config.yaml` so you don't get prompted for every command approval.

---

## Hermes / LLM Fixes (in your `ww` project)

**Reasoning model token limit** — DeepSeek v4 Flash is a reasoning model; `max_tokens=60` was too small (reasoning consumed the whole budget). Bumped to 300 in:

- `ww/note/create_note_utils.py`
- `ww/note/screenshot_log.py`

**Enhanced LLM error diagnostics** — added proxy connectivity checking and richer error messages to `ww/llm/openrouter_client.py` so empty-content responses and non-200 errors include the model name, max_tokens, finish_reason, and proxy status.

---

## Misc

- Read a Wang Yin (王垠) Weibo essay comparing MITM attacks to organizational dysfunction — saved as a note.
- `.gitignore` cleanup: some churn with reverts, but ended up keeping the original rules plus `.env`.

---

### What's Essential Now

1. **Test `ww note`** — it should work with the token limit fix. Give it a try.
2. **Ghostty config** — you have the terminal installed but no config file yet. Its config lives at `~/.config/ghostty/config` if you want to pick a theme, font, or opacity.
3. **GitHub Desktop** — launch it once with `github-desktop`, sign in with OAuth, and clone a repo to verify the keychain integration works.
4. **VS Code extensions** — with 54 pre-installed extensions, you might want to audit what's actually useful vs cruft, especially if some are duplicates or out of date.

Want me to look at any of these, or set up anything else?
