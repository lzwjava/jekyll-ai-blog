---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Port Security Audit Summary
translated: false
type: note
---

Here's the breakdown, Boss:

| Port | Service | Listening | Exposed To |
|------|---------|-----------|------------|
| **22** | sshd | ✅ | Anywhere |
| **80** | nginx | ✅ | Anywhere |
| **3001** | docker-proxy | ✅ | Anywhere |
| **5000** | — | ❌ not listening | Anywhere (rule exists) |
| **7890** | mihomo (proxy) | ✅ | Anywhere (docker0) |
| **8080** | docker-proxy | ✅ | Anywhere |
| **11434** | ollama | ✅ | localhost only |
| **18789** | openclaw-gateway | ✅ | localhost + 192.168.1.0/24 |

**Observations:**

- **Port 5000/tcp** has a ufw rule but nothing's actually listening — might be leftover from a stopped Nextcloud container?
- **Port 3001** and **8080** are wide open to the internet via Docker. These likely map to LibreChat and Nextcloud respectively.
- **7890 on docker0** is SearXNG's mihomo proxy — marked as allowed but your SearXNG shows 0% uptime, so something's off there.
- **Ollama (11434)** is correctly locked to localhost only.
- **OpenClaw (18789)** is nicely scoped to LAN only.

Want me to dig into the SearXNG issue, or tighten up any of these rules?
