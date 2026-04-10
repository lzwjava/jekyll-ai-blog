---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ollama Launch Agent Disabled Summary
translated: false
type: note
---

Here's a review of what was done:

1. **Identified the service** — `launchctl list | grep -i ollama` found `com.ollama.ollama` registered as a launch agent.

2. **Located the plist file** — Searched standard locations (`~/Library/LaunchAgents`, `/Library/LaunchAgents`, `/Library/LaunchDaemons`). Found it bundled inside the app at `/Applications/Ollama.app/Contents/Library/LaunchAgents/com.ollama.ollama.plist`.

3. **Disabled the service** — Two commands:
   - `launchctl bootout` — attempts to stop the running service (failed with I/O error because it wasn't actively running, which is harmless)
   - `launchctl disable` — prevents it from auto-starting on future logins

4. **Verified** — `launchctl print-disabled` confirmed `com.ollama.ollama => disabled`.

**One thing noted:** There's also a `homebrew.mxcl.ollama` entry still marked as `enabled`. If you installed Ollama via Homebrew as well, that could also start it. Let me know if you want that disabled too.