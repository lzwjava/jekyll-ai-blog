---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable Safari Extension in Xcode
translated: false
type: note
---

When you run the app from Xcode, it registers the extension with Safari. Here's what to do:

## Enable in Safari

**Safari → Settings (Cmd+,) → Extensions tab**

You'll see "TabsKiller" in the list. Check the box to enable it.

![Safari Extensions settings showing TabsKiller checkbox]

After enabling, you'll see the TabsKiller icon appear in the Safari toolbar — click it to open the popup and configure max tabs / whitelist.

## If it doesn't show up

**First time:** Xcode runs the app once, which registers the extension. You might need to quit and reopen Safari for it to appear in the list.

**Developer mode:** Safari → Settings → Advanced → check "Show Develop menu in menu bar". Then Develop → Web Extensions — you can see and reload the extension there.

**App already built:** The app lives in Xcode's DerivedData. You can also copy it:
```bash
open /Users/lzwjava/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app
```
Run it from there, then enable in Safari settings.

---

Alternatively, if you want to see it working right now without Xcode re-launching it every time:

```bash
# Build once
cd /Users/lzwjava/projects/projects/TabsKiller
xcodebuild -project TabsKiller.xcodeproj -scheme TabsKiller -destination 'platform=macOS' build

# Find and open the built app
open "$(xcodebuild -project TabsKiller.xcodeproj -scheme TabsKiller -showBuildSettings 2>/dev/null | grep BUILT_PRODUCTS_DIR | awk '{print $NF}')/TabsKiller.app"
```

That will launch the app, it runs in the menu bar briefly, registers the extension, then Safari picks it up.