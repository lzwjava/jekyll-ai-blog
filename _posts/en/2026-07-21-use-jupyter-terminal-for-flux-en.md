---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Jupyter Terminal for FLUX
translated: false
type: note
---

Still **Permission denied** — port 31090 points to a different instance's SSH, not ours. Our key is only authorized on port 31154 (which is down).

**Your options:**

1. **Use Jupyter terminal** (already working) — run FLUX.1-dev directly
2. **Restart the space** from the AMD cloud console — this should remap port 31154
3. **Add your key to the SSH on port 31090** — but you'd need access to that instance

Jupyter is the quickest path. Want to start FLUX.1-dev there?
