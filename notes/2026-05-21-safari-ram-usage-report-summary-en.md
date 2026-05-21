---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safari RAM Usage Report Summary
translated: false
type: note
---

Here's Safari's RAM usage:

| Process | RAM |
|---|---|
| **Safari** (main) | **339.5 MB** |
| Safari Platform Support Helper x3 | 20.7 / 23.8 / 23.8 MB |
| Safari History | 21.8 MB |
| Safari SandboxBroker | 26.5 MB |
| SafariBookmarksSyncAgent | 13.5 MB |
| Safari SearchHelper | 11.0 MB |
| Others (widget, import, agent, etc.) | 4-7 MB each |

TabsKiller runs inside one of the **SafariPlatformSupport.Helper** processes (the ~20-24 MB ones) — Safari hosts all web extensions there. The extension itself adds near-zero overhead since it's just:

- Background page: tab event listeners (`onCreated`, `onUpdated`, `onActivated`, `onRemoved`)
- Popup page: settings UI (only uses memory when opened)
- No timers, no network requests, no DOM manipulation

The extension is already working — since you said it's keeping only 10 tabs, the `checkToClose()` logic is running on each tab event. You can verify by checking the browser console or opening the popup to see your max tabs setting.