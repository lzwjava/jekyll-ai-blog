---
audio: false
generated: true
image: false
lang: en
layout: post
title: SOCKS5 Proxy Tests and Results
translated: false
type: note
---

Done. Here's the summary:

```
TEST RESULTS
============

1. macOS nc -X 5:  BROKEN
   - SOCKS5 handshake fails: "banner line contains invalid characters"
   - Can't use this

2. ncat vs connect throughput (git fetch pytorch depth=50, 3 runs each):
   ncat:    9.6s,  6.1s, 11.8s
   connect: 13.1s, 7.9s, 11.3s
   → Identical within network variance

3. SSH handshake latency (3 runs each):
   ncat:    2.5s, 2.6s, 2.5s
   connect: 2.3s, 2.8s, 2.3s
   → Identical

VERDICT
=======
The bottleneck is your SOCKS5 proxy (mihomo) + GitHub's servers,
not the relay tool. Both ncat and connect are equally fast.

Config updated to connect anyway — it's a cleaner 100KB tool
vs ncat which pulls in nmap's nsock engine.

~/.ssh/config now:
  ProxyCommand connect -S localhost:7891 -5 %h %p
```

The real speedup for large model repo transfers is still what you're already doing — using HTTPS remotes (ghfast.top mirror) to bypass SSH entirely.
