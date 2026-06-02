---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safari Extension Disappearance Fix Summary
translated: false
type: note
---

Here's the full breakdown:

========================================================
ROOT CAUSE ANALYSIS
========================================================

Your Safari extension kept disappearing for 4 reasons:

1. NEVER INSTALLED TO /Applications/
   The extension was only loaded from Xcode's DerivedData:
     ~/Library/Developer/Xcode/DerivedData/TabsKiller-xxx/...
   Every time Xcode cleaned, rebuilt, or auto-purged old DerivedData,
   the path broke and Safari unloaded the extension.

2. MISSING EXTENSION SOURCE FILES
   The `TabsKiller Extension/` directory was NEVER committed to git.
   The Xcode project referenced 3 critical files that didn't exist:
   - SafariWebExtensionHandler.swift (native message handler)
   - Info.plist (extension bundle config)
   - Resources/ (popup.html, popup.js, manifest.json, css/, js/, img/)

   Without these, the extension target couldn't build from a clean clone.

3. BUNDLE ID CASE MISMATCH
   project.pbxproj:  com.lzw.TabsKiller.Extension  (capital T, K)
   ViewController.swift: com.lzw.tabskiller.Extension  (all lowercase)
   Safari extensions are case-sensitive — this caused "not found" errors.

4. AD-HOC CODE SIGNING
   The app had no DEVELOPMENT_TEAM set, so Xcode signed it ad-hoc.
   Safari on macOS 26 requires proper Apple Development signing
   to discover and load extensions.

========================================================
WHAT I DID
========================================================

1. Created `TabsKiller Extension/` directory with:
   - SafariWebExtensionHandler.swift — handles native messaging
     between the web extension and the host app via
     NSExtensionRequestHandling + SFExtensionMessageKey
   - Info.plist — declares NSExtensionPointIdentifier as
     com.apple.Safari.web-extension and the principal class
   - Resources/ — copied all web extension files (popup.html,
     popup.js, background.js, background.html, manifest.json,
     css/, js/, img/, app.build.js, README.md)

2. Fixed ViewController.swift bundle ID:
   com.lzw.tabskiller.Extension → com.lzw.TabsKiller.Extension

3. Added DEVELOPMENT_TEAM = 976YQN9M2D to project.pbxproj
   (4 places — 2 targets × 2 build configurations)

4. Built via `xcodebuild -scheme TabsKiller -configuration Debug`

5. Copied the built app to /Applications/:
   cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

6. Cleaned stale DerivedData registrations from pluginkit:
   rm -rf ~/Library/Developer/Xcode/DerivedData/TabsKiller-*
   pluginkit -r -i com.lzw.TabsKiller.Extension

7. Launched TabsKiller.app from /Applications/ to register the
   extension with Safari at a stable path

========================================================
WHAT STAYS THE SAME
========================================================

- manifest.json: still Manifest V2 (MV2 still works in Safari)
- Extension permissions: tabs, storage
- Host app: NSApplication that opens Safari extension preferences
- Extension behavior: auto-kill oldest tabs when too many

========================================================
WHAT YOU NEED TO REMEMBER
========================================================

After rebuilding from Xcode, always run:

  cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

Or use the one-liner:

  cd ~/projects/tab-killer/safari-tab-killer && \
  xcodebuild -scheme TabsKiller -configuration Debug build && \
  rm -rf /Applications/TabsKiller.app && \
  cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

Commit the missing files:

  git add safari-tab-killer/TabsKiller\ Extension/
  git commit -m "add Safari extension target files + fix bundle ID + signing"
