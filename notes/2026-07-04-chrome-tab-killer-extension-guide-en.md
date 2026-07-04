---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chrome Tab Killer Extension Guide
translated: false
type: note
---

You're right. `chrome-tab-killer/` is the correct one — it's just the Chrome extension without the Safari Xcode wrapper (`safari-tab-killer/` has both).

```
/home/lzw/projects/tab-killer/chrome-tab-killer/
├── manifest.json
├── background.js / background.html
├── popup.html / popup.js
├── js/tabmanager.js
├── js/settings.js
├── css/popup.css
└── img/
```

Load this in Chromium:

1. Open `chrome://extensions`
2. Enable **Developer mode**
3. **Load unpacked** → select `/home/lzw/projects/tab-killer/chrome-tab-killer`

The extension will start immediately. Click its icon to set your max tab limit and whitelist.

Want me to open Chromium and walk through it together, or just hand it off?
