---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Plugin Not Enabled Fix
translated: false
type: note
---

**Problem:** `/note` command returns "Unknown command: /note" in Hermes CLI.

**Investigation:**

1. Plugin source exists at two locations:
   - `~/projects/config/hermes/plugins/note/` (config repo)
   - `~/.hermes/plugins/note/` (Hermes plugins dir)
   - Both are identical (diff shows no difference)

2. Plugin files are valid:
   - `plugin.yaml` — correct manifest (name, version, description)
   - `__init__.py` — has proper `register(ctx)` function that calls `ctx.register_command("note", ...)`
   - Handler saves last assistant response as markdown note via `ww.note.create_note_from_clipboard`
   - Supports args: `[number] [--title <title>] [--dir <dir>]`
   - Auto git commits + pushes after saving

3. Plugin discovery is fine — files are in `~/.hermes/plugins/note/` where Hermes looks

4. **Root cause:** `plugins.enabled: []` in `~/.hermes/config.yaml` — empty list means no plugins load, even if correctly installed

**Fix:** Changed `plugins.enabled: []` → `plugins.enabled: [note]` in `~/.hermes/config.yaml`. Requires Hermes restart to take effect.

**Key takeaway:** Hermes plugin system requires two things: (1) plugin files in `~/.hermes/plugins/<name>/`, and (2) the name listed under `plugins.enabled` in config.yaml. Missing step 2 = plugin silently ignored.
