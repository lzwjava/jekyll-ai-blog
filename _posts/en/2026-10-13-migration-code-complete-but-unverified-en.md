---
audio: false
generated: true
image: false
lang: en
layout: post
title: Migration Code-Complete but Unverified
translated: false
type: note
---

## Project: live-server (Fun Live 知识直播平台后端)

### What this is
PHP backend for a knowledge live-streaming platform (~80 lectures, 30k+ users historically), with Go integration tests in `test/`, Docker deployment, plus SRS/RTMP live config, WeChat/Alipay/Qiniu integrations.

### Main work stream: CodeIgniter 3 → CodeIgniter 4 migration
Per `MIGRATION_SUMMARY.md` / `README_MIGRATION.md` the migration is declared **"COMPLETED" at ~85%**:

| Area | Status |
|---|---|
| Config (25+ files in `app/Config/`, 145 routes, 448 constants) | ✅ 100% |
| Controllers (26, incl. new `Home`) | ✅ 100% |
| Models/DAOs (33) | ✅ 100% |
| CI3 compat layer (`CI3Compat.php`, payment stubs, CI4 libs for JSSDK/WeChat/Pay/Sms/LeanCloud) | ✅ |
| Docker (php:8.5-fpm + MySQL 5.7 + Redis 7 + nginx + optional Vite frontend build) | ✅ |
| Framework install / composer | ✅ done in the workspace copy |
| **Integration testing** | ⬜ **Pending** — checklist in MIGRATION_SUMMARY still shows 9/10 items unchecked (auth, lives, DB queries, WeChat, payments, uploads, Redis, routes, sessions) |

### Git status
- 10 commits, all from **Apr 5–7, 2026**, all pushed; `master` clean and in sync with `origin/master` (HEAD `4ce0cba`).
- Last 3 commits were polish: frontend build stage in docker-compose, `NODE_ENV` fix, `VITE_BASE_URL` + app port remap **8081 → 8082** (8081 taken by llama-server).
- **No commits since April 2026** (today is Oct 13, 2026) — project has been idle ~6 months.

### Current runtime status: ⚠️ All stopped
- All 5 compose containers (`app`, `database`, `redis`, `web`, `frontend`) **exited ~5 months ago** — nothing listening on 8082/8088/3005.
- Working tree at `/home/lzw/projects/live-server` is missing runtime files: **no `.env`, no `vendor/`, no `writable/`, no `composer.lock`** (all gitignored).
- The *real* runnable copy lives at `/home/lzw/.openclaw/workspace/live-server` — same commit, but has `.env` (WeChat/Qiniu/Alipay secrets), `vendor/` (root-owned), `writable/`, `composer.lock`. The old `app` container bind-mounts that path, not `projects/live-server`.
- Also missing: `../live-mobile-web` sibling repo that the `frontend` build service expects.
- Go tests (`test/*.go`, 26 files) target `http://localhost:3005/` — a stale port (current setup uses 8088 nginx / 8082 app), so they'd fail as-is.

### Bottom line
**Migration code-complete (~85%), but functionally unverified.** The stack is dark, the two repo copies have drifted (secrets/vendor only in the openclaw path), and the test suite points at a dead port. Highest-value next steps:

1. `docker compose up -d` (from the workspace copy) and smoke-test `GET /` + auth + `/lives/attended` endpoints
2. Reconcile the two checkouts — copy `.env`, `vendor/`, `writable/` or make `projects/` the canonical dir
3. Point `test/client.go` at the actual port and run the Go suite against live endpoints

Want me to bring the stack up and start running that verification checklist?