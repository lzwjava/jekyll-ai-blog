---
audio: false
generated: true
image: false
lang: en
layout: post
title: Direct Connection Latency Fix
translated: false
type: note
---

## Result: SSH Latency 5–6s → 1.9s

### What Changed

Tailscale switched from DERP relay to a **direct peer-to-peer connection**:

```
Before:  Mac → DERP relay (Singapore) → to       ~500ms RTT → 5–6s SSH
After:   Mac → direct <IP_ADDRESS>:<PORT> → to     76ms RTT  → 1.9s SSH
```

### Root Cause

Both sides actually *support* direct connection:

- `to` machine has **cone NAT** (`MappingVariesByDestIP: false`) — mappings are stable
- Mac's parents' router has **UPnP enabled** — port mapping works

But Tailscale was giving up on NAT traversal probing too early and falling back to DERP relay. Running `tailscale ping --until-direct` forced it to keep probing until the direct path was found.

### Making It Stick

Two options:

**Option 1 — Periodic re-probe (quick fix)**

```bash
# cron on Mac: re-establish direct every 10 min if it drops
*/10 * * * * tailscale ping --until-direct <TAILSCALE_HOSTNAME>
```

**Option 2 — Router port forward (permanent fix)**
Forward UDP `41641` on home router (`192.168.x.1` LuCI) → `192.168.x.36`. This makes `to` always directly reachable, so Tailscale finds the direct path instantly without needing to probe.

Option 2 is the clean fix — one config change, no cron dependency.
