---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Python Version Pinning in CI
translated: false
type: note
---

Fixed. Summary of what was wrong and what I changed in `.github/workflows/gh-pages.yml`:

**Root cause:** `ubuntu-latest` now runs Ubuntu 26.04, and its hosted toolcache no longer contains CPython `3.13.2`. `setup-python` failed with:
```
##[error]The version '3.13.2' with architecture 'x64' was not found for Ubuntu 26.04.
```

**Changes:**
1. **Python version** — changed `python-version: "3.13.2"` → `"3.13"` (patch-less). `setup-python` now resolves to the newest available 3.13.x for the runner OS instead of pinning a removed exact patch.
2. **Failure notification** — it also errored (`No module named 'dotenv'`) because it ran bare system `python3` without the repo deps. Rewrote it to post to Telegram via `curl`, so the alert fires reliably even when Python setup/installation failed earlier.

YAML validated OK. I did not commit — let me know if you want it pushed.

**Heads-up:** the same exact `"3.13.2"` pin exists in other workflows, which will hit the identical Ubuntu 26.04 failure:
- `test.yml`, `punch.yml`, `reminders.yml`, `notes.yml`, `news.yml`, `notes-translation.yml`, `nytimes.yml` (all pin `3.13.2`; `translate.yml`/`habit.yml` already use `3.x`/`3.13`, so they're fine)

Want me to apply the same fix to those?
