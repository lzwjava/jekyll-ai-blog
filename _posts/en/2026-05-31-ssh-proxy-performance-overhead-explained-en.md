---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Proxy Performance Overhead Explained
translated: false
type: note
---

The old SSH path looked like this:

```
git → ssh → ncat (subprocess) → SOCKS5 → mihomo (:7891) → Hysteria2 → DMIT LA → GitHub
```

vs the new HTTPS path:

```
git → HTTP proxy → mihomo (:7890) → Hysteria2 → DMIT LA → GitHub
```

Three things make the SSH path slower:

1. Extra process hop. ncat spawns as a subprocess via `ProxyCommand`. SSH talks to ncat's stdin/stdout, ncat relays to SOCKS5. Every byte passes through two extra context switches (kernel → ncat → kernel → mihomo). The HTTP path goes directly to mihomo's socket — no middleman process.

2. TCP-over-TCP meltdown. SSH runs over TCP. SOCKS5 also runs over TCP. So you have git data inside SSH's TCP stream, which is itself inside another TCP connection to the SOCKS5 proxy. Two independent TCP congestion control algorithms competing — when packet loss happens, both layers retransmit and back off, multiplying the slowdown. HTTP CONNECT is a single TCP hop: mihomo establishes the tunnel and the underlying TLS connection to GitHub runs end-to-end on one TCP stream.

3. ncat's relay buffer. From the source code I read (`ncat.h:140`): `DEFAULT_TCP_BUF_LEN = 8192` — 8KB reads in a select() loop. Each chunk requires a read syscall, a write syscall, and a context switch. For a 30 MB git pack, that's ~3,700 syscall pairs. The HTTP proxy path lets the kernel handle the data more directly through its own buffer management without an extra userspace relay.

The HTTP proxy (mihomo on :7890) is essentially just an HTTP CONNECT tunnel — it receives the CONNECT request, opens a TCP connection to GitHub, responds "200 OK", and then mihomo pipes the raw bytes through. Much less overhead than the SSH/SOCKS5/ncat chain.
