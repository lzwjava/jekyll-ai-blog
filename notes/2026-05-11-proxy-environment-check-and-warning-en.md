---
audio: false
generated: true
image: false
lang: en
layout: post
title: Proxy Environment Check and Warning
translated: false
type: note
---

Added `warn_if_proxy_set()`:

- Checks `http_proxy`, `https_proxy`, `HTTP_PROXY`, `HTTPS_PROXY`, `all_proxy`, `ALL_PROXY`.
- If any is set, prints which vars + values, explains hf-mirror.com doesn't need a proxy, and shows the exact `unset` command.
- Runs `curl -m 5 https://www.google.com` (which inherits the user's proxy env) and reports the HTTP code — `200` means the proxy works but is unneeded; non-200 means it's probably broken anyway.
- Handles missing `curl` gracefully (`FileNotFoundError`).
- Called once at the start of `main()` before any downloads happen.

Doesn't abort — just warns, so the user can still proceed if they really want to.
