---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build fix and deploy success
translated: false
type: note
---

Build triggered and deployed successfully. ✅

**What happened:**

1. I dispatched the workflow and discovered the **previous build had failed** — the CI "Verify generated files are committed" step caught that `portfolio.html` was out of sync with its generator.

2. **Root cause:** `scripts/build_cases.py` generates `portfolio.html` (and `cases/*.html`) from internal templates. My earlier manual favicon edit made the committed `portfolio.html` differ from what the generator produces — and the generator template still had the old emoji favicon.

3. **Fix:** Updated both templates in `scripts/build_cases.py` to emit the new DeepCompute favicon links (`favicon.ico`, `deepcompute-icon.png`, `apple-touch-icon.png`) with correct relative paths (`logo/…` for portfolio, `../logo/…` for case pages), then regenerated all pages.

4. **Committed and pushed** — the push-triggered run passed end-to-end:

   - ✓ **Build (regenerate static pages)** — 8s
   - ✓ **Deploy to Cloudflare Pages** — 30s

The site (with the DeepCompute logo, philosophy band, and all regenerated case pages) is now live. The two earlier failures were both just the same out-of-date verification check, now resolved.
