---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nmap Clone Success with Ncat Source
translated: false
type: note
---

Clone succeeded via HTTPS with credential manager. Here's the result:

```
Repository: https://github.com/nmap/nmap.git
Location:   /Users/lzwjava/projects/nmap/
Size:       84 MB (shallow clone --depth 1)
ncat dir:   /Users/lzwjava/projects/nmap/ncat/
```

The ncat source is at `/Users/lzwjava/projects/nmap/ncat/` — you've got the full nmap source tree with ncat included. The repo cloned cleanly via HTTPS (no auth needed for a public repo, credential manager was available as fallback).

Key ncat files:
- `ncat/ncat_main.c` — entry point
- `ncat/ncat_core.c` — core connection logic
- `ncat/ncat_ssl.c` — SSL/TLS support
- `ncat/ncat_proxy.c` — proxy mode
- `ncat/http.c` — HTTP CONNECT support

Want me to build ncat from source, or dig into any specific part of the code?