---
audio: false
generated: true
image: false
lang: en
layout: post
title: 24-Hour Server Access Report
translated: false
type: note
---

SSH connected and reviewed everything. Here's the full picture:

---

**Server running** since Jun 29 04:51 UTC (~24 hours), PID 3312, native nanoGPT checkpoint loaded. stdout pipes to `/workspace/fastapi.log` — logs are being kept.

**Access stats since publish (last ~24h):**

| Metric | Count |
| --- | --- |
| **Index page visits** (GET /) | 83 |
| **Chat completions** (POST /v1/chat/completions) | **54** |
| Legacy completions (POST /v1/completions) | 1 |
| Health checks (GET /health) | 1 |
| 404 junk (favicons, apple-touch-icons) | ~80 |
| 400 Bad Request (malformed client) | 2 |

**Unique "user" groups** (RunPod internal IPs) that hit the chat endpoint — these are proxy-mapped, so each group = ~1 real user:

- **100.64.1.99** — 12 completions (heaviest user)
- **100.64.1.98** — 9 completions
- **100.64.1.97** — 9 completions
- **100.64.1.101** — 8 completions
- **100.64.1.96** — 7 completions
- **100.64.1.100** — 7 completions
- Plus 127.0.0.1 (my own local test) and 100.64.1.33 (1 each)

So roughly **6 real users** actively tried the model. That's about right for a company WeChat group + internal share — people click, try a few prompts, explore.

**Also notable:**

- Someone crawled `/api/status?token=z9cgjolmphbkms0ui0je` 8 times from 5 different proxy IPs — looking for admin endpoints
- 2 requests returned 400 Bad Request — likely someone's API client sent bad JSON
- A Safari user hit `/README.md` with referer showing the RunPod proxy domain — someone read the docs

**Log retention:**

- `/workspace/fastapi.log` — 15KB, covers all requests since server start. Being kept.
- `/var/log/nginx/access.log` — tiny (only 15 entries), nginx logrotate is configured but nginx isn't the main ingress
- **No rotation on fastapi.log** — at 15KB after 24h it's fine, but for a live production-facing server you'd want logrotate or a restart-based split

Want me to add log rotation or a simple access counter to the index page?
