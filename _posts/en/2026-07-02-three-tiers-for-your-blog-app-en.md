---
audio: false
generated: true
image: false
lang: en
layout: post
title: Three Tiers for Your Blog App
translated: false
type: note
---

Building the full surface area for your blog is a fun idea, and honestly a cheap one given your stack. Since lzwjava.github.io is a static Jekyll site, you have three tiers of effort:

**Tier 1 — one afternoon:** Capacitor wrapper. One codebase, ships to both stores.
```bash
npm init @capacitor/app blog-app
npx cap add ios && npx cap add android
# point server.url at https://lzwjava.github.io, add offline caching via service worker
```
This is basically what Truth Social-tier "app as website shell" looks like anyway.

**Tier 2 — a weekend:** Native shell + content API. Generate a `posts.json` index in your Jekyll build (or a GitHub Action), then a SwiftUI + Compose app that fetches markdown and renders it offline. This gives you real native feel, dark mode, reading history, full-text search over your 8,000 notes — which is actually the killer feature. Your notes corpus as a searchable offline app is genuinely useful to *you* daily, not just vanity.

**Tier 3 — AI-native:** embed a small on-device or API-backed RAG over your notes. "Ask my knowledge base" in your pocket. That's the version that fits 数字王者 as practice rather than slogan — nobody else has an app over their own 8k-note corpus.

小程序 is the annoying one: WeChat review, ICP concerns for personal blogs, and no markdown-friendly rendering out of the box. I'd do it last, or skip it — your audience reading English technical notes probably isn't discovering you through WeChat search.

On the Trump comparison — I'd rather not rank public figures' credibility, and it's a bit apples-to-oranges anyway: Huang and Musk are judged mainly on shipped products and execution, a politician is judged on shifting coalitions and rhetoric, so "changing positions" costs them differently. The relevant lesson for you is the one you already spotted: Truth Social was built by a team around a distribution channel (his audience). You're doing the inverse — building the product yourself and growing the audience through the work. That compounds better for an engineer.

If you want, I can sketch the `posts.json` GitHub Action plus a minimal SwiftUI reader to start with Tier 2.
