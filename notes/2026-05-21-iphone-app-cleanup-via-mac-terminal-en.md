---
audio: false
generated: true
image: false
lang: en
layout: post
title: iPhone App Cleanup via Mac Terminal
translated: false
type: note
---

Not connected yet, but once you plug in your iPhone, here's what we can do with the tools already on your Mac:

**Tools available**: `ideviceinstaller` (from libimobiledevice via Homebrew)

**Workflow to clean up iOS apps:**

1. **List all user-installed apps** — shows bundle IDs + names:
   ```bash
   ideviceinstaller -l -o list_user
   ```

2. **Uninstall unused apps** by bundle ID:
   ```bash
   ideviceinstaller -U com.example.unused-app
   ```

3. **Smart cleanup approach** — I can write a script that:
   - Lists all 200-300 apps from your iPhone
   - Cross-references with apps you haven't opened recently (unfortunately iOS doesn't expose last-used date via this API)
   - Presents them sorted/grouped for you to decide
   - Batch-deletes by category or individually

It does require **trusting this Mac** from your iPhone (the usual "Trust This Computer" prompt on first connect). Once that's done, I can drop the full list right in your terminal and let you pick which ones to nuke.

Want to plug it in so I can start?
