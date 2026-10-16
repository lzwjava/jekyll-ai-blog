---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Goofish.com: React, Not Flutter"
translated: false
type: note
---

**Question:** Is goofish.com (the Xianyu web version) built with Flutter?

**Answer:**

**No**, `goofish.com` is **not** built with Flutter Web. It's a traditional web application.

Here's how I can tell from inspecting the page source:

### ❌ No Flutter Web signatures found:
A Flutter Web app always leaves clear fingerprints in the HTML:
- `flutter.js` bootstrap script
- `main.dart.js` compiled Dart code
- `flutter_service_worker.js`
- `CanvasKit` WASM loading
- `flt-` prefixed DOM elements

None of these are present on `goofish.com`.

### ✅ What it actually uses:
Looking at the page source, there's a telling clue:

```
meta-ice-meta-count: 0
```

The `ice` prefix points to **[ICE.js](https://ice.work/)** — Alibaba's own internal React-based frontend framework (also known as `icejs` or `AppWorks`). The web version is a standard **React + SSR (Server-Side Rendered)** app, which also explains why it has proper SEO meta tags (Baidu verification, Google verification, keywords, description) — Flutter Web CanvasKit mode renders into a `<canvas>` and is essentially invisible to search engines.

### Summary:

| Platform | Technology |
|---|---|
| 📱 Xianyu iOS/Android app | ✅ Flutter |
| 🌐 goofish.com website | ❌ React + Alibaba ICE.js (not Flutter) |

This is a very common pattern — companies use Flutter for their **mobile apps** but keep a separate **traditional web stack** for the website, mainly because Flutter Web still has limitations around SEO and initial load performance for content-heavy e-commerce sites.
