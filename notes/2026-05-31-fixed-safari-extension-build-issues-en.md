---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed Safari Extension Build Issues
translated: false
type: note
---

Done. Here's what happened:

========================================================
FIXED
========================================================

1. Recreated missing `TabsKiller Extension/` directory:
   - SafariWebExtensionHandler.swift
   - Info.plist (extension bundle config)
   - Resources/ (all web extension files)

2. Fixed bundle ID case mismatch:
   - Was: com.lzw.tabskiller.Extension (lowercase)
   - Now: com.lzw.TabsKiller.Extension (matches pbxproj)

3. Built successfully via `xcodebuild`

4. Installed to stable path:
   /Applications/TabsKiller.app/Contents/PlugIns/TabsKiller Extension.appex

========================================================
WHAT TO DO NOW
========================================================

Open Safari → Settings (⌘,) → Extensions tab → enable "TabsKiller Extension".

The extension will NOT disappear anymore because the .appex is at
/Applications/ (stable) instead of DerivedData (ephemeral).

========================================================
REMEMBER
========================================================

Every time you rebuild from Xcode, also run:

  cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

Or just build with xcodebuild + copy in one shot:

  cd ~/projects/tab-killer/safari-tab-killer && \
  xcodebuild -scheme TabsKiller -configuration Debug build && \
  rm -rf /Applications/TabsKiller.app && \
  cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

========================================================
COMMIT THE MISSING FILES
========================================================

The `TabsKiller Extension/` directory was never in git. You should commit it:

  git add safari-tab-killer/TabsKiller\ Extension/
  git commit -m "add missing Safari extension target files"
