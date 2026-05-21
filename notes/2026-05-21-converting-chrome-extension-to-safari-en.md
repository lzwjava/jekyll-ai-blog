---
audio: false
generated: true
image: false
lang: en
layout: post
title: Converting Chrome Extension to Safari
translated: false
type: note
---

Here's a summary of everything that was done:

---

## Converted TabsKiller from Chrome Extension → Safari Extension

### Project structure

```
safari-tabs-killer/         ← original source, now Safari-compatible too
TabsKiller/                 ← generated Xcode project (builds successfully)
├── TabsKiller.xcodeproj
├── TabsKiller/
│   ├── AppDelegate.swift
│   ├── ViewController.swift
│   ├── Main.storyboard
│   └── Resources/            ← empty app shell resources
└── TabsKiller Extension/
    ├── SafariWebExtensionHandler.swift   ← native message bridge
    ├── Info.plist                        ← identifies as Safari web extension
    └── Resources/
        ├── manifest.json                 ← same manifest, works in Safari
        ├── background.html / background.js
        ├── popup.html / popup.js
        └── js/                           ← tabmanager.js, settings.js, libs
```

### What changed in the source code

| File | Change |
|---|---|
| `js/settings.js` | `chrome.storage.sync` → `chrome.storage.local` (Safari doesn't support sync storage) |
| `js/settings.js` | Default whitelist: `['chrome://*']` → `[]` (Chrome-only scheme) |
| `README.md` | Updated docs for Safari install instead of Chrome Web Store |

### How to build & run

```bash
# Open Xcode (or use the command line)
open /Users/lzwjava/projects/projects/TabsKiller/TabsKiller.xcodeproj

# In Xcode:
# 1. Select your development team in Signing & Capabilities
# 2. Product → Run (or Cmd+R)

# Or via CLI:
cd /Users/lzwjava/projects/projects/TabsKiller
xcodebuild -project TabsKiller.xcodeproj -scheme TabsKiller build

# Then find the app and run it (or run from Xcode)
```

Once launched, the app registers the extension in Safari. Go to **Safari → Settings → Extensions** and enable "Tabs Killer".

### Convert again from scratch (if needed)

```bash
xcrun safari-web-extension-converter safari-tabs-killer \
  --app-name "TabsKiller" \
  --bundle-identifier "com.lzw.TabsKiller" \
  --macos-only --force --no-prompt --copy-resources
```

A backup of the original Chrome-only code is at `safari-tabs-killer-backup/`.