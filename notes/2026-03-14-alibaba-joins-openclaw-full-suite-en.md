---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alibaba Joins OpenClaw With Full Suite
translated: false
type: note
---

Question: Has Alibaba Cloud (Aliyun) released its own version of OpenClaw, similar to what Tencent and Kimi (Moonshot) have done?

Answer:

## Yes — Alibaba/Aliyun Has Fully Joined the OpenClaw Race

Alibaba is actually one of the most active players in the Chinese OpenClaw ecosystem right now. Here's a breakdown of everything they've launched:

---

### 1. 🦞 JVS Claw — Mobile App (Launched March 13, 2026)

Alibaba released **"JVS Claw"**, a mobile app for iOS and Android aimed at smartphone users without coding knowledge, allowing them to instruct AI agents to perform real-world tasks. It is free for the first 14 days. It came shortly after Baidu launched its own Android OpenClaw app, with Tencent and MiniMax also competing in the same space.

---

### 2. ☁️ One-Click Cloud Deployment via Simple Application Server (轻量应用服务器)

Alibaba Cloud supports deploying OpenClaw directly via their **Simple Application Server** (轻量应用服务器) using a one-click image deployment. The system automatically detects the nearest Model Studio endpoint and provides the API key. The default model as of early 2026 is **qwen3.5-plus**.

Tencent, Alibaba, Moonshot, and MiniMax are all offering their own tweaked versions of OpenClaw, and their stock prices have surged alongside the hype.

---

### 3. 📦 Coding Plan — Flat-Rate API Subscription for OpenClaw

Alibaba Cloud created a dedicated **"Coding Plan"** API subscription specifically for OpenClaw users, giving them access to Qwen models under a flat monthly fee rather than pay-as-you-go token billing.

The Coding Plan supports models including **qwen3.5-plus**, **qwen3-max**, **qwen3-coder-plus**, and even third-party models like **Kimi K2.5**, **MiniMax-M2.5**, and **GLM-5**, all accessible from OpenClaw via a single Alibaba Cloud API key.

---

### 4. 🛠️ Qwen Code — Their Claude Code Equivalent

Alibaba also has **Qwen Code**, a terminal-based coding agent (similar to Claude Code), which integrates with the Coding Plan. Users can run `/auth` and `/model` commands to switch between all models.

---

### Summary: Where Each Major Player Stands

| Company | OpenClaw Offering |
|---|---|
| **Alibaba / Aliyun** | JVS Claw mobile app + one-click ECS deploy + Coding Plan API |
| **Tencent Cloud** | One-click deploy + offline install booths |
| **Kimi (Moonshot)** | KimiClaw + Kimi K2.5 model integration |
| **Baidu** | Android app for OpenClaw |
| **ByteDance (Volcengine)** | Coding Plan subscription |

So if you're running OpenClaw on Aliyun, you get a pretty tight native integration — the server image, auto-detected API keys, and their Qwen models all work together out of the box.

References:

- [Alibaba Debuts OpenClaw App (Bloomberg)](https://www.bloomberg.com/news/articles/2026-03-13/alibaba-debuts-openclaw-app-to-feed-china-s-agentic-ai-addiction)
- [Alibaba Cloud OpenClaw Deployment Docs](https://www.alibabacloud.com/help/en/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)
- [Alibaba Cloud Coding Plan for OpenClaw](https://www.alibabacloud.com/help/en/model-studio/openclaw-coding-plan)
- [OpenClaw China Frenzy — Beyond Cloud Vendors (CIW)](https://www.ciw.news/p/openclaw-china-frenzy)
- [Tom's Hardware: OpenClaw craze in China](https://www.tomshardware.com/tech-industry/artificial-intelligence/openclaw-ai-agent-craze-sweeps-china-as-authorities-seek-to-clamp-down-amid-security-fears-adoption-surges-as-state-run-enterprises-are-barred-from-use)