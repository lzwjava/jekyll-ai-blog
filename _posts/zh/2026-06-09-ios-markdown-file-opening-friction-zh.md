---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iOS Markdown文件打开摩擦
translated: true
type: note
---

**问题：** 为什么在 iOS 上即便安装了数百款应用，打开 markdown 文件依然如此困难？而声明 .md 文件类型支持为何如此重要？

**回答：**

这是"沙盒机制 + 文件类型声明"共同导致的问题，揭示了 iOS 对"通用"文件打开方式有意设置的摩擦机制。以下是背后的运作原理。

## iOS 文件类型架构

iOS 没有像 Windows/macOS 那样的全局文件扩展名→应用映射机制。相反，应用必须在 `Info.plist` 中*明确声明*支持的文件类型。当你在微信中点击 `.md` 文件时，iOS 会询问所有已安装应用："谁声称能处理 `public.plain-text` 或 `com.markdown`？"只有注册了这些类型的应用才会出现在共享菜单中。

你安装的 200-300 个应用中，绝大多数从未注册 markdown 支持——即便它们*能够*读取 markdown。

**示例：Notion 的 Info.plist 中未包含的内容：**

```xml
<!-- Notion 实际的 Info.plist（简化版） -->
<key>CFBundleDocumentTypes</key>
<array>
  <!-- Notion 声明支持网页剪辑、图片等 -->
  <!-- 但并未明确声明支持 .md 文件 -->
</array>
```

Notion 在*内部*解析 markdown 用于显示，但并未声明 `public.plain-text` 或 markdown UTTypes 作为其可处理的文件类型。该应用能够渲染 markdown，但 iOS 的沙盒机制规定："未经明确声明，无法从沙盒外部接收 .md 文件。"

**read.md 为何能正常运作：**

```xml
<!-- read.md 的 Info.plist -->
<key>CFBundleDocumentTypes</key>
<array>
  <dict>
    <key>CFBundleTypeRole</key>
    <string>Editor</string>
    <key>LSItemContentTypes</key>
    <array>
      <string>public.plain-text</string>
      <string>com.markdown</string>  <!-- 明确声明支持 markdown -->
      <string>public.text</string>
    </array>
  </dict>
</array>
```

它声明自己是文件处理者。iOS 现在知道："用户点击了 .md → 询问 read.md。"

## DuckDuckGo 浏览器为何不出现

浏览器属于特殊情况。它们处理的是 `http://` 和 `https://` 方案，而非文件类型。`.md` 文件不是 URL——它是沙盒中的文档。共享菜单中永远不会包含处理本地文件的浏览器。（这是有意为之：苹果希望防止应用拦截文档。）

## 这种设计存在的真正原因

这并非漏洞——而是刻意制造的摩擦：

1. **安全性**：未经明确声明，恶意应用无法静默拦截文件。一个暗中处理 .md 文件并试图窃取笔记的应用无法得逞——它必须先声明意图。

2. **沙盒模型**：iOS 强制执行单向通信。应用无法访问微信的沙盒并读取文件，除非微信明确将其传递出去（通过共享菜单）。接收应用必须声明"我接受这种类型"。

3. **应用发现激励机制**：苹果希望用户下载*专用*应用，而非依赖通用文件处理程序。read.md 之所以存在，是因为有人看到了需求。Notion 无需声明 markdown 支持，因为用户在 Notion*内部*打开笔记，而非外部。

## 在 iOS 上你实际需要的

对于 markdown 文件，你的选择包括：

- **专用 markdown 阅读器**：read.md、iA Writer、Ulysses、Markdown Editor（已声明 .md 支持）
- **代码编辑器**：Working Copy (Git)、Xcode Playgrounds、Runestone（均已声明文本/markdown 支持）
- **已声明支持的文本编辑器**：部分应用支持（请查看其 App Store 描述）
- **变通方案**：通过 CloudKit 同步到备忘录应用或 iCloud Drive，然后从那里打开（绕过共享菜单摩擦）

## 更深层的模式

这就是 iOS 相比 macOS 感觉更"固执己见"的原因。在 macOS 上，双击 `file.md`，系统会检查文件关联。在 iOS 上，你会遇到摩擦，被引导使用专用、精选的应用。这是设计使然——不是限制，而是一种理念。

如果你正在开发 iOS 应用并希望处理 markdown 文件，请在 `Info.plist` 中添加：

```xml
<key>UTImportedTypeDeclarations</key>
<array>
  <dict>
    <key>UTTypeIdentifier</key>
    <string>com.markdown</string>
    <key>UTTypeConformsTo</key>
    <array><string>public.plain-text</string></array>
    <key>UTTypeTagSpecification</key>
    <dict>
      <key>public.filename-extension</key>
      <array><string>md</string><string>markdown</string></array>
    </dict>
  </dict>
</array>
```

然后声明你的应用处理该类型。现在用户将在共享菜单中看到你的应用。