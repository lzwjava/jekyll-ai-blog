---
audio: false
generated: true
image: false
lang: en
layout: post
title: ZSH Completion for CLI Tool
translated: false
type: note
---

Here's the full summary:

What was built:

1. Completion script: /Users/lzwjava/projects/ww/completions/_ww
   - 476 lines of zsh completion code
   - Covers all 33 top-level command groups
   - Covers all subcommands for each group (github, git, macos, image, proc, utils, java, network, search, pdf, copilot, sync, read, llm, openrouter, env, display, degree, whisper, host, linux, cloudflare, ghostty, clash, latest, note, screenshot)
   - Covers nested sub-subcommands (e.g. sync bashrc back/forth, sync hermes back/forth)
   - Covers flags (--no-push, --only-message, --json, --days, --model, --debug, --top-k, --pages, --dir, --type)
   - Covers file completions where appropriate (whisper -> audio files, marp/pdf -> .md files, read index -> directories)

2. CLI commands added to ww/main.py:
   - `ww completion install` — copies _ww to ~/.zsh/completions/ and prints setup instructions
   - `ww completion script` — prints the completion script to stdout
   - Help text updated with "Completion:" section

3. Shell configuration:
   - Added `fpath=(~/.zsh/completions $fpath)` and `autoload -Uz compinit && compinit` to ~/.zprofile (line 70-72)
   - Also present in ~/.zshrc (line 24-25) for non-Ghostty terminals
   - .zprofile is the one that matters — Ghostty sources it on startup

4. Files changed:
   - ww/main.py — added completion handler + help text
   - completions/_ww — new zsh completion script
   - ~/.zprofile — added fpath + compinit

Git: committed as 1eed8fc on main, pushed to origin.

To verify after restarting Ghostty:
  ww <TAB>           → shows all 33 command groups
  ww github <TAB>    → shows info, repos, starred, followers, following, notifications, rate, gitmessageai
  ww git <TAB>       → shows amend-push, classify, find-commit, delete-commit, diff-tree, ...
  ww sync bashrc <TAB> → shows back, forth
  ww clash <TAB>     → shows select-provider, speed, run, top-proxies, ...
  ww github gitmessageai <TAB> → shows --no-push, --only-message, --allow-pull-push, --type
