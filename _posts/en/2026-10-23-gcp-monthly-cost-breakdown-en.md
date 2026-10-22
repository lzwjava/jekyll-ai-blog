---
audio: false
generated: true
image: false
lang: en
layout: post
title: GCP Monthly Cost Breakdown
translated: false
type: note
---

Got everything. Here's the full cost breakdown for your GCP setup.

## GCP monthly cost — `graphite-ally-445108-k3` (project "My Project 56412")

**Your resources (measured):**
- **1× Compute VM `live-server`** — `e2-medium` (2 vCPU / 4 GB), on-demand, **asia-east2 (Hong Kong)**, running since Oct 15
- **1× boot disk** — 50 GB `pd-standard` (standard persistent disk)
- **Daily snapshots** via policy `default-schedule-1` (14-day retention, 7 so far, ~5.5 GB stored)
- **GCS buckets** — `funlive-videos` 37.4 GiB (videos), `qulive` 1.96 GiB, `lzwjava1` 0.1 GiB (all STANDARD storage)
- MySQL/Redis run as containers on the VM (no Cloud SQL), external IP is **ephemeral** → $0

| Item | Quantity | Rate | Monthly |
|---|---|---|---|
| e2-medium CPU (2 vCPU) | 2 × 730 h | $0.030519/vCPU-h | $44.56 |
| e2-medium RAM (4 GB) | 4 × 730 h | $0.004295/GB-h | $12.54 |
| **Compute subtotal** | | | **$57.10** |
| Sustained-use discount (auto, ~30%, always-on) | | | −$17.13 |
| PD standard disk | 50 GB | $0.0498/GB | $2.49 |
| Snapshots (14-day retention, growing) | ~5.5 GB | $0.044/GB | ~$0.25 |
| GCS storage (videos etc.) | ~42 GB | ~$0.023–0.026/GB | ~$1.00 |
| Network egress (measured 4.4 GB/30d) | ~5 GB | $0.12/GB (premium) | ~$0.60 |
| **Estimated TOTAL** | | | **≈ $44–46/mo** |

## Key notes
- **~90% of the bill is the single `e2-medium` VM (~$40 after automatic SUD)**. List price $57; GCP's automatic sustained-use discount (~30%) brings the compute down to ~$40 for a full month of uptime.
- **Everything else is small**: disk $2.49, snapshots ~$0.25 (watch — retention is 14 days then self-prunes), GCS ~$1, egress ~$0.60.
- **The one unknown**: if viewers stream the videos in `gs://funlive-videos` over the internet, GCS egress bills separately (~$0.12/GB out of Asia) and can dominate — that's traffic-dependent, not included above.
- I could not pull the actual billed amounts (the `costDetails` API returned 404 — the billing account `013A1C-EEDE00-C37882` isn't granting read access to your account), so this is an estimate from GCP's official SKU catalog + your live resource inventory.

**Ways to cut it:** nothing you're wasting much on — the VM dominates. If load permits, an `e2-small` would halve compute (~$20/mo) and keeps 4 GB via memory tradeoff; otherwise this stack is already lean.
