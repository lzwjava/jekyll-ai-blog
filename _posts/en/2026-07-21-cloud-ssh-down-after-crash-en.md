---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloud SSH Down After Crash
translated: false
type: note
---

**External IP 36.150.116.206 scan results:**

| Port | Status | What |
|------|--------|------|
| 31090 | ✅ **Open** | Cloud SSH (other instance) |
| 31091 | ✅ **Open** | Cloud SSH (other instance) |
| 31092 | ✅ **Open** | Cloud SSH (other instance) |
| 31095 | ✅ **Open** | Cloud SSH (other instance) |
| 31098 | ✅ **Open** | Cloud SSH (other instance) |
| 31099 | ✅ **Open** | Cloud SSH (other instance) |
| 31100 | ✅ **Open** | Cloud SSH (other instance) |
| 31154 | ❌ **Refused** | **Our SSH — still down** |
| 22, 80, 443, 8000, 8888 | ❌ Refused | All blocked |

**Port 31154 is still not being forwarded by the cloud proxy** after the OOM crash. The cloud provider needs to remap it.

**Just use the Jupyter terminal** for now — it works fine. Want me to guide you through running FLUX.1-dev there?
