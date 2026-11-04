---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pushed all with concurrent commits
translated: false
type: note
---

All pushed. GitHub `main` is now at `f5e6401b3`, working tree clean.

What went up (in order):
1. `5ca3c4aa9` — `fix(ci)`: patch-less Python version (previous task)
2. `045c8466f` — `fix(build)`: remove duplicate posts/marp collisions *(not mine — appeared in the history concurrently)*
3. `62d9ef190` — `fix(style)`: dark-mode DeepWiki pill specificity fix
4. `f5e6401b3` — `feat(home)`: notes as front page *(not mine — a concurrent process committed this on top of mine)*

Heads-up on the last two: **another process (or a second session) is actively committing to this repo** — `045c8466f` and `f5e6401b3` weren't made by me, and I pushed them along as part of "push all." If that concurrent work shouldn't have gone up yet, let me know and I can help sort it out. Also, still pushing via the HTTPS + `HTTP/1.1` workaround since SSH through your proxy keeps getting MITM'd — consider `git config --global http.version HTTP/1.1` to make this permanent (I can apply it for you).
