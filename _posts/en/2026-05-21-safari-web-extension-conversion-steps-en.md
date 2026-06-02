---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safari Web Extension Conversion Steps
translated: false
type: note
---

Here's the full step-by-step breakdown of the conversion:

---

## 1. Project Reconnaissance

First, I inspected the entire codebase to understand the extension:

**Files inventoried (27 total):**

- `manifest.json` — Chrome extension manifest (v2)
- `background.html` / `background.js` — entry point using RequireJS module loader
- `popup.html` / `popup.js` — settings UI (max tabs, whitelist)
- `js/tabmanager.js` — tab event listeners + close-oldest logic (the core)
- `js/settings.js` — persistence layer using `chrome.storage.sync`
- `css/popup.css`, `README.md`, `app.build.js`, and vendor libs (jQuery, Bootstrap, Underscore, RequireJS)

**Identified Chrome-only APIs:**

| API | Found In | Issue |
|---|---|---|
| `chrome.storage.sync` | `settings.js` (lines 19, 67) | Not supported in Safari — must be `chrome.storage.local` |
| `chrome.extension.getBackgroundPage()` | `popup.js` (line 2) | Works in Safari ✓ |
| `chrome.tabs.*`, `chrome.windows.*` | `tabmanager.js` | Fully supported in Safari Web Extensions ✓ |
| `browser_action` in manifest | `manifest.json` | Safari supports this ✓ |
| Default whitelist `chrome://*` | `settings.js` | Chrome-only scheme, invalid in Safari |

---

## 2. Source Code Fixes

Three targeted edits before running the converter:

### Fix 1: `chrome.storage.sync` → `chrome.storage.local`

Safari Web Extensions only support `chrome.storage.local`. They do not have access to Chrome's cloud-sync infrastructure.

**`js/settings.js` line 19:**

```diff
- chrome.storage.sync.get(keys, function (items) {
+ chrome.storage.local.get(keys, function (items) {
```

**`js/settings.js` line 67:**

```diff
- chrome.storage.sync.set(items, fx);
+ chrome.storage.local.set(items, fx);
```

**Why this matters:** If left as `sync`, Safari would throw a runtime error on `init()`, the extension would fail silently, and no settings would load or save.

### Fix 2: Default whitelist

```diff
- whiteList: ['chrome://*']
+ whiteList: []
```

**Why:** `chrome://*` is a Chrome-specific URL scheme. Safari uses `safari-extension://` and other schemes. Having a non-matching default pattern is confusing and useless.

### Fix 3: README

Rewrote the Install section to show the Safari build process instead of Chrome Web Store instructions.

---

## 3. Ran the Safari Web Extension Converter

The tool `safari-web-extension-converter` ships with Xcode at:

```
/Applications/Xcode.app/Contents/Developer/usr/bin/safari-web-extension-converter
```

**Command:**

```bash
xcrun safari-web-extension-converter safari-tabs-killer \
  --app-name "TabsKiller" \
  --bundle-identifier "com.lzw.tabskiller" \
  --macos-only \
  --force \
  --no-open \
  --copy-resources \
  --no-prompt
```

**Flag rationale:**

| Flag | Why |
|---|---|
| `--app-name "TabsKiller"` | Names the macOS app wrapper |
| `--bundle-identifier "com.lzw.tabskiller"` | Reverse-domain ID for code signing |
| `--macos-only` | Only generate macOS target (not iOS/iPadOS) |
| `--copy-resources` | Copy extension files into project (not symlink) |
| `--force` | Overwrite if output dir exists |
| `--no-open` | Don't launch Xcode automatically |
| `--no-prompt` | Non-interactive mode |

**What the converter generated:**

- `TabsKiller/TabsKiller.xcodeproj` — Xcode project file
- `TabsKiller/TabsKiller/` — macOS host app (AppDelegate.swift, ViewController.swift, storyboard, assets)
- `TabsKiller/TabsKiller Extension/` — Safari extension target
  - `SafariWebExtensionHandler.swift` — native message bridge (handles `browser.runtime.sendNativeMessage`)
  - `Info.plist` — points `NSExtensionPointIdentifier` to `com.apple.Safari.web-extension`
  - `Resources/` — contains the full copy of our extension code

---

## 4. Build Validation & Fix

First build failed:

```
error: Embedded binary's bundle identifier is not prefixed with the parent app's bundle identifier.
```

**Root cause:** The converter set different bundle identifiers with mismatched case:

| Target | Bundle ID |
|---|---|
| Host app | `com.lzw.TabsKiller` |
| Extension | `com.lzw.tabskiller.Extension` |

Apple requires: extension bundle ID = parent bundle ID + suffix  (e.g. `com.lzw.TabsKiller.Extension`)

**Fix:** Patched `project.pbxproj` to align case:

```
com.lzw.tabskiller.Extension  →  com.lzw.TabsKiller.Extension
```

Second build: **BUILD SUCCEEDED** ✓

---

## 5. Final Project Structure

```
TabsKiller/
├── .gitignore                            # Added (Xcode build artifacts)
├── TabsKiller.xcodeproj/                 # Xcode project
├── TabsKiller/                           # macOS host app (Swift)
│   ├── AppDelegate.swift
│   ├── ViewController.swift
│   ├── Main.storyboard
│   ├── Assets.xcassets/                  # App icons
│   ├── Info.plist
│   └── Resources/                        # App shell resources
└── TabsKiller Extension/                 # The actual extension
    ├── SafariWebExtensionHandler.swift   # Native ↔ JS bridge
    ├── Info.plist                        # Safari extension registration
    └── Resources/                        # Ported extension code
        ├── manifest.json                 # Unchanged (works as-is)
        ├── background.html / background.js
        ├── popup.html / popup.js
        ├── js/                           # tabmanager.js, settings.js (patched)
        ├── css/                          # popup.css
        └── img/                          # icons
```

---

## 6. How Safari Web Extensions Work Here (Architecture)

```
┌──────────────────────────────────────────────────────────┐
│  TabsKiller.app (macOS native app, Cocoa)               │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  TabsKiller Extension.appex (Safari plugin)      │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │  SafariWebExtensionHandler.swift            │  │   │
│  │  │  (NSExtensionRequestHandling)              │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  │                                                   │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │  Resources/ (Web Extension JS code)        │  │   │
│  │  │  - background.html + JS                    │  │   │
│  │  │  - popup.html + JS                          │  │   │
│  │  │  Safari loads these into WebKit context    │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
         │
         ▼
    Safari.app  ──→ Tabs Killer toolbar button
                    ──→ Background page runs continuously
                    ──→ Popup opens on click
```

The native macOS app is a thin wrapper — it just registers the extension with Safari on launch. All the actual tab-killing logic runs in Safari's Web Extension JavaScript context, unchanged from the Chrome version (with the two API fixes applied).
