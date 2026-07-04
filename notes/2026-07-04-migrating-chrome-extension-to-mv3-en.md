---
audio: false
generated: true
image: false
lang: en
layout: post
title: Migrating Chrome Extension to MV3
translated: false
type: note
---

Done. The extension is ported from MV2 → MV3. Here's what changed:

**`manifest.json`** — MV2 (`browser_action`, `background.page`) → MV3 (`action`, `background.service_worker`), dropped `content_security_policy` (MV3 doesn't allow `unsafe-eval` and it's not needed now)

**`background.js`** — Was a page-based background using RequireJS + `background.html`. Now it's a service worker. Uses `importScripts('js/lib/underscore.js')`, inlines the tab-manager and settings logic directly. No DOM, no `window`, no RequireJS.

**`popup.js`** — Replaced `chrome.extension.getBackgroundPage().GlobalObject.settings.get()` with direct `chrome.storage.sync.get/set` calls. No background page dependency. Also replaced `_.template()` with plain jQuery DOM construction (avoiding `unsafe-eval`).

**Removed** — `background.html`, `app.build.js`, `js/require.js`, `js/tabmanager.js`, `js/settings.js` (all dead code in MV3)

Now load it in Chromium:

1. `chrome://extensions` → **Developer mode** (top-right) → **Load unpacked**
2. Select `/home/lzw/projects/tab-killer/chrome-tab-killer`
3. Click the extension icon to set max tabs and whitelist