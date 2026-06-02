---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Stale OpenClaw Plugin Entries
translated: false
type: note
---

Two ways to fix this:

**Option 1 — Auto-clean with doctor (recommended):**

```
openclaw doctor --fix
```

This removes the stale `brave` entries from config (`plugins.entries.brave` + `plugins.installs.brave`). It won't reinstall, just cleans up.

**Option 2 — Reinstall:**

```
openclaw plugins install @openclaw/brave-plugin
```

Use this if you actually want the Brave plugin back. If the package doesn't exist on npm, this will fail — in which case Option 1 is the right path.

**Root cause:** The brave plugin's package directory (`/home/lzw/.openclaw/npm/node_modules/@openclaw/brave-plugin`) was missing when the update tried to verify it. OpenClaw attempted auto-recovery but it failed (likely the package doesn't exist on npm). The config still holds the stale entry, hence the repeated warning.

After running `doctor --fix`, also remove the redundant `plugins.load.paths` entry it warns about — that can be done in the same run.
