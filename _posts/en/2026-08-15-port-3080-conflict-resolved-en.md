---
audio: false
generated: true
image: false
lang: en
layout: post
title: Port 3080 Conflict Resolved
translated: false
type: note
---

Done. ✅

**What happened:** Port 3080 wasn't held by a stray process — it was the **LibreChat** Docker container publishing `0.0.0.0:3080->3080/tcp`, which conflicted with your `dsh-app-boot` (DeepSeek app).

**Fix applied:** `docker stop LibreChat` — port 3080 is now free.

**Notes:**
- To bring LibreChat back: `docker start LibreChat`
- If you want both running simultaneously, change LibreChat's port mapping in its docker-compose (e.g., `3081:3080`) and re-create the container: `docker compose up -d`
- The `CLOSE_WAIT` entries from Chrome earlier were just stale connections to the old listener and are harmless.

You can now re-run your DeepSeek app.