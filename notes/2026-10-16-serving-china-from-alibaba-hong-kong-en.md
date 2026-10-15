---
audio: false
generated: true
image: false
lang: en
layout: post
title: Serving China from Alibaba Hong Kong
translated: false
type: note
---

Alibaba Cloud with a **Hong Kong origin (`cn-hongkong`)** is arguably an even better fit than GCP for your app — because your user base and payment/SMS integrations are China-centric, and Alibaba's cross-border network to mainland China is the best in the business. This is the classic "serve mainland users without ICP" architecture.

## Where Alibaba Cloud wins vs GCP

| Aspect | Alibaba HK | GCP HK |
|---|---|---|
| Mainland CN latency | Best-in-class — Alibaba backbone + optional **CN2 GIA / Global Accelerator** lines to mainland | Good, but cross-border peering is whatever public transit gives you |
| Managed live video | **Apsara Video Live (阿里云视频直播)** — managed ingest/transcode/CDN, you could drop SRS | None — self-run SRS |
| Payments / SMS | First-class Alipay, WeChat Pay, domestic SMS/OTP | Alipay via your own integration; SMS needs a CN provider anyway |
| Payment/billing | RMB invoicing, domestic support | USD, intl support |
| Mainland CDN nodes | Yes — **but requires ICP filing** (see below) | No mainland nodes at all |
| Global footprint (US/EU edge) | Smaller, weaker outside Asia | Much stronger |

## Concrete blueprint — Alibaba HK origin

| Tier | Service |
|---|---|
| API + web (nginx/PHP) | **ECS** in `cn-hongkong` (or **ACK** container cluster if you scale) |
| Global entry | **ALB** in HK + optionally **Global Accelerator (GA)** — GA gives mainland users a stable, fast entry IP over Alibaba's CN lines, big win for cross-border |
| MySQL | **RDS for MySQL** HA edition (replaces dockerized MySQL 5.7) |
| Redis | **Tair / ApsaraDB for Redis** |
| Replays VOD, images | **OSS** bucket in HK + **Alibaba CDN** |
| Live streaming | Either **Apsara Video Live** (managed: push domain → transcode → play domain over CDN, drop SRS entirely) **or** keep SRS on ECS as origin + Alibaba CDN for HLS delivery |
| Frontend static | OSS static hosting + CDN |
| SMS/OTP | **Alibaba Cloud SMS** (domestic + international templates) — could replace part of your Supabase SMS path for CN users |

**Flow:** streamer pushes RTMP to nearest ingest (Apsara Live has overseas ingest nodes too) → HK origin → HLS → CDN edge → viewer.

## The compliance gotchas (important, different from GCP)

1. **Hosting in HK: no ICP filing needed.** Your website/API/replay bucket served from HK works without ICP. This is the whole point of the HK origin.
2. **But mainland CDN nodes require ICP.** If you enable Alibaba CDN nodes *inside* mainland China for your domain, you must have ICP. Without ICP, restrict CDN to **overseas/HK/TW nodes** — mainland viewers then get served from HK edges (still fast, but not as fast as domestic PoPs).
3. **Cross-border data (PIPL).** Storing mainland users' PII (+86 phones, payments) in HK = cross-border data export. You need consent + a legal basis (standard contract filing). Keep CN user PII in the HK region only; don't replicate it casually.
4. **Live-streaming license.** If mainland users both broadcast and watch, 《网络表演经营许可证》/related licenses apply to services *targeting* mainland users regardless of where the servers are. Enforcement is real for platforms monetizing CN users — factor this in if you charge fees (you do: paid lectures + rewards).

## Verdict

- **If the app's core market is China + Asia (+ general global users): choose Alibaba Cloud, HK origin.** Coherent single-vendor stack (ECS + RDS + OSS + Apsara Live + GA), easy Alipay/SMS, best CN latency without ICP. This is what domestic apps launching "international versions" do.
- **Add Cloudflare in front** (orange-cloud on the API domain) if you also want cheap US/EU edge caching — mixing works fine: Cloudflare caches your static/HLS, origin stays in HK.
- **Only pick GCP/AWS if** your primary market is US/EU and China is secondary — then Alibaba's CN advantage doesn't matter to you.

Cost note: HK region is priced ~30–50% above mainland Alibaba regions; GA and CN2 cross-border traffic are the expensive parts — start with plain HK ECS + overseas-only CDN (~$30–60/month for a small stack) and add GA only if mainland latency proves to be a problem.

Want me to write the concrete migration configs — docker-compose → Alibaba HK (ECS startup script + RDS/OSS env vars), the SRS (or Apsara Live) ingest/play domain setup, and an Alibaba CDN config restricted to overseas nodes?