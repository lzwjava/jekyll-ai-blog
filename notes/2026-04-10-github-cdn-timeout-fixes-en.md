---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub CDN Connection Timeout Fixes
translated: false
type: note
---

Question: Why does `npx camoufox-js fetch` fail with `UND_ERR_CONNECT_TIMEOUT 185.199.109.133:443` after stopping proxy, and how to fix it?

Answer:

This error shows **direct connection to GitHub CDN is blocked or unreachable**:

```
ConnectTimeoutError: 185.199.109.133:443
```

That IP belongs to **GitHub release CDN**.
So what happened:

* With proxy → **very slow but reachable**
* Without proxy → **blocked / timeout**
* Result → you are stuck between **slow proxy** and **blocked direct route**

This is very common on some networks.

---

# What the error means

Node.js is trying:

```
https://github.com/.../camoufox...
```

It resolves to:

```
185.199.109.133
```

Then:

```
timeout: 10000ms
```

Meaning:

* TCP connection cannot be established
* firewall / ISP / DNS route issue
* or GitHub CDN unreachable from your network

---

# Fastest Fix (use proxy ONLY for this command)

Run:

```bash
proxychains4 -q npx camoufox-js fetch
```

But add **dynamic_chain** in proxychains config:

Edit:

```bash
/opt/homebrew/etc/proxychains.conf
```

Change:

```
strict_chain
```

to:

```
dynamic_chain
```

This avoids dead proxies blocking.

---

# Better Fix (recommended)

Use HTTPS proxy just for this download:

```bash
HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
```

or:

```bash
ALL_PROXY=socks5://127.0.0.1:7890 npx camoufox-js fetch
```

(depends on your local proxy port)

This is **much faster than proxychains**.

---

# Best Fix (manual download — fastest)

Get the download URL:

```bash
DEBUG=camoufox* npx camoufox-js fetch
```

It prints:

```
Downloading from:
https://github.com/.../camoufox-macos.zip
```

Then download using your proxy tool:

If using clash:

```bash
curl -L -x http://127.0.0.1:7890 -o camoufox.zip <URL>
```

or socks:

```bash
curl --socks5 127.0.0.1:7890 -L -o camoufox.zip <URL>
```

Then extract:

```bash
mkdir -p ~/.cache/camoufox
unzip camoufox.zip -d ~/.cache/camoufox
```

Then:

```bash
npx camoufox-js fetch
```

It will detect already downloaded.

---

# Why this happens

Your behavior proves:

| mode         | result         |
| ------------ | -------------- |
| proxychains  | slow but works |
| direct       | timeout        |
| system proxy | not configured |

So only **proper proxy env var** works.

---

# Clean Solution (one command)

Use:

```bash
ALL_PROXY=socks5://127.0.0.1:7890 npx camoufox-js fetch
```

This usually finishes in:

```
10–30 seconds
```

instead of:

```
14 hours
```

---

If you're not sure your proxy port, run:

```bash
lsof -iTCP -sTCP:LISTEN | grep -E "7890|1080|8888"
```

or tell me:

* Clash?
* Surge?
* v2ray?
* shadowsocks?

I'll give exact command.