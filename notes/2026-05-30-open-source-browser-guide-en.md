---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Source Browser Guide
translated: false
type: note
---

**Question:** What are good open source browsers to use, and does Safari open source any of its components?

**Answer:**

## Open Source Browsers Worth Using

### Tier 1 — Daily-driver quality

**Firefox** (Mozilla)
- Fully open source (MPL 2.0), own engine: **Gecko** + **SpiderMonkey** (JS)
- Repo: [github.com/mozilla/gecko-dev](https://github.com/mozilla/gecko-dev)
- Only major non-Chromium engine left standing (besides WebKit)
- Good for: privacy, devtools, extensions, non-Google engine diversity

**Brave**
- Open source (MPL 2.0), Chromium-based (Blink engine)
- Repo: [github.com/brave/brave-browser](https://github.com/brave/brave-browser)
- Brave blocks harmful advertising, tracking pixels and cookies, and redirects sites to HTTPS. Available for macOS, Windows, and Linux.
- Many now argue that Brave has taken Firefox's former top spot in the open source world.
- Good for: daily use, built-in ad block, Chromium compat, no Google tracking

**Chromium**
- The upstream of Chrome, fully open source
- Repo: [chromium.googlesource.com/chromium/src](https://chromium.googlesource.com/chromium/src)
- Good for: debugging web apps exactly as Chrome renders them, without Google telemetry

### Tier 2 — Developer/Niche

**ungoogled-chromium**
- Chromium with all Google API calls stripped
- Repo: [github.com/ungoogled-software/ungoogled-chromium](https://github.com/ungoogled-software/ungoogled-chromium)

**Ladybird** (most exciting technically)
- A new browser built on a completely original engine — shares no code with Blink, WebKit, Gecko, or any other existing engine. Non-profit backed, funded entirely through donations and sponsorships, with no search deals, no data collection, and no advertising. A first Alpha release is targeting Linux and macOS in 2026, aimed at developers and early adopters. Eight full-time engineers are working on it alongside community contributors. Recent updates include an inline PDF viewer, browsing history, HTTP caching, media streaming, CSS anchor positioning, off-thread JS compilation, and a new regex engine.
- This is the most architecturally interesting one right now — worth watching.

---

## Safari and Open Source

Safari itself (the app shell, UI, sync, etc.) is **closed source proprietary**. But its two core engines are open source:

**WebKit** — the rendering/layout engine
- WebKit is an open source web content engine for browsers and other applications. Apple developed and open-sourced it. The WebKit project prioritizes real-world web compatibility, standards compliance, stability, performance, battery life, security, privacy, portability, and hackability.
- Repo: [github.com/WebKit/WebKit](https://github.com/WebKit/WebKit)
- License: LGPL 2.1 (WebCore) + BSD (JavaScriptCore)

**Components inside WebKit:**
- **WebCore** — HTML/CSS layout and rendering (the DOM, painting pipeline)
- **JavaScriptCore (JSC)** — Apple's JS engine, equivalent to V8/SpiderMonkey
- Both have been open since 2005. In June 2005, Apple announced it was open-sourcing the entirety of WebKit (previously only WebCore and JavaScriptCore were open source), reportedly as part of an effort to work more closely with KDE and the open-source community.

**What's closed:** Safari's UI, iCloud sync, Handoff, Keychain integration, Private Relay — all proprietary.

---

## Quick Reference

| Browser | Engine | Open Source | Notes |
|---|---|---|---|
| Firefox | Gecko/SpiderMonkey | ✅ Full | Only major non-Blink/WebKit engine |
| Brave | Blink/V8 | ✅ Full | Best daily-driver for privacy |
| Chromium | Blink/V8 | ✅ Full | Chrome upstream |
| ungoogled-chromium | Blink/V8 | ✅ Full | Chromium - Google telemetry |
| Ladybird | LibWeb (custom) | ✅ Full | New from scratch, alpha 2026 |
| Safari | WebKit/JSC | ❌ App, ✅ Engine | WebKit/JSC are open source |
| Chrome | Blink/V8 | ❌ Closed | Built on open Chromium |

**My recommendation for you:** Brave or ungoogled-chromium for daily use. Ladybird is worth cloning and running just to see what building a browser engine from scratch looks like — very Karpathy-style learning.

References:
- [WebKit Open Source Project](https://webkit.org/)
- [Apple Open Source — WebKit](https://opensource.apple.com/projects/webkit/)
- [Ladybird Browser](https://openalternative.co/alternatives/brave)