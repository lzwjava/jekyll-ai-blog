---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dock Pinned and Running Apps Overview
translated: false
type: note
---

Done. Here's what was added:

  Created: /Users/lzwjava/projects/ww/ww/macos/dock.py
  Modified: /Users/lzwjava/projects/ww/ww/main.py

`ww macos dock` reads the Dock plist (~Library/Preferences/com.apple.dock.plist) and shows all pinned apps with:

  - Numbered list of all Dock apps
  - Bundle identifier for each
  - ● marker for currently running apps (via osascript System Events)
  - --json flag for structured output

Your Dock has 9 apps: Safari, Ghostty, Telegram, Zed, Microsoft To Do, GitHub Desktop, WeChat, Passwords, System Settings — 6 of them running right now.