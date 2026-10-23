---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spot e2-Medium Cuts Costs by 50%
translated: false
type: note
---

Yes — there are cheaper options, but each has a tradeoff. Here's what's available in asia-east2 (Hong Kong), based on GCP's actual Hong Kong SKU rates:

## Cheaper options compared ($/month, asia-east2, 730 h)

| Option | vCPU / RAM | Compute /mo | Est. total/mo | vs. now | Tradeoff |
| --- | --- | --- | --- | --- | --- |
| **e2-small on-demand** (current) | 2 shared / 2 GB | ~$35.6 (after SUD) | **$39–42** | — | — |
| **e2-medium SPOT** ⭐ | 2 / 4 GB | **$15.6** | **~$20** | −50% | VM can be reclaimed anytime (~30s notice, usually rare in HK) |
| e2-small spot | 2 shared / 2 GB | $14.2 | ~$19 | −53% | same spot risk, only ~$1 cheaper than e2‑medium spot — not worth it |
| **e2-micro on-demand** | 1 shared / 1 GB | ~$15–25 | **$20–30** | −30% | 1 GB RAM → MySQL + PHP + Redis + SRS in 1 GB = OOM risk; would need heavy tuning |
| 1-yr committed use (e2-small) | same as now | ~$35 | ~$39 | −5% | no risk, but locks you in and saves little |

## The real lever: **Spot instances** (~70–75% off compute)

Switching to **e2-medium spot** would:

- **Keep 4 GB RAM + 2 vCPU** (no memory/cpu downgrade at all from your original config)
- Drop the bill from ~$40 → **~$20/mo** (compute $15.6 + disk $2.5 + snapshots/GCS/egress ~$4)
- **Best price/RAM ratio** — the spot e2-small is barely cheaper, so spot e2-medium is the sweet spot

## The catch (why I'm asking before doing it)

Spot VMs have **no uptime guarantee** — GCP can terminate with ~30 s notice when capacity is needed or prices spike (in practice events are rare, but they do happen). For a live-streaming site that means:

- in-flight streams drop at that moment
- the box does **not** auto-restart (spot termination = stopped VM)
- I'd partially mitigate with a static-IP boot script + an external watchdog that re-creates the instance when it's found down (e.g., Cloud Scheduler → Cloud Function, adds a tiny bit of complexity, a few $/mo at most)

Options I'd endorse:

1. **Spot e2-medium + watchdog** → ~$20/mo, best value, minor availability risk. *My recommendation.*
2. **Stay e2-small on-demand** → ~$40/mo, no new risk (current state).
3. **e2-micro on-demand** → cheapest *guaranteed-uptime* machine (~$20–30/mo) but 1 GB of RAM is honestly too tight for MySQL + everything else on this box; not recommended.

Want me to go with **option 1 (spot e2-medium + a simple watchdog)**, or stay on the current e2-small?
