---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Resuming Suspended Jobs in zsh
translated: false
type: note
---

To resume a suspended job (like your `bundle exec jekyll serve --incremental` command, which was likely paused with Ctrl+Z) in zsh within Ghostty, follow these steps in the same terminal session:

1. List all background/suspended jobs to confirm it's there:
   ```
   jobs
   ```
   This will show something like `[1]+  Suspended  bundle exec jekyll serve --incremental`.

2. Resume it in the foreground (it'll take over your terminal again):
   ```
   fg
   ```
   - If you have multiple jobs, specify the one you want with `fg %1` (replacing `1` with the job number from the `jobs` output).

If you want to run it in the background instead (so you can use the terminal for other things while it serves), use `bg %1` (again, with the job number).

Once resumed, Jekyll should pick up where it left off, assuming no major interruptions. If the process seems stuck or errors out, you might need to kill it with `kill %1` and restart.
