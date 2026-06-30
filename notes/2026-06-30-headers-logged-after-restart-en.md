---
audio: false
generated: true
image: false
lang: en
layout: post
title: Headers Logged After Restart
translated: false
type: note
---

Server restarted and now logs headers with every request. Here's what a logged record now looks like:

```json
{
  "id": "chatcmpl-...",
  "timestamp": "2026-06-30T05:59:...Z",
  "prompt": "user: Test headers logging",
  "response": "...",
  "headers": {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.5 Safari/605.1.15",
    "referer": "https://gq8kq409jjxh7r-8081.proxy.runpod.net/",
    "origin": "https://gq8kq409jjxh7r-8081.proxy.runpod.net"
  }
}
```

Currently logged headers: `user-agent`, `referer`, `origin`, `x-forwarded-for`, `x-real-ip`, `cf-connecting-ip`. Whatever the RunPod proxy forwards through is captured. The earlier Amazon question user didn't leave a referer or origin (just the `user-agent` from the browser), but now any future request will have full context.

Committed to git as `c537e7c`.
