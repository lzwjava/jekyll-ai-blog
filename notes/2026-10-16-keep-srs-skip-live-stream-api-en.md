---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keep SRS, Skip Live Stream API
translated: false
type: note
---

Short answer: **not for this app, not now.** The Live Stream API is a great product, but its model fights how Fun Live works. I compared it against your code:

## Why it's a poor fit here

| Your app today | Live Stream API |
| --- | --- |
| A `live` row is created any moment; anchor gets a **per-live `rtmpKey`** and pushes instantly with OBS | Channels + input endpoints are **pre-provisioned resources**. Provisioning takes minutes; you'd have to `POST` create a channel per lecture, wait for `ACTIVE`, then push, then stop it |
| Multiple simultaneous lectures | Default project quota allows only a **handful of concurrent channels** → you'd need a quota increase before growth |
| Web desktop plays **HTTP-FLV** (`flv.js`), iOS plays **RTMP** | Outputs **HLS/DASH only** — no FLV, no RTMP playback. You'd need client changes in `live-web` and the native iOS app loses its `rtmpUrl` |
| `on_publish` auth hook (reject unknown stream keys), `on_dvr` → `recorded_video` row | **No webhooks at all.** No publish authorization callback, no DVR callback. Replay would have to be rebuilt around "live-to-VOD → GCS → poll for files" |
| Random multi-line `hlsUrls` failover | Single output path (GCS + Media CDN) |
| Cost: your VM already exists, SRS adds ~0 marginal cost | **Billed per input hour** while a channel is provisioned/running + GCS writes + delivery egress |
| Instant push → viewers see stream in ~1–3 s (FLV) | Segment-based packaging, typically ~6–30 s latency |

So adopting it means: a channel-lifecycle manager in PHP (create/provision/poll/stop per lecture), IAM service accounts, quota requests, Media CDN setup, removing all hook logic, and rewriting two frontends + iOS playback. That's a multi-day project that *replaces* working features rather than adding them.

## Where it *would* make sense later

- You outgrow one e2-medium VM and want managed ABR transcoding (SRS `copy` gives viewers one rendition only — that's the main real feature gap).
- You want Google-grade reliability/ops instead of self-hosted SRS.
- Non-interactive, high-value broadcasts (webinars) where 30 s latency is fine.

## Recommendation

Stick with the plan: **SRS on your VM → HTTPS playback via nginx → repoint `LiveDao` → verify.** It reuses your existing hooks, DVR, FLV/RTMP/HLS players, and per-lecture stream keys with zero client changes, and it's ~an hour of work instead of days. If transcoded multi-rendition output becomes a need later, you can even have SRT/RTMP-forward from SRS into a managed service then — but that's a Phase 6 decision, fully reversible since frontends read URLs from the API.

I'm mid-way through verifying SRS's hook response semantics (confirmed: allow = body `0`, deny = any other JSON; hooks POST **JSON**, so I'll make `LiveHooks` read JSON form-or-body robustly).

**Continue with the SRS implementation?**
