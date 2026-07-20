---
audio: false
generated: true
image: false
lang: en
layout: post
title: Team Knowledge Governance Platform
translated: false
type: note
---

This is a **Team Knowledge Base** (团队知识库) — a full-stack web application for managing and governing team knowledge, built around a layered knowledge model.

**Stack:**

- **Backend**: Python FastAPI (controllers, services, middlewares, SQL database)
- **Frontend**: Vue 3 + TypeScript + Vite + Vue Router
- **Storage**: Markdown files in a Git repo with machine-validated JSON metadata blocks

**Knowledge layers** (the core organizing concept):

| Layer | Description |
| ------- | ------------- |
| Layer 0-P | Personal experience |
| Layer 0-T | Team conventions |
| Layer 1 | Technical knowledge |
| Layer 2 | Business knowledge |
| Layer 3 | Project knowledge |

**Knowledge types**: model, decision, guideline, pitfall, process

**Features** (from the routes and views):

- Knowledge creation with a guided flow (create → preview → complete)
- Knowledge browsing with layer/category filtering
- Permission management (reader / contributor / maintainer / super_admin roles)
- Super admin panel
- Member management & business domain management
- Preview tokens for sharing knowledge externally
- Governance CLI tool (`knowledge_governance.py`) for file-based validation
- Audit logging

**Already populated**: The `tech-wiki/` directory has 18 knowledge entries — decisions (e.g., "Python 3.12", "Vue 3 + TypeScript"), guidelines (e.g., "hidden mirror layer scheme", "bash one-click dev script"), patterns, anti-patterns, and pitfalls — all maintained as Markdown with machine-parseable metadata.

Basically it's a **knowledge governance platform** — a structured wiki system where knowledge is treated as code (stored in Git, reviewed, versioned) with a web UI for injection and browsing, plus a CLI tool for governance enforcement.
