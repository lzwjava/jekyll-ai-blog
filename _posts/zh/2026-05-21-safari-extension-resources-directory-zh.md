---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Safari扩展资源目录
translated: true
type: note
---

选择这个目录：

```
/Users/lzwjava/projects/projects/TabsKiller/TabsKiller Extension/Resources/
```

`manifest.json` 就在这里：

```
TabsKiller/
├── TabsKiller/                    ← macOS 应用外壳
├── TabsKiller.xcodeproj/          ← Xcode 项目
└── TabsKiller Extension/
    └── Resources/                 ←  ← 就是这个文件夹——选中它
        ├── manifest.json
        ├── background.html
        ├── popup.html
        └── js/...
```

Safari 的 "Add Temporary Extension" 相当于 Chrome 的 "Load unpacked extension"——它只需要包含 `manifest.json` 的文件夹即可。快速测试时无需进行 Xcode 构建。
