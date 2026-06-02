---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp AI Default Model Configuration
translated: false
type: note
---

**Question:** What AI model does Warp use by default when no model is configured?**Answer:**

Warp's built-in AI (branded as **"Warp AI"**) routes queries through **Warp's own servers**, so you don't need to configure an API key yourself — they handle the model backend for you.

As of 2026, Warp AI is powered by **Oz** (Warp's orchestration layer) integrated with OpenAI models. It supports frontier models including Claude Opus 4.5, GPT-5.2, and Gemini 3 Pro, with bring-your-own-API-key on paid plans.

So by default with no configuration, you're hitting **Warp's hosted backend (Oz + OpenAI)** — the specific model depends on your tier, but free tier users get a default model selected by Warp. You can check `Settings → AI` in Warp to see exactly which model is active for your account.

Note that queries go through Warp's servers by default, which is worth being aware of for anything sensitive (bank work, etc.).
