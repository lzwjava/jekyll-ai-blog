---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flarum Deployed on Google Cloud
translated: false
type: note
---

Done! 🎉 **Flarum is deployed and running in Google Cloud — Hong Kong (`asia-east2-a`).**

## Live site → **http://35.220.164.97**

### Verified working

| Check | Result |
|---|---|
| Forum homepage | HTTP 200, loads compiled JS/CSS |
| JSON API `/api/` | HTTP 200, forums resource served |
| Admin login | HTTP 200 — token issued |
| Assets `forum.js` | 673KB, HTTP 200 |

### Credentials (also saved in `/tmp/flarum-credentials.txt`)
- **Admin**: `admin` / `3a54beb179f36e90` → sign in at http://35.220.164.97/
