---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Relay Service Explained
translated: false
type: note
---

**Question:** What is the platform of pincc.ai, and what does it do? Also, what is the GitHub project at https://github.com/Wei-Shaw/claude-relay-service?

**Answer:**

## pincc.ai — Platform Overview

**pincc.ai** is the official documentation and support website for **Claude Relay Service (CRS)** — a self-hosted, open-source AI API relay/proxy service. It is **not** related to the medical NGO "PINCC" (Preventing Cervical Cancer), which is a completely separate organization.

---

## What is Claude Relay Service (CRS)?

CRS is a self-hosted Claude API relay service with multi-account management. It is designed to solve three main problems: regional restrictions where users can't directly access Claude Code, privacy concerns about third-party mirror services, and the desire to share Claude Code Max subscription costs with others (cost sharing / "carpool").

In short, CRS acts as a **middleware proxy** that sits between AI clients and the actual AI APIs.

---

## What Does It Do?

Claude Relay Service is a multi-platform AI API relay service supporting Claude (Official/Console), Gemini, OpenAI Responses (Codex), AWS Bedrock, Azure OpenAI, Droid (Factory.ai), CCR, and other account types. It provides complete multi-account management, API Key authentication, proxy configuration, user management, LDAP authentication, Webhook notifications, and a modern Web management interface. The service acts as middleware between clients (such as Claude Code, Gemini CLI, Codex, Droid CLI, Cherry Studio, etc.) and AI APIs, providing authentication, rate limiting, monitoring, pricing calculation, and cost statistics.

Key features include:

- **Unified scheduler**: Intelligently routes requests across multiple accounts and platforms
- **Cost sharing / "carpool"**: Multiple users share one Claude subscription to split costs
- **Client restriction**: Controls which clients (by User-Agent) can use each API key
- **Usage statistics**: Tracks input/output tokens and calculates costs per user
- **Web management UI**: A dashboard for managing accounts, keys, and users

---

## GitHub Repo (Wei-Shaw/claude-relay-service)

The repository has over 9,200 stars and 1,400+ forks on GitHub, showing strong community adoption. The latest release as of early March 2026 is v1.1.292.

**Tech stack:** Node.js 18+, Redis, Docker-compatible.

**Deployment options** (from pincc.ai docs):
- One-click script install (`crs` command-line tool)
- Docker / Docker Compose
- Manual deployment via `git clone` + `npm install`

**Important disclaimer from the project itself:** Using this project may violate Anthropic's terms of service. The author is not responsible for any account bans, service interruptions, or other losses, and states the project is for technical learning and research purposes only.

---

## Summary

| Item | Details |
|---|---|
| **Platform** | pincc.ai — docs/portal for Claude Relay Service |
| **Core function** | Self-hosted AI API proxy/relay |
| **Supported AIs** | Claude, OpenAI, Gemini, AWS Bedrock, Azure, Droid |
| **Key use case** | Multi-account management + cost sharing ("carpool") |
| **Tech** | Node.js + Redis, deployable via script or Docker |
| **Risk** | May violate Anthropic ToS — use at your own risk |

**References:**

- [pincc.ai Deployment Guide](https://pincc.ai/en/installation)
- [GitHub: Wei-Shaw/claude-relay-service](https://github.com/Wei-Shaw/claude-relay-service)
- [GitHub README (English)](https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md)