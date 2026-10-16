---
audio: false
generated: true
image: false
lang: en
layout: post
title: Live Streaming Deployed on Google Cloud
translated: false
type: note
---

Done. **Live streaming is now working on Google Cloud.** Summary:

## What was deployed

| Piece | Change |
|---|---|
| `srs/srs.conf` | New SRS 6 config: RTMP ingest, HLS (2 s fragments) + HTTP-FLV, per-session DVR, hooks → app |
| `docker-compose.yml` | New `srs` service (`ossrs/srs:6`, ports 1935+8080, `restart: unless-stopped`, persistent `./srs-data`) |
| `nginx.conf` | `/live/` proxy on the funlive.io vhost → `https://funlive.io/live/<key>.m3u8|.flv` (no mixed content; CORS for web.funlive.io players; merged with your VM-only `fun-live-icon` blocks) |
| `LiveDao.php` | `pushUrl` = `rtmp://funlive.io/live/<key>`, HLS/FLV/RTMP playback URLs repointed (all `*.quzhiboapp.com`/dead Aliyun hosts gone) |
| `LiveHooks.php` | Accepts SRS 6 JSON hook bodies; rejects publishes whose stream key has no live row |
| `RecordedVideoDao.php` | Fixed table name (`recorded_videos`) — pre-existing CI3→CI4 bug |

## Bugs found and fixed during verification
1. **CI4 debug toolbar corrupted the hook's `0` response** (28 KB of HTML appended in dev mode) → every publish was rejected by SRS. Fixed with a `text/plain` allow-response.
2. `recorded_video` → `recorded_videos` table name.

## Verified end-to-end (production)
- ffmpeg push → `on_publish ok ... response=0`; unknown key → denied ✅
- `https://funlive.io/live/<key>.m3u8` playlist + `.ts` segments ✅
- `https://funlive.io/live/<key>.flv` streaming ✅, CORS + `OPTIONS 204` preflight ✅
- Stop push → `on_unpublish` + `on_dvr` → `recorded_videos` row + FLV in `srs-data/` ✅
- 45-day retention cron added for DVR files (runs via container, handles root-owned files)
- Test streams, rows, and files cleaned up; repo committed & pushed (`6aa3bf3`, `a39d7e0`)

## How an anchor goes live now
In the live config screen: **URL** `rtmp://funlive.io/live` + **Stream Key** (the per-live key) in OBS → Start Streaming. Viewers (attended/owner) automatically get the new `https://funlive.io/...` URLs from the API — **no frontend changes needed**.

## Notes
- My local RTMP-out is blocked by your clash proxy, so the ingest test ran from the VM itself; the public 1935 path is open (`nc` OK) — worth one real OBS test from an anchor's machine.
- Phase 5 (replay): convert the DVR FLVs in `srs-data/` to HLS and upload to GCS (reusing `GcsStorage`), replacing the dead ssh2-based `RecordedVideos` pipeline. Say the word when you want it.