---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacBook Disk Cleanup Summary and Breakdown
translated: false
type: note
---

Here's the full picture.

```
═══════════════════════════════════════════════════════════════
 DISK CLEANUP SUMMARY — MacBook Air M2
═══════════════════════════════════════════════════════════════

 BEFORE:  364 GB used / 460 GB  |  ~1 GB free  |  94% FULL  ⚠️
 AFTER:   364 GB used / 460 GB  |  60 GB free  |  86% used  ✓

 TOTAL FREED:  ~95 GB
═══════════════════════════════════════════════════════════════
```

WHAT WAS CLEANED (by size):

```
 SIZE     ITEM                          WHY IT WAS BIG
 ─────────────────────────────────────────────────────────────
 23 GB    .git tmp_pack files           10 abandoned git gc operations
          (lzwjava.github.io)           interrupted by sleep/kill over weeks.
                                        Pure dead weight — safe delete.

 21 GB    ~/.cache/huggingface/         Downloaded model weights:
          llama-7b-hf (13 GB alone)    bge-reranker, bce-embedding,
          gpt2, MiniLM, etc.           chatglm-6b, DeepSeek-R1.
                                        Re-download on demand.

  7 GB    ~/Library/Caches/JetBrains/  IntelliJ/PyCharm build caches,
                                        indexes, logs. Auto-regenerates.

  7 GB    ~/.npm/                       npm download cache from
                                        node projects. npm rebuilds it.

  5 GB    ~/.cache/torch/               PyTorch hub models (torch.hub.load
                                        downloads). Auto re-downloads.

  3 GB    ~/Library/Caches/Homebrew/    Downloaded formula bottles.
                                        brew redownloads as needed.

  3 GB    ~/.cache/pre-commit/          Pre-commit hook environments
                                        (virtualenvs per hook). pre-commit
                                        reinstalls on next run.

  3 GB    ~/Library/Caches/pip/         pip wheel/build cache.
                                        pip rebuilds on next install.

  1 GB    ~/.cache/uv/                  uv package cache.
                                        uv rebuilds on next sync.

  1 GB    ~/Library/Caches/LarkShell/   Lark/Feishu desktop cache.
```

WHAT STILL TAKES SPACE (actionable):

```
 SIZE     ITEM                          WHAT TO DO
 ─────────────────────────────────────────────────────────────
 35 GB    lzwjava.github.io .git/       Run `git gc --aggressive` to
          (23 packs, 29.5M objects)     repack into 1 compact pack.
          Still bloated for 1666        May save 5-10 GB more.
          commits. Likely has
          large binaries in history.

 37 GB    ~/Library/Containers/         WeChat alone is 19 GB (chat
          WeChat 19 GB                  history, media, caches).
          Docker 8 GB                   Open WeChat → Settings →
          QQ 4.5 GB                     Storage → Manage → Clear.
          Teams 1 GB                    Docker: docker system prune -a
          Slack 860 MB

 11 GB    ~/Library/Caches remaining    ms-playwright, go-build,
          (after cleanup)               vscode-cpptools, camoufox,
                                        Spotify, Cypress. Lower priority.

 58 GB    ~/projects/ (not .git)        Qwen2.5-Coder (3.4 GB),
          jekyll-ai-blog (3 GB),
          blog-assets (2.3 GB),
          jdk (2.4 GB), etc.
                                        Audit: do you still need all
                                        cloned repos on Air?

  5 GB    ~/Library/Application Sup/    JetBrains 5.4 GB (plugins,
          nomic.ai 3.5 GB               local models?). nomic.ai is
          Steam 1.4 GB                  likely local embedding models.
          Discord 1.2 GB
```

WHAT WAS PRESERVED (not touched):

```
 ✓ All project source code
 ✓ All app data and configs
 ✓ Git repos (working trees intact)
 ✓ ~/Documents, ~/Desktop, ~/Downloads
 ✓ All application containers (WeChat, Docker, etc.)
 ✓ HuggingFace auth tokens
 ✓ All environment configs (.env, .zshrc, etc.)
```

REMAINING QUICK WINS (if you want more):

```
 1. git gc --aggressive on lzwjava.github.io     ~5-10 GB
 2. WeChat storage cleanup (app settings)        ~10-15 GB
 3. Docker prune (if not using on Air)           ~8 GB
 4. Delete stale repos you don't use on Air      ~20+ GB
```

Want me to tackle any of these?
