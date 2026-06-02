---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switched Qwen Repos to HTTPS for Speed
translated: false
type: note
---

Done. All 5 Qwen repos switched to HTTPS. Summary:

**Root cause:** `ncat` as SSH ProxyCommand is slow for large data transfers. The SOCKS5 proxy itself (mihomo, port 7891) is fast (~1 MB/s), but ncat's bidirectional tunneling adds overhead for git packfiles.

**Fix applied:** All Qwen repos now use HTTPS, which goes through mihomo's HTTP proxy (port 7890). Verified working — `Qwen2.5-Coder` fetch completed in ~77s for 413 objects.

**Bonus:** Your `.git` directory has 1.38 GiB of garbage. Worth running:
```
git -C /Users/lzwjava/projects/Qwen2.5-Coder gc --prune=now
```

For future repos: if you clone model repos from GitHub, use HTTPS by default — the HTTP proxy is faster than the SSH tunnel for large transfers.
