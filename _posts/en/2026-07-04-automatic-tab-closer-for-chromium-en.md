---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automatic Tab Closer for Chromium
translated: false
type: note
---

This project **can** help with Chromium here. It's a Chrome extension under `safari-tab-killer/` — Chromium supports Chrome extensions natively. The Safari Xcode stuff is just a macOS wrapper around the same extension logic.

**What it does:** Automatically closes the oldest tabs when your tab count exceeds a configured `maxTabs` limit. Whitelist URLs are protected. Configurable via the popup UI.

**How to load it into Chromium (on this machine):**

```bash
chromium-browser
```

Then in Chromium:

1. Navigate to `chrome://extensions`
2. Enable **Developer mode** (toggle top-right)
3. Click **Load unpacked**
4. Select `/home/lzw/projects/tab-killer/safari-tab-killer/`

That's it. The extension will start running. Default max tabs is probably undefined (needs to be set in the popup). Click the extension icon to configure:

- **Max tabs** — how many tabs before the killer kicks in
- **Whitelist** — URL patterns to never auto-close (e.g., `github.com`, `mail.google.com`)

Want me to also check what Chromium extensions are currently installed, or open it and load the extension directly?
