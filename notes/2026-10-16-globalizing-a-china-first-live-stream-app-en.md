---
audio: false
generated: true
image: false
lang: en
layout: post
title: Globalizing a China-First Live-Stream App
translated: false
type: note
---

Good question. I looked at your codebase: it's a PHP (CodeIgniter) live-streaming platform with SRS for RTMP, MySQL 5.7, Redis, WeChat/Alipay integration, and +86 OTP — i.e., built China-first. Making it "globally accessible" like RED/TikTok is mainly a **media delivery + data tier** problem, not a code problem. Here's how to think about it.

## 1. Set expectations: what "global" apps actually do

- **小红书** is *not* truly global — it's hosted on Alibaba Cloud inside China (needs ICP, content licenses), and users abroad get mediocre latency. That's fine for a China-focused product.
- **TikTok/Douyin** runs a true global architecture: dual-stack (global + China), global CDN for media, multi-region stateful services.
- Pick your target: **(A) global users with China included**, or **(B) global users *except* mainland China**. Option B is 10x easier — one deployment, no ICP, no data-localization compliance.

## 2. The four tiers of a global design

| Tier | Design for global access |
|---|---|
| **Media (the hard part)** | Don't distribute origin. Push RTMP to a **nearest ingest edge** (multi-region SRS: HK, Singapore, Tokyo, LA, Frankfurt), relay to a central **origin** (SRS + ABR transcode to HLS), then play through a **global CDN** (Cloudflare, Akamai, CloudFront) in front of HLS/LL-HLS. Playback latency goes from seconds-to-30s to 2–5s. |
| **API** | Keep the PHP app **stateless** and multi-region (same image in HK/SG/US-East), behind one Anycast DNS/GSLB (Cloudflare Load Balancer / AWS Route53 latency routing). Alternatively, run API in one well-connected region (HK or Singapore) and only cache at the edge — much simpler, acceptable p95 < 300ms for most of Asia. |
| **Data** | One writable MySQL primary (HK/SG) + read replicas per region, or migrate to **Aurora Global Database / PlanetScale** if budget allows. Redis for sessions with regional instances. **Object storage for VOD, images, replay thumbnails**: S3 + cross-region replication, or Cloudflare R2 (free egress, one bucket serves worldwide). |
| **Realtime/other** | WebSockets need sticky routing per region; phone OTP (Supabase), payments (Stripe globally + Alipay/WeChat only for CN users) — abstract payments by user region. |

## 3. Where to deploy — concrete recommendations

**Best starting point: Hong Kong or Singapore as the primary region.** Both have low latency to mainland China, SEA, Japan/Korea, and US West. This is what most "global app with CN users" startups do.

- **Simplest path (recommended for a solo/small team):**
  - Origin: HK (e.g., a single cloud VM or Fly.io/Hetzner HK).
  - All static + HLS playback behind **Cloudflare CDN** (free tier covers a lot).
  - SRS ingest endpoints in HK + one US/EU region, relay to HK origin.
  - MySQL stays single-primary in HK initially.
- **Cloudflare-native path:** keep the PHP app on a VM behind Cloudflare (orange-cloud proxy), put media on **Cloudflare Stream Live** (managed ingest + transcode + global delivery, ~$1/min streamed), storage on R2. Removes most SRS/CDN ops work.
- **Full global path (TikTok-style):** AWS or GCP — CloudFront + ECS/EKS regional clusters, Aurora Global Database, S3 cross-region replication, MediaStore/MediaLive or a fleet of SRS nodes.

## 4. The part you can't skip: legal/compliance

- **Hosting inside mainland China** requires ICP filing, and live streaming requires licenses (网络文化经营许可证, etc.) — heavy compliance burden. Most global apps avoid this with a **HK/intl stack**; mainland users then get decent-but-not-great latency (acceptable, since playback goes via CDN PoPs which often have mainland-adjacent edges).
- **Data residency**: PIPL/GDPR — keep user PII in one primary DB region, avoid replicating personal data everywhere; CDN/cache is fine.
- If you truly need fast CN delivery, the pragmatic move is a **dual deployment**: global stack + a separate domestic stack (Tencent Cloud/Aliyun), with account federation — that's the Douyin/TikTok model.

## 5. Suggested migration path for live-server

1. Containerize everything (you already have docker-compose) → deploy the whole stack to **one HK VM/cloud**; measure baseline.
2. Put Cloudflare in front (orange cloud) for DNS, TLS, caching, WAF — instant "global feel" for static/API GETs.
3. Add HLS playback via CDN + move replays/images to R2/S3. This is the single biggest perceived-latency win.
4. Add a second SRS ingest region (US or EU), relay to HK origin.
5. Only later: API read replicas per region, and consider DB migration if you outgrow single-primary.

Start with steps 1–3; for most apps that gets you "globally accessible" at 10% of the ops cost of a true multi-region architecture. Want me to draft the concrete Cloudflare + HK-deployment setup (wrangler config, CDN caching rules, SRS multi-region relay config) for this repo?