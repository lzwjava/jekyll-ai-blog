---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Relay Services Outside China
translated: false
type: note
---

Question: Are there Claude Code relay services in Europe or South Asia similar to China ones like pincc-v2 or ssssai code?

Answer:

Yes — but outside China, **Claude Code relay services are mostly open-source proxies or small community relays**, not large commercial “carpool” platforms like Chinese ones. Here are the main categories:

---

# 1) Direct equivalents to pincc-v2 (self-hosted relay / pooling)

These work globally (Europe / South Asia OK):

### 1. Claude Relay Service (CRS / pincc-style)

* Self-hosted relay for Claude / OpenAI / Gemini
* Supports **account rotation + pooling + cost sharing**
* Compatible with **Claude Code CLI**
* Docker one-click deploy
* Often used by teams instead of buying shared accounts

This is essentially the same architecture as pincc-v2. ([Claude Relay Service][1])

---

### 2. claude-code-proxy (LiteLLM backend router)

* Translates Claude API → OpenAI / Gemini
* Works as drop-in Claude Code relay
* Used to swap models behind Claude Code

This is more technical but very flexible. ([SourcePulse][2])

---

### 3. LunaRoute (local relay + session capture)

* Local proxy for Claude Code / Codex CLI
* Zero-latency passthrough
* Full session recording + debugging
* Works anywhere (EU/Asia)

Useful if you want **private relay instead of shared service**. ([GitHub][3])

---

# 2) Community relay services (non-China but smaller)

These are similar to ssssai-code style:

### EasyClaude (commercial relay)

* Ready-to-use Claude Code relay
* pooled plans
* no setup required
* enterprise isolation

This is basically **hosted relay like Chinese carpool sites**. ([Easy Claude Code - Claude Code 中转服务][4])

---

# 3) Newer community proxies (Reddit / dev communities)

These are emerging globally:

* **RelayCode** — local proxy swapping Claude to DeepSeek/Qwen
* **CC-Relay** — multi-provider load balancing proxy
* **tingly-box** — desktop Claude Code router

Example developer description:

> “RelayCode runs a local proxy… switch Claude Code to open-weights models.” ([Reddit][5])

---

# Region availability

These **all work in Europe / South Asia** because they are:

* self-hosted
* local proxy
* VPS-deployable
* no region lock

Unlike Chinese services, they usually **don’t advertise region** — you just deploy on:

* EU VPS (Hetzner / OVH)
* India VPS
* Singapore VPS
* home server

---

# Why China has more of these

You probably noticed:

China:

* pincc-v2
* ssssai code
* aigocode
* sub2api
* CRS
* carpool sites

Outside China:

* mostly open source
* fewer shared-account resellers
* more DIY

Because:

* payment access issues in China
* heavy dev demand
* community group buying culture

---

# Best options (outside China)

If you want same experience:

Most similar:

* Claude Relay Service (CRS)
* EasyClaude (hosted)

Most powerful:

* LunaRoute
* CC-Relay
* claude-code-proxy

Most lightweight:

* RelayCode
* tingly-box

---

If you tell me:

* want hosted (like ssssai)
* or self-hosted
* or cheapest pooling
* or fastest

…I can recommend the **best one**.

[1]: https://pincc.ai/en/?utm_source=chatgpt.com "Claude Relay Service - Self-hosted Claude API Relay | Claude Code Tutorial"
[2]: https://www.sourcepulse.org/projects/2336256?utm_source=chatgpt.com "claude-code-proxy by 1rgs - SourcePulse"
[3]: https://github.com/erans/lunaroute?utm_source=chatgpt.com "GitHub - erans/lunaroute: LunaRoute is a high-performance local proxy for AI coding assistants like Claude Code, OpenAI Codex CLI, and OpenCode. Get complete visibility into every LLM interaction with zero-overhead passthrough, comprehensive session recording, and powerful debugging capabilities."
[4]: https://easyclaude.com/en?utm_source=chatgpt.com "Claude Code Relay Service | Vibe Coding Platform | Easy Claude Code"
[5]: https://www.reddit.com/r/vscode/comments/1s4o8fi/route_claude_codecopilot_through_opensource/?utm_source=chatgpt.com "Route Claude Code/Copilot through Open-Source models with one click (RelayCode)"
