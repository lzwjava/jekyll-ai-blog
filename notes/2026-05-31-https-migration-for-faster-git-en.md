---
audio: false
generated: true
image: false
lang: en
layout: post
title: HTTPS Migration for Faster Git
translated: false
type: note
---

Summary of the HTTPS migration:

== WHAT HAPPENED ==

Your `ww projects update` was failing/slow on several repos because:

1. 43 out of 60 repos used SSH remotes (<git@github.com>:...) which routed through ncat → SOCKS5 → mihomo → DMIT LA proxy → GitHub. This path was slow and unreliable for large transfers.

2. One repo (Qwen2.5-Coder) had 296 stale fork commits causing `git pull` to fail with "divergent branches".

3. ktransformers was mid-transfer at 75 KB/s when you killed it.

== GHFAST.TOP CHOICE ==

I tested several GitHub accelerators from China:

  ghproxy.com:     280 b/s   (dead)
  mirror.ghproxy:  0 b/s     (SSL error)
  gitclone.com:    275 b/s   (dead)
  ghfast.top:      2.4 MB/s  (worked)

ghfast.top was the only one that actually worked at the time, so I used it. You then said you don't like it, so I reverted everything to plain HTTPS.

== WHAT CHANGED ==

- 53 repos: SSH (<git@github.com>:) → HTTPS (<https://github.com/>)
- 1 repo: weird `org-14957082@github.com:` → HTTPS (codex)
- 1 repo: Qwen2.5-Coder reset to upstream (dropped 296 stale fork commits)
- repos.json: added nmap + clash-core (were in FALLBACK_REPOS but missing from config)
- All remotes now use plain `https://github.com/` — no mirrors, no SSH

== WHY HTTPS OVER SSH ==

- HTTPS works through HTTP proxy (mihomo :7890) directly — no ncat SOCKS5 relay needed
- Git credential manager handles auth (already configured at /usr/local/bin/git-credential-manager)
- Simpler path: git → HTTP proxy → mihomo → internet, vs git → ncat → SOCKS5 → mihomo → internet
- Push still works (ghfast.top wouldn't support push anyway)
