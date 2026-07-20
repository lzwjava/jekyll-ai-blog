---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix infinite moderation retry loop
translated: false
type: note
---

Syntax is clean. Here's what the fix does:

**Problem**: `_openrouter_image` in `ww/gen_video/video.py` had an unbounded recursive retry loop — when moderation blocked an image prompt, it sanitized the prompt and called itself. If the sanitized version also got moderated, it retried infinitely (you saw ~40+ retries before hitting Ctrl-C).

**Fix**: Added a `retry_count` parameter (default 0) and `MAX_RETRIES = 3` cap. After 3 failed attempts, it prints "Moderation blocked after 3 retries — giving up" and returns `[]`, which causes the scene to fall through to a dark placeholder image instead of looping forever.

Also fixed the file structure that was corrupted from the first patch attempt (the function was nested inside `_openrouter_chat`). Both functions are now standalone at module level where they belong.
