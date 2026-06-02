---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Normal wget redirect from mirror.accum.se
translated: false
type: note
---

Your `wget` command is hitting `https://mirror.accum.se/mirror/wikimedia.org/dumps/...` and getting a **302 redirect** to `https://laotzu.ftp.acc.umu.se/...`. This is completely normal and expected behavior for the **accum.se** mirror — here’s why it happens and what it means:

### Why the redirect happens
`mirror.accum.se` is only a **redirector / load-balancer** run by Academic Computer Club at Umeå University (ACC) in Sweden.
It does **not** host the files itself. Instead:

- It looks at your IP’s geolocation (or sometimes load)
- It automatically redirects you to the fastest/closest actual storage server in their mirror farm
- In your case it chose `laotzu.ftp.acc.umu.se` (which is the real FTP/HTTP server that has the data)

This is the same system they have used for many years. Other common hostnames you might be redirected to are:

- `issac.ftp.acc.umu.se`
- `laotzu.ftp.acc.umu.se` (the one you got)
- `morpork.ftp.acc.umu.se`
- etc.

So even though you wrote `mirror.accum.se` in your script, you almost always end up downloading from one of the `*.ftp.acc.umu.se` back-ends.

### Why you saw “206 Partial Content” on the first file
Because you (or someone/some script) already started downloading that exact same file before, `wget -c` detected the partial local file and sent a `Range` request. The server correctly resumed the download → 206 Partial Content. That’s good!

### Is there any problem?
No. Everything is working as intended.

- The redirect is normal and harmless
- The final server (`laotzu.ftp.acc.umu.se`) is still the official ACC/Wikimedia mirror
- Checksums will be identical no matter which back-end server you get redirected to

### If you want to avoid the redirect (optional)
You can skip the redirector completely and point directly to one of the real hosts, e.g.:

```bash
# These three are round-robined behind mirror.accum.se anyway
wget -c https://laotzu.ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/20251101/...
# or
wget -c https://issac.ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/20251101/...
```

But most people just keep using `mirror.accum.se` because the redirector automatically picks the best one for you.

### TL;DR
Your script is fine. The 302 redirect from `mirror.accum.se` → `laotzu.ftp.acc.umu.se` is the normal, expected behavior of that mirror. Nothing is wrong, and you’re still downloading the authentic Wikimedia dump. Keep using `mirror.accum.se` — it’s one of the fastest and most reliable mirrors worldwide.
