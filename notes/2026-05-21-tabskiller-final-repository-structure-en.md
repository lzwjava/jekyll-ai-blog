---
audio: false
generated: true
image: false
lang: en
layout: post
title: "TabsKiller: Final Repository Structure"
translated: false
type: note
---

Done. Pushed `3d8090e` → `master`.

Final repo structure at https://github.com/lzwjava/TabsKiller:

```
README.md           ← English, dual Chrome + Safari
README-CN.md        ← Chinese
safari-tab-killer.png   ← Safari screenshot (664 KB)
safari-tab-killer.mp4   ← Safari demo video (664 KB)
chrome-tab-killer/      ← Chrome extension (load unpacked)
├── manifest.json
├── popup.html / popup.js / background.js
├── css/ img/ js/
└── ...
safari-tab-killer/      ← Safari Web Extension + Xcode project
├── manifest.json
├── TabsKiller.xcodeproj/
├── TabsKiller/ (Swift app)
└── ...
```

Both READMEs cover features, install for each browser, and the story. The Safari section has the screenshot inline and the mp4 demo. Chrome links to the Web Store with the version badge.
