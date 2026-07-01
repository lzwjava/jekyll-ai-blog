---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restart Docker to Apply Proxy Settings
translated: false
type: note
---

Sure, here's the full breakdown:

---

## Root Cause: Docker Daemon Proxy Not Applied

### The Error

```
Get "https://auth.docker.io/token?account=lzwjava&scope=repository%3Alibrary%2Fnode%3Apull&service=registry.docker.io": EOF
```

### What Happened

Docker Hub requires an auth token before you can pull any image. The flow is:

1. Docker contacts `registry-1.docker.io` for an image manifest
2. Registry says "401 — go get a token from `auth.docker.io`"
3. Docker hits `auth.docker.io/token?scope=...`
4. Auth server returns a JWT token
5. Docker retries the manifest request with the token
6. Image layers download

**Step 3 failed.** The TCP connection to `auth.docker.io` got an `EOF` — meaning the connection was immediately dropped. This happens when a firewall or network path kills the connection (common in HK/China for Docker Hub).

### Why the Proxy Didn't Help

Your machine runs **mihomo** (a Clash-based proxy) on `localhost:7890`. The `daemon.json` had proxy settings configured:

```json
{
  "proxies": {
    "http-proxy": "http://localhost:7890",
    "https-proxy": "http://localhost:7890",
    "no-proxy": "localhost,127.0.0.1,.local"
  }
}
```

But here's the thing — **Docker daemon doesn't hot-reload proxy config from `daemon.json`**. When you edit `daemon.json`, the running `dockerd` process doesn't pick up the changes. The proxy settings were only *written*, never *applied* to the running daemon.

I confirmed the proxy itself worked fine:

```
$ curl -x http://localhost:7890 https://registry-1.docker.io/v2/
{"errors":[{"code":"UNAUTHORIZED","message":"authentication required"}]}
```

The `UNAUTHORIZED` response is normal — it means the proxy successfully reached Docker Hub (it's just saying "log in first"). So the proxy was functional; Docker just wasn't using it.

### The Fix

```bash
sudo systemctl restart docker
```

Restarting Docker forced `dockerd` to re-read `daemon.json` and apply the proxy config. After restart, all outbound Docker Hub traffic routes through mihomo → proxy server → Docker Hub, bypassing the blocked connection.

### Verification

```
$ docker pull node:16-bullseye
e12e3f6cbdd8: Pull complete
139c9fa440fc: Pull complete
Status: Downloaded newer image for node:16-bullseye ✅
```

Both images (`node:16-bullseye` and `node:16-buster`) pulled successfully through the proxy.

### Why It Worked for curl But Not Docker

**curl** explicitly used `-x http://localhost:7890` — I told it to route through the proxy.

**dockerd** is a long-running daemon. It reads its config at startup. Editing `daemon.json` while it's running is like changing a config file without restarting the service — the changes sit on disk but the process still uses its in-memory config from when it started.

### Summary

| Item | Before | After |
| --- | --- | --- |
| Docker daemon proxy | Written to config, not applied | Applied after restart |
| `auth.docker.io` connection | EOF (blocked) | ✅ Routed through mihomo |
| `node:16-bullseye` image | Not cached | Cached locally |
| `node:16-buster` image | Not cached | Cached locally |
| Runner service | Down (Docker restart killed it) | Restarted, active |

---

Clear enough, Boss?
