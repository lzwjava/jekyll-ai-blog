---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix for Angular CLI Shell Hang
translated: false
type: note
---

Done. Here's the summary:

**Root cause:** `source <(ng completion script)` in ~/.zshrc line 23. Angular CLI's `ng completion script` outputs the completion text correctly but the Node process never exits — it hangs forever. Every new Ghostty tab (or any terminal) was waiting 60s+ for this to finish.

**Fix applied:**
1. Saved the completion script statically to `~/.ng-completion.zsh`
2. Replaced the dynamic `source <(ng completion script)` with `source ~/.ng-completion.zsh`

**Result:** Shell startup went from **60s+ → 0.25s**. Open a new Ghostty tab and it should be instant now.

Note: If you add new Angular CLI commands and need updated completions, just re-run `timeout 5 ng completion script > ~/.ng-completion.zsh` (the completions rarely change).
