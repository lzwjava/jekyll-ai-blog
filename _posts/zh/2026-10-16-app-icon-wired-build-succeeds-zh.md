---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 应用图标连线错误，构建成功
translated: true
type: note
---

完成。构建成功，图标已接入。

**我所做的：**

1. **选择了正确的尺寸：** iOS 的 `AppIcon.appiconset` 使用现代单一尺寸格式，确切要求 **1024×1024** —— 因此 `fun-live-icon-1024.png` 是正确的源文件（已通过 `sips` 验证，确认为 1024×1024）。较小的尺寸（32/48/64/128/160/256/512）用于网页 favicon，iOS 不使用。

2. **将其复制到资源目录中：** `fun-live-icon-1024.png` → `LiveIos/Assets.xcassets/AppIcon.appiconset/AppIcon.png`

3. **更新了 `Contents.json`**，使其在 `ios universal 1024x1024` 槽位中引用 `AppIcon.png`。

4. **已验证：** `ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon` 已指向该资源目录，并且模拟器构建成功。
