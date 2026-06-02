---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safari Extension Resources Directory
translated: false
type: note
---

Choose this directory:

```
/Users/lzwjava/projects/projects/TabsKiller/TabsKiller Extension/Resources/
```

That's where `manifest.json` lives:

```
TabsKiller/
├── TabsKiller/                    ← macOS app shell
├── TabsKiller.xcodeproj/          ← Xcode project
└── TabsKiller Extension/
    └── Resources/                 ←  ← THIS ONE — pick this folder
        ├── manifest.json
        ├── background.html
        ├── popup.html
        └── js/...
```

Safari's "Add Temporary Extension" is the equivalent of Chrome's "Load unpacked extension" — it just needs the folder containing `manifest.json`. No Xcode build needed for quick testing.
