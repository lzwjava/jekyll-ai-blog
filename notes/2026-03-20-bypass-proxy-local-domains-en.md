---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bypass Proxy for Local Custom Domains
translated: false
type: note
---

## Problem

You have a local service (e.g., Uptime Kuma) running on your LAN server, and you want to access it via a custom domain like `http://myapp.local:3001` instead of an IP address.

You've added the entry to `/etc/hosts`:

```
192.168.1.36 myapp.local
```

`ping myapp.local` works, but **the browser can't connect**.

## Root Cause

A system proxy (ClashX, V2Ray, Surge, etc.) is intercepting HTTP/HTTPS traffic. The proxy doesn't know `myapp.local` is a local address, so it tries to route it through an external tunnel — which fails.

**Key insight:** `ping` and `curl` (without proxy env vars) bypass the proxy. Browsers respect system proxy settings.

## Solution: Bypass the Proxy for Local Domains

### Step 1: Identify Your Proxy Tool

Common ones on macOS:

- **ClashX** / **ClashX Pro**
- **Surge**
- **V2Ray**
- **Quantumult X**

### Step 2: Add Bypass Rules

Add these to your proxy's **bypass list** or **direct rules**:

```
myapp.local
*.local
192.168.1.0/24
```

#### ClashX Example (`config.yaml`)

```yaml
bypass:
  - myapp.local
  - '*.local'
  - 192.168.1.0/24
```

#### System Proxy (macOS)

1. System Preferences → Network → Advanced → Proxies
2. Check **"Bypass proxy settings for these Hosts & Domains"**
3. Add: `myapp.local, *.local, 192.168.1.*`

### Step 3: Verify

```bash
# Test resolution
ping myapp.local

# Test without proxy
curl --noproxy '*' http://myapp.local:3001

# Test with proxy (should also work after bypass)
curl http://myapp.local:3001
```

## Debugging Checklist

| Check | Command | Expected |
| ------- | --------- | ---------- |
| DNS resolution | `ping myapp.local` | Resolves to `192.168.1.36` |
| Service running | `curl http://192.168.1.36:3001` | HTTP 200/302 |
| Firewall open | `sudo ufw status` | Port 3001 allowed |
| Proxy bypassing | `curl --noproxy '*' http://myapp.local:3001` | HTTP 200/302 |
| Browser bypassing | DevTools → Network → check request destination | Direct to LAN IP |

## Common Pitfalls

1. **Editing server's `/etc/hosts` instead of client's** — the hosts file must be on the machine running the browser
2. **Forgetting firewall rules** — `sudo ufw allow 3001/tcp` on the server
3. **Proxy intercepting local traffic** — always add `.local` and LAN CIDR to bypass
4. **Browser DNS cache** — clear with `chrome://net-internals/#dns` (Chrome) or restart browser

## Quick Reference

```bash
# On the SERVER (192.168.1.36)
sudo ufw allow 3001/tcp                    # Open firewall
docker ps                                  # Verify service running

# On the CLIENT (192.168.1.37)
echo "192.168.1.36 myapp.local" >> /etc/hosts  # DNS mapping
# Then add myapp.local to proxy bypass list
```
