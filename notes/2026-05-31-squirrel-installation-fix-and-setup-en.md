---
audio: false
generated: true
image: false
lang: en
layout: post
title: Squirrel Installation Fix and Setup
translated: false
type: note
---

The brew cask already fetched the file (v1.1.2) but failed on `sudo`. I can't enter your macOS password from the agent. Here's the two-line install you need to run in your own terminal:

```
brew install --cask squirrel
```

It will prompt for your macOS password — that's normal for `.pkg` installers.

If brew already cached it and refuses to re-download, clear the cache first:

```
brew reinstall --cask squirrel
```

After install:

1. **Log out and log back in** (or restart) — macOS needs a fresh login to pick up the new input method.
2. Go to **System Settings → Keyboard → Text Input → Edit** → click `+` → find "Squirrel" (鼠须管) → add it.
3. Press `Ctrl+`` or click the input method icon in the menu bar to switch to Squirrel.

Then I'll help you configure double pinyin and the rime-ice dictionary. Want me to set up the config files once Squirrel is installed?
