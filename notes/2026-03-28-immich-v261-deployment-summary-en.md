---
audio: false
generated: true
image: false
lang: en
layout: post
title: Immich v2.6.1 Deployment Summary
translated: false
type: note
---

Immich v2.6.1 is live and responding. Here's the rundown:

**✅ Running — `http://192.168.1.36:2283`**

| Container | Status |
|---|---|
| immich_server | Starting up |
| immich_postgres | Healthy ✅ |
| immich_redis | Starting |
| immich_machine_learning | Starting (face recognition, search) |

**What's configured:**
- **Version:** v2.6.1 (pinned)
- **Timezone:** Asia/Hong_Kong
- **Photo storage:** `~/immich-app/library`
- **DB password:** random 20-char alphanumeric
- **Port:** 2283

**Next steps:**
1. Open `http://192.168.1.36:2283` in your browser
2. Create the admin account
3. Install the Immich mobile app (iOS/Android) — it'll auto-backup your photos over WiFi
4. The ML container will start indexing faces and objects after you upload some photos

Want me to set up a reverse proxy with HTTPS for external access, or is local-only fine for now?
