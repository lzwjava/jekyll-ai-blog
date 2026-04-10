---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Slow Camoufox Download
translated: false
type: note
---

Question: Why is `npx camoufox-js fetch` still extremely slow (1% with ~50,000s remaining) even after it started moving?

Answer:

This means the download **is working**, but your connection to the Camoufox binary server is **extremely slow**. The ETA `50606.8s` (~14 hours) is calculated from the **current transfer speed**, which is likely only a few KB/s.

This usually happens due to one of these reasons:

---

## 1. You are still going through a proxy (most likely)

Even if you removed `proxychains4`, your system may still be using:

* SOCKS proxy (Clash / V2Ray / Shadowsocks)
* HTTP proxy (`HTTP_PROXY`, `HTTPS_PROXY`)
* VPN with slow exit node
* Corporate network filtering

Check quickly:

```bash
env | grep -i proxy
```

If you see something like:

```
HTTP_PROXY=...
HTTPS_PROXY=...
ALL_PROXY=...
```

Then you're **still downloading through proxy** → very slow.

Fix:

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
npx camoufox-js fetch
```

---

## 2. Node.js downloader is single-threaded

`camoufox-js fetch` downloads using Node fetch → **single connection**
Large binary + far CDN = very slow.

This is common when:

* Server is in US/EU
* You're routing through Asia proxy
* Packet loss high

---

## 3. The Camoufox binary is large

Camoufox downloads:

* patched Firefox
* stealth patches
* sandbox runtime
* platform-specific bundle

Usually **150MB–400MB**

At **10 KB/s**:

```
300MB / 10KB/s ≈ 8 hours
```

Your ETA (~14h) matches this.

---

## 4. Best fix (recommended)

Cancel and force direct fast download:

```
Ctrl + C
```

Then:

```
NO_PROXY=* npx camoufox-js fetch
```

or:

```
npm_config_proxy= npm_config_https_proxy= npx camoufox-js fetch
```

---

## 5. Even better (fastest method)

Use **curl multi-thread download** manually:

First find URL:

```
DEBUG=camoufox* npx camoufox-js fetch
```

It will print something like:

```
Downloading from https://github.com/.../camoufox-mac.zip
```

Then download with:

```
curl -L -o camoufox.zip <URL>
```

Then extract to cache:

```
~/.cache/camoufox/
```

This is **10x faster**.

---

## 6. If you're installing Hermes agent

After fetch completes:

```
cd hermes-agent
npm install
npm run build
```

or:

```
pnpm install
pnpm dev
```

Hermes itself is small — **Camoufox is the heavy part**.

---

## Expected normal speed

Healthy download should look like:

```
Downloading Camoufox... [======----------------------] 15% 20s
```

Not:

```
1% 50606s
```

So your connection is **~1000x slower than normal**.

---

## Quick diagnosis (run this)

```
curl -I https://github.com
```

If this takes >2s → your GitHub/CDN route is slow.

---

## Most likely cause (ranked)

1. Proxy still enabled (90%)
2. VPN slow exit node
3. GitHub CDN blocked/slow region
4. Packet loss / DNS issue
5. ISP throttling large downloads

---

## Fastest solution

Use mobile hotspot (seriously):

```
switch wifi → phone hotspot
npx camoufox-js fetch
```

Often finishes in **30 seconds**.