---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backend Detection and Cache Test
translated: false
type: note
---

Backend Detection Test
  Model: tencent/hy3-preview
  Proxy: HTTP_PROXY=<http://127.0.0.1:7890> (port 7890 reachable)

[1/3] Sending streaming request to detect backend...

  Response id:  gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX
  id detection: unknown (id='gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX')
  delta keys:   ['content', 'role']
  delta detect: unknown (delta keys: ['content', 'role'])
  TTFT:         4.319s
  Total time:   4.319s
  Full text:    'Hello! It is a'

[2/3] Checking server header...
  Server:        cloudflare
  X-Powered-By:  not reported

[3/3] Prefix cache test (two requests with shared prefix)...
  Shared prefix: 13000 chars, ~2000 tokens

  Request A (cold)... TTFT=7.703s, total=7.703s
  Request B (same prefix, different suffix)... TTFT=2.674s, total=2.674s
  -> Likely cache HIT (TTFT dropped to 34.7% of cold)

Summary:
  Backend:       unknown (id='gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX') / unknown (delta keys: ['content', 'role'])
  Server:        cloudflare
  TTFT (cold):   4.319s
