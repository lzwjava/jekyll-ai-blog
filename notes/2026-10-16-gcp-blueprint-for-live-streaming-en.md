---
audio: false
generated: true
image: false
lang: en
layout: post
title: GCP Blueprint for Live Streaming
translated: false
type: note
---

Yes — Google Cloud is a solid choice for this. Its **Premium Tier global network** is actually one of the best for Asia-Pacific reach, and it has a **Hong Kong region**, which is the sweet spot for your app (good latency to mainland China + SEA + US West). But there are a few caveats you must design around:

## GCP caveats for a RED-like app

1. **No mainland China region** (true for AWS/Azure too — only Aliyun/Tencent/Huawei have them). Mainland users connect via HK/Tokyo/Singapore edge.
2. **Google is blocked in mainland China** — so no Firebase, Google Fonts, reCAPTCHA, Google Sign-In, or `storage.googleapis.com` CDN URLs for CN users. Use Google services **server-side only**, or self-host assets behind your own domain.
3. **No managed live-streaming service** — you'll self-run SRS on Compute Engine (fine, that's what you already do). For VOD transcoding of replays you can use the Transcoder API.

## Concrete GCP blueprint for live-server

| Tier | Service |
|---|---|
| API + web (nginx) | **GKE Autopilot** or 2–3 Compute Engine VMs in `asia-east2` (Hong Kong) — start with VMs, it's simpler |
| Global entry | **Global HTTP(S) Load Balancer + Cloud CDN** — one anycast IP worldwide, TLS at edge, cache static/API GETs |
| MySQL | **Cloud SQL for MySQL** (HA in HK) — replaces your dockerized MySQL 5.7; read replicas later |
| Redis | **Memorystore for Redis** |
| Replay VOD, images | **Cloud Storage** (`multi-region` or HK bucket) + Cloud CDN in front — replays served as HLS through CDN |
| Live ingest/origin | **SRS on GCE**: 1 VM in HK (origin) + optional 1 VM in `us-west1`/`europe-west1` (nearest push ingest, relay to HK); play out via CDN'd HLS |
| Frontend (live-mobile-web) | **Cloud Storage static website** or Cloud Run, behind the same LB |

**Latency flow:** streamer pushes RTMP → nearest SRS ingest → HK origin → transcode HLS → Cloud CDN edge → viewer (2–5s latency, and no cross-Pacific traffic on your origin bill).

## Cost notes

- Egress ~$0.08–0.12/GB (same ballpark as AWS); Cloud CDN has a free tier and cache-fill pricing is cheaper than serving from origin.
- **Worth applying to Google for Startups** — up to $200k in cloud credits for eligible startups; that would cover this stack for a year easily.
- If budget is the priority and you don't need managed services: a HK VPS (Hetzner HK / Vultr HK) + Cloudflare free CDN does steps 1–3 of the migration path for ~$10/month.

## Verdict

- **Choose GCP if**: you want managed DB/Redis, good APAC networking, and plan to scale the API tier. Deploy in **Hong Kong (`asia-east2`)** as primary, Cloud CDN globally, SRS origin in HK.
- **Choose AWS instead if**: you want managed live video (MediaLive) or expect enterprise/compliance customers.
- **Skip both if**: you just want "global-ish" cheaply — VPS + Cloudflare first, migrate to GCP when you have real traffic.

The GCP route doesn't require rewriting your PHP app — docker-compose maps almost 1:1 (Cloud SQL ↔ your `database` service, Memorystore ↔ `redis`), so the migration is mostly infra config.

Want me to draft the deployment configs for this path — e.g., a `cloudbuild.yaml`/Terraform for the GKE-or-VM + Cloud SQL setup, and the multi-region SRS ingest/relay config?