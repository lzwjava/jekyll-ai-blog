---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Resized to e2-small Successfully
translated: false
type: note
---

Done. The server is resized, running, and verified. Here's the full summary:

## ✅ e2-medium → e2-small — complete

**What was done**

1. **Promoted the external IP to static** (`live-server-ip`) first — it was ephemeral and all 4 domains point to it, so a stop/start would have changed it. Same IP `34.150.108.243`, DNS untouched. (Static IPs attached to a running VM are **free**.)
2. **Stopped → resized → started** the VM: now `e2-small`, asia-east2.
3. **Brought the stack back up** (`docker compose up -d` at `/home/lzw/live-server/`) — app, web, database, redis, srs all running.
4. **Added 2 GB swap** (persistent via `/etc/fstab`, swappiness 10) as OOM protection — RAM halved to 2 GB and this box runs MySQL 8.
5. **Added `restart: unless-stopped`** to app/web/database/redis — this resize exposed that they didn't auto-start after a reboot (only SRS did). Applied on the VM and synced to your local `docker-compose.yml`.

**Verification**

- `https://funlive.io`, `www`, `web`, `api` → all **200** from the public internet
- MySQL data intact (`qulive`, 87 MB, SELECT 1 OK)
- Containers all `Up`, restart policy `unless-stopped` on all 5
- Current memory: ~1 GB used of 2 GB + 2 GB swap (was 1.5 GiB of 4 GiB)

**Cost impact (asia-east2 list prices × 730 h)**

| | e2-medium (before) | e2-small (now) |
| --- | --- | --- |
| vCPU (2 × $0.030519) | $44.56 | $44.56 (capped; billed on actual usage, ~17% avg) |
| RAM (4→2 GB @ $0.004295) | $12.54 | **$6.27** |
| after auto SUD (~30%) | ~$40 | **~$35–37** |
| disk + snapshots + GCS + egress | ~$4.4 | ~$4.4 |
| **Estimated total** | **~$44–46/mo** | **~$39–42/mo** |

So roughly **$4–8/mo in direct savings**, possibly more since e2-small is a **shared-core** type billed per vCPU‑second of actual usage (your box averages 17% CPU, so the CPU line may come in under the configured 2-vCPU cap).

**Tradeoffs to know**

- **2 GB RAM** (was 4 GB) — fine at current usage (~1 GB), swap added as backstop. If MySQL/PHP growth pushes it, revisit.
- **Shared cores** — you can still burst to 2 vCPU, but sustained heavy load (e.g., many concurrent viewers/transcodes on the VM) will perform worse than e2-medium's dedicated cores. SRS itself is just a relay, so this matters little for streaming.
- One more thing: the deployed `docker-compose.yml` on the VM has a `srs` service that your local repo copy doesn't — the repo has drifted from production. I synced only the restart changes; consider merging the rest when you next touch the repo.
