---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stale A Record Causing 502
translated: false
type: note
---

## Answer to your question

**It's an A record** — but there are **two** A records on `funlive.io`, and that's the real problem:

```
funlive.io.  403  IN  A  34.150.108.243      ← your server
funlive.io.  403  IN  A  162.255.119.114     ← Namecheap URL Forward (leftover)
```

Nameservers are `dns1/dns2.registrar-servers.com` (Namecheap).

## Why you're seeing 502

There are **two separate problems**, and I want to be precise about what I could and couldn't verify:

**1. The stale second A record is hijacking half your traffic.** `162.255.119.114` is Namecheap's URL Forwarding server. It answers with:

```
HTTP/1.1 302 Found
Server: namecheap-nginx
X-Served-By: Namecheap URL Forward
Location: http://www.funlive.io/
```

But **`www.funlive.io` does not exist** — it returns `NXDOMAIN` (Status:3) from both Google and Cloudflare DoH. So the redirect points at a dead name. This is a leftover from a "Redirect Domain" setup in Namecheap; with round-robin DNS, roughly half of visitors hit this broken path regardless of what your server does.

**2. `34.150.108.243` isn't answering on port 80/443.** Here I have to be careful, because your environment runs everything through a local proxy (`127.0.0.1:7890`), and that proxy mints its own 502s. I verified this with a control test — a guaranteed-dead IP (`192.0.2.1`) returns the *identical* response:

```
HTTP/1.1 502 Bad Gateway
Connection: keep-alive
Keep-Alive: timeout=4
Proxy-Connection: keep-alive      ← proxy-generated, no Server header
Content-Length: 0
```

A genuine origin 502 would carry a `Server:` and `Date:` header (as the Namecheap one did). So the 502 you're seeing is your **proxy failing to connect to the origin**, not your app returning 502. Port 443 also fails at handshake (`SSL_ERROR_SYSCALL`). The PTR is `243.108.150.34.bc.googleusercontent.com`, so it's a GCP IP.

**Caveat:** I could not distinguish with certainty whether the VM is unreachable from the public internet or just from the proxy exit node — my direct no-proxy attempts also timed out, but my egress may be restricted.

## What to fix

1. **Delete the `162.255.119.114` record** in Namecheap DNS → remove the "Redirect Domain" / URL Forward entry. Keep only `34.150.108.243`.
2. **Add an `A` record for `www`** pointing to `34.150.108.243` (or a CNAME to the apex), so nothing depends on the dead `www` name.
3. **Check the GCP side** — this is the part I couldn't test from here. On the VM: `sudo ss -tlnp | grep -E ':80|:443'`, confirm nginx/caddy is running, and verify VPC firewall rules allow ingress on 80/443 from `0.0.0.0/0`. If it's behind a GCP HTTPS Load Balancer, check the backend health status — a 502 from a real LB means an unhealthy or unreachable backend.

After editing, flush propagation: `dig funlive.io A @8.8.8.8` until only the single IP remains.
