---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Throttling Fixed via Mirror
translated: false
type: note
---

Fetch completed instantly. Let me now give you the full analysis.

Here's what I found:

== ROOT CAUSE ==

The slowness is NOT ncat or the proxy. It's China→GitHub ISP throttling.

Speed tests:
  Direct to GitHub:         33 KB/s
  Via Hysteria2 proxy:      59 KB/s
  Via ghfast.top mirror:    2.4 MB/s  (70x faster)

Both direct and proxied paths are throttled by Chinese ISPs. The Hysteria2 proxy (DMIT LA) doesn't help because the bottleneck is the last-mile China exit, not the proxy itself.

== NCAT SOURCE CODE ==

Found at /Users/lzwjava/projects/nmap/ncat/

ncat_connect.c lines 621-921: `do_proxy_socks5()` — standard SOCKS5 handshake, no performance issues.
ncat.h line 140: `#DEFAULT_TCP_BUF_LEN = 8192` (8KB relay buffer) — adequate for throughput.
ncat_posix.c: relay loop uses select() + 8KB reads — not the bottleneck.

ncat is clean. The problem is the network path.

== SOLUTION APPLIED ==

Changed Qwen2.5-Coder remote to use ghfast.top GitHub mirror:
  https://ghfast.top/https://github.com/QwenLM/Qwen2.5-Coder.git

Fetch now completes instantly.

NOTE: Repo has 296 local commits ahead of upstream (looks like a fork merge history). You may want to rebase or reset:
  git rebase origin/main     # preserve local commits
  git reset --hard origin/main  # discard local commits

== FOR ALL GITHUB REPOS ==

To apply globally (all GitHub repos use ghfast.top):
  git config --global url.https://ghfast.top/https://github.com/.insteadOf https://github.com/

Or per-repo only. Note: pushes won't work through the mirror — you'd need to temporarily override for push:
  git push https://github.com/... main

Want me to set up the global config?
