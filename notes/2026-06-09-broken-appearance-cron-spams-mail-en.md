---
audio: false
generated: true
image: false
lang: en
layout: post
title: Broken Appearance Cron Spams Mail
translated: false
type: note
---

Here's the full picture:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 SYSTEM CRONTAB (crontab -l)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  */10 * * * *  /opt/homebrew/bin/ww appearance smart-auto
  0 * * * *     /opt/homebrew/bin/ww projects update

  Two jobs: appearance check every 10 min, git pull every hour.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ww projects update — WORKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  - Config: 148 repos across 8 categories (ai-models, ai-training, ai-inference, ai-apps, ai-agents, dev-tools, infra-network, web-platforms)
  - 2 repos missing locally: TensorRT-LLM, rocBLAS (skipped cleanly)
  - Latest run just now: 134 current, 12 updated, 0 failed (27.9s)
  - Top updates: hermes-agent (265 commits), warp (3), langfuse (1), desktop (15)
  - Previous run (from mail): 118 current, 26 updated, 2 failed (hermes-agent + desktop — transient, resolved now)

  Verdict: The hourly cron is doing real work — pulling real upstream changes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 MAIL — 163 CRON EMAILS (mostly errors)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  140 × "appearance smart-auto" — BROKEN (96% failure rate)
  23 × "projects update" — normal output (success emails)

  The appearance job is spamming your mailbox every 10 minutes with:

    FileNotFoundError: [Errno 2] No such file or directory: 'imagesnap'

  Root cause: cron runs with PATH=/usr/bin:/bin — doesn't include
  /opt/homebrew/bin where imagesnap lives. The binary IS installed:

    /opt/homebrew/bin/imagesnap

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FIX NEEDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Two options:

  1. Use full path in crontab (cleanest):
     Change the appearance line to:
     PATH=/opt/homebrew/bin:/usr/bin:/bin
     */10 * * * * /opt/homebrew/bin/ww appearance smart-auto

  2. Or add PATH directive at top of crontab:
     PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin

  Want me to fix the crontab? Also want me to clear the 163 accumulated cron emails from /var/mail/lzwjava?

  Hermes cron: 0 jobs (you're using system crontab instead).
