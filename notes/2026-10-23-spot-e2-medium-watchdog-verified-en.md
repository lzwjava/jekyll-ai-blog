---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spot e2-medium Watchdog Verified
translated: false
type: note
---

All green. Final verification passed — here's the complete rundown:

## ✅ Switched to SPOT e2-medium + watchdog

### What's running now

| Item | Status |
|---|---|
| **VM** | `live-server`, **e2-medium** (2 vCPU / 4 GB), **provisioningModel: SPOT** (preemptible, term-action: STOP) |
| **IP** | `34.150.108.243` — unchanged, static, DNS intact |
| **Containers** | app, web, database, redis, srs — all `Up`, auto-start after boot (restart policies) |
| **Public sites** | funlive.io / web.funlive.io / api.funlive.io → **200** |
| **SRS** | API 200 (RTMP/HLS back up) |
| **Memory** | 4 GB box, only ~730 MB used — lots of headroom |
| **Swap** | 2 GB persistent (still there) |

### The watchdog (built so preemption self-heals)
- **Cloud Function** `spot-watchdog` (gen2, Seoul/asia-east1, 256 MB): every check it fetches the VM status; if not RUNNING → calls `instances.start`
- **Cloud Scheduler** job every **5 minutes** → OIDC-authenticated call
- **Dedicated SA** `spot-watchdog-sa` with only 2 permissions (`compute.instances.get`, `compute.instances.start` + the function invoker)
- **Verified working**: scheduler runs succeeded at 18:15 (earlier PERMISSION_DENIEDs fixed with `roles/run.invoker`), function returned `{"status": "RUNNING", "action": "noop"}`
- **Cost: ~$0** — within Cloud Functions and Scheduler free tiers

So if GCP ever reclaims the VM: it stops → watchdog restarts it within ≤5 min → static IP reattaches → Docker brings all services back automatically. Worst case downtime ~5–10 min, only during an actual preemption event.

### Monthly cost now

| Item | $/mo |
|---|---|
| Compute — **e2-medium SPOT** (2×$0.00874 + 4×$0.00097)/h | **$15.59** |
| Disk 50 GB pd-standard | $2.49 |
| Snapshots (14-day retention) | ~$0.25 |
| GCS storage | ~$1.00 |
| Network egress (~5 GB) | ~$0.60 |
| **Total** | **≈ $20/mo** |

**Result: from ~$44–46→ ~$20/mo (~55% cheaper), same 4 GB/2 vCPU machine you started with.** The original e2-medium on-demand cost ~$57; spot pricing in Hong Kong is ~70% off, so the compute component dropped from ~$40 → ~$15.6.

### Things to keep in mind
- **Preemption is possible** — it's the one availability caveat vs. on-demand. Watchdog mitigates; actual events in HK are typically rare, but not impossible.
- Keep an eye on the watchdog: `gcloud scheduler jobs describe spot-watchdog --location=asia-east1` will show any failed runs in the logs.
- The egress/GCS lines grow only if video traffic grows — that's what to watch if the bill ever creeps up.
