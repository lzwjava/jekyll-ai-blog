---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Docker Internal DNS Resolution Works
translated: false
type: note
---

There it is. Here's how it works:

### The `/etc/hosts` in the container

The container's own hostname (`32bb25fb32c8`) is listed with all its IPs from each connected network. But **`LibreChat` is NOT in `/etc/hosts`**.

### So how does it resolve?

1. **`/etc/resolv.conf`** points to `nameserver 127.0.0.11` — that's Docker's **embedded DNS resolver**, running inside every container's network namespace.

2. When you do a DNS lookup for `LibreChat`, it goes to `127.0.0.11`, which is Docker's DNS. Docker knows about all containers on each network — when you `docker network connect librechat_default uptime-kuma`, the DNS resolver now sees `LibreChat` on that shared network and returns its IP (`172.18.0.6`).

3. If the container wasn't on `librechat_default`, Docker's DNS would **not** know about `LibreChat` and the lookup would fail — exactly what happened before.

**TL;DR:** It's not `/etc/hosts`. It's Docker's internal DNS at `127.0.0.11` that resolves container names, and it only works when both containers share at least one network.