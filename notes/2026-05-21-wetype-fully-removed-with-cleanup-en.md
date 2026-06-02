---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeType Fully Removed with Cleanup
translated: false
type: note
---

WeType is completely gone:

| Location | Status |
|---|---|
| `/Library/Input Methods/WeType.app` | Removed |
| Launch agent (running process) | Killed + deregistered |
| `~/Library/Preferences/` | Cleaned |
| `~/Library/Caches/` | Cleaned |
| `~/Library/Application Support/` | Cleaned |
| `~/Library/HTTPStorages/` | Cleaned |
| `~/Library/WebKit/` | Cleaned |
| Diagnostic logs | Cleaned |

**~1.6 GB saved.** You'll need to add Apple Pinyin manually:

```
System Settings > Keyboard > Input Sources > Add > Chinese > Pinyin - Simplified
```
