---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Chrome扩展转换为Safari
translated: true
type: note
---

以下是完成的所有工作的摘要：

---

## 已将 TabsKiller 从 Chrome 扩展程序转换为 Safari 扩展程序

### 项目结构

```
safari-tabs-killer/         ← 原始源代码，现已兼容 Safari
TabsKiller/                 ← 生成的 Xcode 项目（构建成功）
├── TabsKiller.xcodeproj
├── TabsKiller/
│   ├── AppDelegate.swift
│   ├── ViewController.swift
│   ├── Main.storyboard
│   └── Resources/            ← 空的应用外壳资源
└── TabsKiller Extension/
    ├── SafariWebExtensionHandler.swift   ← 原生消息桥接
    ├── Info.plist                        ← 标识为 Safari Web 扩展
    └── Resources/
        ├── manifest.json                 ← 相同的 manifest，可在 Safari 中运行
        ├── background.html / background.js
        ├── popup.html / popup.js
        └── js/                           ← tabmanager.js, settings.js, libs
```

### 源代码中的更改

| 文件 | 更改内容 |
| --- | --- |
| `js/settings.js` | `chrome.storage.sync` → `chrome.storage.local`（Safari 不支持同步存储） |
| `js/settings.js` | 默认白名单：`['chrome://*']` → `[]`（仅 Chrome 使用的协议） |
| `README.md` | 更新文档，改为 Safari 安装说明，而非 Chrome Web Store |

### 如何构建与运行

```bash
# 打开 Xcode（或使用命令行）
open /Users/lzwjava/projects/projects/TabsKiller/TabsKiller.xcodeproj

# 在 Xcode 中：
# 1. 在 Signing & Capabilities 中选择你的开发者团队
# 2. Product → Run（或 Cmd+R）

# 或通过命令行：
cd /Users/lzwjava/projects/projects/TabsKiller
xcodebuild -project TabsKiller.xcodeproj -scheme TabsKiller build

# 然后找到应用并运行（或从 Xcode 运行）
```

启动后，应用会在 Safari 中注册该扩展。前往 **Safari → 设置 → 扩展** 并启用 "Tabs Killer"。

### 如需重新转换（从零开始）

```bash
xcrun safari-web-extension-converter safari-tabs-killer \
  --app-name "TabsKiller" \
  --bundle-identifier "com.lzw.TabsKiller" \
  --macos-only --force --no-prompt --copy-resources
```

原始仅 Chrome 版本的备份位于 `safari-tabs-killer-backup/`。
