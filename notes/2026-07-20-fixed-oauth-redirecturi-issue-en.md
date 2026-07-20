---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed OAuth redirect_uri issue
translated: false
type: note
---

The fix is applied. The issue was:

1. **Root cause**: `flow.authorization_url()` was called **before** the local server was started, so the redirect_uri (`http://localhost:8080/`) was never included in the authorization URL. Google rejected the request with "Missing required parameter: redirect_uri".

2. **Fix**: Removed the manual `webbrowser.open(flow.authorization_url()[0])` call. Now `flow.run_local_server(port=8080)` handles the entire flow — it starts the server, generates the URL with the correct redirect_uri, opens the browser, and waits for the callback.

3. **Also added**: Clear instructions to add `http://localhost:8080/` as an Authorized redirect URI in the Google Cloud Console — this is a required step that's easy to miss.

Try again now:

```bash
uv run ww gen-video upload /Users/lzwjava/projects/jekyll-ai-blog/notes/2026-07-20-tesla-p100-vs-m60-for-ai-en.md /Users/lzwjava/Downloads/test_gen_video.mp4
```

If you haven't already, make sure `http://localhost:8080/` is listed in your Google Cloud Console under **APIs & Services → Credentials → your OAuth 2.0 Client ID → Authorized redirect URIs**.
