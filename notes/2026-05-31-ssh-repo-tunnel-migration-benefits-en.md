---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Repo Tunnel Migration Benefits
translated: false
type: note
---

Here's the verdict:

```
SSH repos:  205  (87.6%)
HTTPS repos: 23  ( 9.8%)
Other:        7  ( 3.0%)
```

Yes, you absolutely need the fix. 87.6% of your repos go through the ncat SOCKS5 tunnel.

The good news: macOS's built-in `nc` already supports SOCKS5:

```
nc -X 5 -x localhost:7891 %h %p
```

Want me to update your `~/.ssh/config` right now? Current:

```
ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

Would become:

```
ProxyCommand nc -X 5 -x localhost:7891 %h %p
```

`nc` uses raw `read()/write()` with no nsock event loop abstraction — simpler I/O path for bulk transfers like `git pull` on large repos. No install needed, it's already at `/usr/bin/nc`.
