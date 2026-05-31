---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safari Extension Path and Configuration Issues
translated: false
type: note
---

Found it. Here's the full diagnosis:

========================================================
ROOT CAUSE: Extension loaded from Xcode DerivedData, never installed
========================================================

Your Safari extension is registered at:

  ~/Library/Developer/Xcode/DerivedData/TabsKiller-fxpnluewboejtagbipylkghpxpjx/Build/Products/Debug/TabsKiller.app/Contents/PlugIns/TabsKiller Extension.appex

TabsKiller.app is NOT in /Applications/.

This is why it keeps disappearing. Safari's extension registry points to a path inside DerivedData. Every time ANY of these happens, the path breaks and Safari unloads it:

  1. You do "Clean Build Folder" in Xcode
  2. Xcode auto-purges old DerivedData (it does this periodically)  
  3. You rebuild and Xcode creates a NEW DerivedData folder with a different hash
  4. macOS updates or Safari gets updated
  5. System restart (Safari re-validates extension paths on boot)

The extension was NEVER properly installed — you've been running it from Xcode's debug build, which is temporary by design.

========================================================
SECONDARY ISSUES (also problematic)
========================================================

1. MISSING FILES — The "TabsKiller Extension/" directory (SafariWebExtensionHandler.swift + extension Info.plist) was NEVER committed to git. The Xcode project references them but they don't exist on disk. This means the extension target can't build from a clean clone.

2. BUNDLE ID CASE MISMATCH:
   - project.pbxproj: com.lzw.TabsKiller.Extension
   - ViewController.swift: com.lzw.tabskiller.Extension  (lowercase!)
   Safari extensions are case-sensitive. This can cause "extension not found" errors.

3. MANIFEST V2 on macOS 26 — Your manifest.json uses manifest_version: 2 (browser_action, background.page). Safari on macOS 26 Tahoe may require Manifest V3 (action, service_worker). Safari periodically deprecates MV2 APIs and can disable MV2 extensions.

========================================================
FIX
========================================================

To permanently fix this, you need to:

1. Rebuild the Xcode project (since the Extension target files are missing, create a fresh Safari Web Extension project or regenerate with Xcode's "Safari Web Extension" template)

2. ARCHIVE the app (Product → Archive in Xcode), then:
   - Export as "Developer ID" signed app
   - Copy TabsKiller.app to /Applications/
   - Launch it once from /Applications/ to register the extension

3. OR the quick fix: just build in Xcode, then manually copy the built app:
   cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/
   Then launch it from /Applications/ once.

4. Update manifest.json to Manifest V3 if targeting macOS 26.

The copy-to-Applications step is the key. Once the .appex is in a stable path (/Applications/TabsKiller.app/Contents/PlugIns/), Safari won't lose it.