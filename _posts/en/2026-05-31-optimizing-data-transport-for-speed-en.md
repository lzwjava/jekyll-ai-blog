---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Data Transport for Speed
translated: false
type: note
---

Think of it like a supply chain for data:

== THE OLD SSH PATH ==

```
git (factory)
  ↓ produces bytes
ssh (shipping company)
  ↓ wraps in SSH encryption
ncat (middleman warehouse)
  ↓ receives, unpacks, repacks
SOCKS5 (customs broker)
  ↓ protocol negotiation
mihomo (freight forwarder)
  ↓ routes to tunnel
Hysteria2 (container ship)
  ↓ crosses the ocean
DMIT LA (port)
  ↓
GitHub (destination)
```

Every stop adds cost. ncat sits in the middle doing nothing useful — it just receives bytes from one socket and writes them to another. That's a warehouse that just repackages boxes.

== THE NEW HTTPS PATH ==

```
git (factory)
  ↓ produces bytes, wraps in TLS
mihomo (freight forwarder)
  ↓ opens tunnel, steps aside
Hysteria2 (container ship)
  ↓ crosses the ocean
DMIT LA (port)
  ↓
GitHub (destination)
```

mihomo receives the HTTP CONNECT request, opens a TCP connection to GitHub, says "200 OK, go ahead", and then the data flows straight through. It's like a freight forwarder that just opens the gate and lets the truck drive through directly.

== THE THREE COSTS OF EXTRA HOPS ==

1. Syscall overhead. ncat uses `select()` + `read()` + `write()` in a loop with 8KB buffers. Each chunk: kernel copies data from socket A → userspace (ncat) → kernel copies to socket B. That's two kernel-to-userspace copies per chunk. With mihomo's HTTP proxy, the data stays in kernel space longer — fewer copies.

2. Process scheduling. ncat is a separate process. The OS has to context-switch between ssh, ncat, and mihomo. Each switch: save registers, flush TLB, switch page tables, restore registers. At high throughput, this happens thousands of times per second. The HTTP path has fewer processes competing for CPU time.

3. TCP congestion control. SSH's TCP stack is trying to fill its send window. SOCKS5's TCP stack is also trying to fill its send window. They're independent — when one sees packet loss, it backs off, but the other doesn't know and keeps sending, causing more loss. It's like two drivers trying to merge into the same lane without seeing each other. The HTTP path has one TCP stream end-to-end — one driver, one lane, no coordination problems.

== THE STARTUP ANALOGY ==

Big company (SSH path):
  Engineer → Team Lead → Director → VP → CTO → VP → Director → Team Lead → Engineer

  Each person reads the message, understands it, rewrites it in their own words, passes it on. Information degrades, latency accumulates.

Startup (HTTPS path):
  Engineer → Engineer

  Direct communication. Same language. No translation loss.

The "flatter" the protocol stack, the fewer translations between layers, the faster information flows. That's why removing ncat (a relay that just copies bytes) and the SOCKS5 layer (an extra protocol negotiation) made such a huge difference.
