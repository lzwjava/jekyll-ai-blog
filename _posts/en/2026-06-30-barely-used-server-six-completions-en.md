---
audio: false
generated: true
image: false
lang: en
layout: post
title: Barely Used Server, Six Completions
translated: false
type: note
---

The server is running but barely used. Here's the English summary:

**Server**: SEC-EDGAR-GPT — 124M nanoGPT (`/workspace/model/server.py`) listening on port 8888. Started at 05:59 UTC today (restarted ~7 hours ago).

**Real completions served (6 total since restart)**:

1. `05:28:33` — "What risk factors are disclosed in 10-K filings?" → 1000 tokens, 21.3s. From browser via code-server (your test).
2. `05:51:23` — "What legal proceedings in Amazon's SEC filing?" → 200 tokens, 1.3s. iPhone via WeChat browser → your 8888 URL.
3. `06:00:31` — "Test headers logging" → 1000 tokens, 21s. From browser via code-server (your test).
4. `06:42:12` — Same Amazon question again → 200 tokens, 1.3s. iPhone WeChat, CF IP 69.63.219.52.
5. `11:53:35` — "Microsoft revenue segments" → 200 tokens, 1.28s. Mac Safari → 8888 URL, CF IP 69.63.219.52.
6. `11:53:43` — Amazon question again → 200 tokens, 1.32s. Same Safari session.

**What this tells you**:

- The iPhone + WeChat browser request at 06:42 from the 8888 URL — someone clicked a link you shared (probably WeChat/朋友圈). They asked one question and left.
- The 11:53 Safari requests from CF IP 69.63.219.52 could be you testing from another network or someone else on the same carrier NAT.
- Everything else was you testing from the code-server browser (8081 localhost).

**Background noise** (all 404s, no real users):

- Runpod internal IPs (100.64.1.x) polling `/robots.txt`, `/sitemap.xml`, `/favicon.ico`, `/apple-touch-icon.png`
- Some requests to `/api/status?token=z9cgjolmphbkms0ui0je` — monitoring scripts looking for an API status endpoint that doesn't exist

**Verdict**: Very light usage. You + maybe one curious person from WeChat. No sustained traffic.
