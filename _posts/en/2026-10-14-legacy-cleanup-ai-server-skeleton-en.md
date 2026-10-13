---
audio: false
generated: true
image: false
lang: en
layout: post
title: Legacy cleanup, AI server skeleton
translated: false
type: note
---

Committed and pushed to `master` (`4db3aac`, 41 files, +2067/−2938):

- **Cleanup**: legacy webpack build, plupload submodule, unused components removed
- **New**: `ai-server/index.js` (SSE chat service with retrieval) and `ai-server/ingest.js`

Two notes:

1. **GitHub flagged 141 dependency vulnerabilities** on the default branch (2 critical, 61 high) — mostly from the old dependency tree. Worth a `npm audit` pass later.
2. **The RAG demo is only half-wired** — remaining pieces when you pick it back up: seed corpus JSON, `/ai` proxy in `vite.config.js`, the "助手" tab in `LiveView`, and the streaming `AssistantPanel.vue` component.
