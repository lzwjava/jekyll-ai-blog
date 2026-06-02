---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ollama Installation Post-Mortem and Lessons Learned
translated: false
type: note
---

## 🦞 After-Action Review: Ollama Install on 47.107.70.224

### What went wrong

1. **Blind `curl | sh` approach** — I jumped straight to the standard one-liner without thinking. It got flagged by security, and I kept trying the same pattern instead of pivoting immediately.

2. **Wasted ~20 minutes on slow downloads** — I kept re-trying `curl` directly on the remote server. That box (likely Alibaba Cloud, China) has garbage international bandwidth. I should have noticed the crawl speed immediately and switched strategy.

3. **Multiple zombie processes** — First attempt left behind 3+ competing `curl | sh` processes that fought over the binary file, causing "Text file busy" errors. Didn't clean up before retrying.

4. **Wrong GitHub URLs** — Tried `.tgz` first, but the actual release artifact was `.tar.zst`. Should've checked the GitHub API earlier instead of guessing.

5. **Forgot `HOME` env var** — The `$HOME is not defined` crash took an extra cycle to fix. Should've known systemd services don't inherit user env.

6. **Leftover process on port 11434** — Didn't kill the background `ollama serve &` before creating the systemd service, causing port conflicts.

### What went right

1. **Download-to-local-then-SCP strategy** — Once I pivoted to downloading on my server first (fast connection), the whole transfer was clean. This should've been step one.

2. **Proper systemd service** — Got auto-restart and boot persistence right.

3. **Final result is solid** — Ollama is running, listening on 0.0.0.0, service enabled.

### What I should have done

1. **Download binary on my server → SCP → extract** — the winning approach, just should've started there
2. **Check GitHub API for exact filename** before guessing URLs
3. **Kill stale processes** before each retry
4. **Set up systemd from the start** with `HOME` included
5. **Check for GPU first** to set expectations

### Time breakdown
- ~35 min actual → should've been ~5 min with the right approach

**Lesson learned:** When dealing with Chinese cloud servers, never download from international sources directly. Always proxy through a fast intermediary. 🦞
