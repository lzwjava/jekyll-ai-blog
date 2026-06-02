---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Proxy for China Access
translated: false
type: note
---

**Question:** What is `https://ghfast.top`?

**Answer:**

It's a **GitHub proxy / accelerator** (`GitHub 代理加速`) — a mirror/CDN service that speeds up GitHub downloads for users in mainland China, where GitHub is slow or throttled by the GFW.

It proxies:

- GitHub file downloads (repos, releases, raw files)
- `github.com` release assets
- `raw.githubusercontent.com` content
- GitHub Gist files
- Archive downloads (`.tar.gz`, `.zip`)

**How it works:**
You prepend the proxy URL to any GitHub URL:

```bash
# Direct (slow in CN)
https://github.com/owner/repo/releases/download/v1.0/binary.tar.gz

# Via ghfast.top
https://ghfast.top/https://github.com/owner/repo/releases/download/v1.0/binary.tar.gz
```

Or for `raw.githubusercontent.com`:

```bash
https://ghfast.top/https://raw.githubusercontent.com/owner/repo/main/file.txt
```

**Typical use case for you:**
If you're `pip install`-ing or `wget`-ing GitHub-hosted model weights, binaries, or scripts from your Guangzhou machine (or the Ubuntu workstation), and it's crawling — this proxy can unblock it. Similar services include `ghproxy.com`, `mirror.ghproxy.com`, etc. They come and go as the GFW adapts.

**Trustworthiness caveat:** These are third-party proxies run by individuals. Don't pipe untrusted binaries through them without verifying checksums — `sha256sum` everything.
