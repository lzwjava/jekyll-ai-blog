---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Health and Container Status Report
translated: false
type: note
---

Here's the full picture:

---

## 🖥️ Server Health Summary

**Load / CPU**

- Load: **0.50** (was 11 — fan issue resolved ✅)
- CPU: **99% idle**, 6GB / 62GB RAM used, 56GB available
- **Swap**: 107MB / 2GB — healthy

---

## 📊 Disk — ⚠️ 84% Used (142GB Free)

| Category | Size |
| --- | --- |
| Total | 916GB |
| Used | 728GB |
| Available | 142GB |

**Problem:** Not critical yet, but 84% is getting high for a root partition with Docker.
**Actionable reclaimables:**

- 22.9GB unused images (62% of images are reclaimable)
- 220MB stopped container writable layers
- 73MB build cache

**Recommendation:** Run `docker system prune -a` to clean up old image versions. Or at minimum `docker image prune -a`.

---

## 🐳 All Containers Running (19/19)

| Container | CPU | RAM | Status |
| --- | --- | --- | --- |
| nextcloud-app-1 | 0% | 206MB | ✅ Healthy |
| nextcloud-db-1 | 0% | 67MB | ✅ Healthy |
| nextcloud-redis-1 | 1% | 7MB | ✅ Healthy |
| live-server-app-1 | 0% | 21MB | ✅ Running |
| live-server-web-1 | 0% | 22MB | ✅ Running |
| live-server-database-1 | 0.1% | 183MB | ✅ Running |
| live-server-redis-1 | 1% | 5MB | ✅ Running |
| immich_server | 0.3% | 485MB | ✅ Healthy |
| immich_postgres | 0% | 147MB | ✅ Healthy |
| immich_machine_learning | 0.2% | 251MB | ✅ Healthy |
| immich_redis | 0.5% | 16MB | ✅ Healthy |
| LibreChat | 0% | 240MB | ✅ Running |
| gitea | 0.2% | **980MB** | ⚠️ High RAM |
| chat-mongodb | 0.8% | 151MB | ✅ Running |
| chat-meilisearch | 0.6% | 133MB | ✅ Running |
| rag_api | 0.2% | 141MB | ✅ Running |
| vectordb | 0% | 43MB | ✅ Running |
| searxng | 0% | 133MB | ✅ Running |
| uptime-kuma | 2% | 162MB | ✅ Healthy |

---

## 🔴 Non-Critical Issues Found

### 1. **Gitea — High RAM (980MB)**

Gitea is using nearly 1GB of RAM, the most of any container. This is unusual — it may be doing a git gc or reindex. Check if it's just temporarily high or consistently growing.

### 2. **SearXNG — wikidata engine failed to init**

```
ERROR: wikidata (init failed)
```

This is a third-party engine that failed. SearXNG still works for other engines, but you may want to disable wikidata in settings.

### 3. **LibreChat — Meilisearch config missing**

```
[indexSync] error Meilisearch configuration is missing
```

Meilisearch is running (chat-meilisearch container is up) but LibreChat's indexer isn't connecting properly. May need to reconfigure the Meilisearch URL in LibreChat env.

### 4. **llama endpoint /health → 404**

`GET http://localhost:8081/api/v1/health` returns 404 — jellyfin is fine at port 8096. The llama/Ollama health endpoint might be at a different path.

### 5. **Nextcloud 33.0.2** ✅

Upgraded from 33.0.0. Uptime-Kuma now polling `/status.php` instead of `/apps/dashboard/`. Load is normal.

---

## 📋 Quick Action Items

| Priority | Task | Command |
| --- | --- | --- |
| Medium | Clean up 22.9GB unused images | `docker system prune -a` |
| Low | Monitor Gitea RAM (980MB) | `docker stats gitea` |
| Low | Fix LibreChat Meilisearch sync | Check LibreChat env `MEILISEARCH_` vars |
| Low | Disable wikidata in SearXNG | SearXNG settings UI |
| Info | Nextcloud DB backup | `/home/lzw/backup-nextcloud-db-20260407_165943.sql` |

Want me to tackle any of these?
