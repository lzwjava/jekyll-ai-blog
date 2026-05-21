---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Safari网络扩展转换步骤
translated: true
type: note
---

以下是完整的逐步转换过程：

---

## 1. 项目侦察

首先，我检查了整个代码库以了解该扩展：

**清点的文件（共27个）：**
- `manifest.json` — Chrome 扩展清单（v2）
- `background.html` / `background.js` — 使用 RequireJS 模块加载器的入口
- `popup.html` / `popup.js` — 设置界面（最大标签页数、白名单）
- `js/tabmanager.js` — 标签页事件监听器 + 关闭最旧标签页逻辑（核心）
- `js/settings.js` — 使用 `chrome.storage.sync` 的持久化层
- `css/popup.css`、`README.md`、`app.build.js` 以及第三方库（jQuery、Bootstrap、Underscore、RequireJS）

**识别出的仅限 Chrome 的 API：**
| API | 所在位置 | 问题 |
|---|---|---|
| `chrome.storage.sync` | `settings.js`（第 19、67 行） | Safari 不支持 — 必须改用 `chrome.storage.local` |
| `chrome.extension.getBackgroundPage()` | `popup.js`（第 2 行） | Safari 中可用 ✓ |
| `chrome.tabs.*`、`chrome.windows.*` | `tabmanager.js` | Safari Web Extensions 完全支持 ✓ |
| 清单中的 `browser_action` | `manifest.json` | Safari 支持 ✓ |
| 默认白名单 `chrome://*` | `settings.js` | 仅限 Chrome 的协议，在 Safari 中无效 |

---

## 2. 源代码修复

在运行转换器之前，进行三项针对性编辑：

### 修复 1：`chrome.storage.sync` → `chrome.storage.local`

Safari Web Extensions 仅支持 `chrome.storage.local`。它们无法访问 Chrome 的云同步基础设施。

**`js/settings.js` 第 19 行：**
```diff
- chrome.storage.sync.get(keys, function (items) {
+ chrome.storage.local.get(keys, function (items) {
```

**`js/settings.js` 第 67 行：**
```diff
- chrome.storage.sync.set(items, fx);
+ chrome.storage.local.set(items, fx);
```

**为何重要：** 如果保留 `sync`，Safari 会在 `init()` 时抛出运行时错误，扩展静默失败，设置无法加载或保存。

### 修复 2：默认白名单

```diff
- whiteList: ['chrome://*']
+ whiteList: []
```

**原因：** `chrome://*` 是 Chrome 特有的 URL 协议。Safari 使用 `safari-extension://` 等其他协议。使用不匹配的默认模式会造成混淆且毫无意义。

### 修复 3：README

重写了“安装”部分，改为展示 Safari 构建流程，而非 Chrome Web Store 说明。

---

## 3. 运行 Safari Web Extension 转换器

工具 `safari-web-extension-converter` 随 Xcode 提供，路径为：
```
/Applications/Xcode.app/Contents/Developer/usr/bin/safari-web-extension-converter
```

**命令：**
```bash
xcrun safari-web-extension-converter safari-tabs-killer \
  --app-name "TabsKiller" \
  --bundle-identifier "com.lzw.tabskiller" \
  --macos-only \
  --force \
  --no-open \
  --copy-resources \
  --no-prompt
```

**参数说明：**

| 参数 | 原因 |
|---|---|
| `--app-name "TabsKiller"` | 命名 macOS 应用程序包装器 |
| `--bundle-identifier "com.lzw.tabskiller"` | 用于代码签名的反向域名 ID |
| `--macos-only` | 仅生成 macOS 目标（不包括 iOS/iPadOS） |
| `--copy-resources` | 将扩展文件复制到项目中（而非符号链接） |
| `--force` | 如果输出目录已存在则覆盖 |
| `--no-open` | 不自动启动 Xcode |
| `--no-prompt` | 非交互模式 |

**转换器生成的内容：**
- `TabsKiller/TabsKiller.xcodeproj` — Xcode 项目文件
- `TabsKiller/TabsKiller/` — macOS 主机应用（AppDelegate.swift、ViewController.swift、故事板、资源）
- `TabsKiller/TabsKiller Extension/` — Safari 扩展目标
  - `SafariWebExtensionHandler.swift` — 原生消息桥（处理 `browser.runtime.sendNativeMessage`）
  - `Info.plist` — 将 `NSExtensionPointIdentifier` 指向 `com.apple.Safari.web-extension`
  - `Resources/` — 包含扩展代码的完整副本

---

## 4. 构建验证与修复

第一次构建失败：

```
error: Embedded binary's bundle identifier is not prefixed with the parent app's bundle identifier.
```

**根本原因：** 转换器设置了不同的包标识符，且大小写不匹配：

| 目标 | Bundle ID |
|---|---|
| 主机应用 | `com.lzw.TabsKiller` |
| 扩展 | `com.lzw.tabskiller.Extension` |

Apple 要求：扩展的 Bundle ID = 父应用的 Bundle ID + 后缀（例如 `com.lzw.TabsKiller.Extension`）

**修复：** 修改 `project.pbxproj` 以使大小写一致：
```
com.lzw.tabskiller.Extension  →  com.lzw.TabsKiller.Extension
```

第二次构建：**构建成功** ✓

---

## 5. 最终项目结构

```
TabsKiller/
├── .gitignore                            # 已添加（Xcode 构建产物）
├── TabsKiller.xcodeproj/                 # Xcode 项目
├── TabsKiller/                           # macOS 主机应用（Swift）
│   ├── AppDelegate.swift
│   ├── ViewController.swift
│   ├── Main.storyboard
│   ├── Assets.xcassets/                  # 应用图标
│   ├── Info.plist
│   └── Resources/                        # 应用外壳资源
└── TabsKiller Extension/                 # 实际扩展
    ├── SafariWebExtensionHandler.swift   # 原生 ↔ JS 桥接
    ├── Info.plist                        # Safari 扩展注册
    └── Resources/                        # 移植后的扩展代码
        ├── manifest.json                 # 未修改（直接可用）
        ├── background.html / background.js
        ├── popup.html / popup.js
        ├── js/                           # tabmanager.js、settings.js（已修复）
        ├── css/                          # popup.css
        └── img/                          # 图标
```

---

## 6. Safari Web Extensions 在此处的架构原理

```
┌──────────────────────────────────────────────────────────┐
│  TabsKiller.app（macOS 原生应用，Cocoa）                  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  TabsKiller Extension.appex（Safari 插件）        │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │  SafariWebExtensionHandler.swift            │  │   │
│  │  │  （NSExtensionRequestHandling）             │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  │                                                   │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │  Resources/（Web 扩展 JS 代码）             │  │   │
│  │  │  - background.html + JS                    │  │   │
│  │  │  - popup.html + JS                          │  │   │
│  │  │  Safari 将这些加载到 WebKit 上下文中        │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
         │
         ▼
    Safari.app  ──→ Tabs Killer 工具栏按钮
                    ──→ 后台页面持续运行
                    ──→ 点击时弹出窗口
```

macOS 原生应用是一个薄包装器——它仅在启动时向 Safari 注册该扩展。所有实际的标签页关闭逻辑都在 Safari 的 Web Extension JavaScript 上下文中运行，与 Chrome 版本相同（已应用两个 API 修复）。