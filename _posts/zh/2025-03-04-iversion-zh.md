---
audio: false
generated: true
lang: zh
layout: post
title: 在iOS中使用iVersion
translated: true
type: note
---

要在 iOS 项目中使用 `iVersion` 依赖库，请按以下步骤操作：

1. **在 Xcode 中打开项目**：确保已打开需要添加 `iVersion` 依赖库的 Xcode 项目。

2. **初始化 CocoaPods**：如果尚未在项目中初始化 CocoaPods，请打开终端，进入项目目录并执行：

   ```bash
   pod init
   ```

   这将在项目目录中创建 `Podfile` 文件。

3. **编辑 Podfile**：在文本编辑器或 Xcode 中打开 `Podfile`。在 target 部分添加以下行来引入 `iVersion` 依赖库：

   ```ruby
   pod 'iVersion', '1.11.4'
   ```

4. **安装依赖库**：保存 `Podfile` 后返回终端。运行以下命令安装 `iVersion` 依赖库：

   ```bash
   pod install
   ```

5. **打开 `.xcworkspace` 文件**：安装完成后，如果原 Xcode 项目处于打开状态请先关闭，然后打开新生成的 `.xcworkspace` 文件。该文件通常位于原 `.xcodeproj` 文件同目录下。

6. **导入 iVersion**：在 Swift 或 Objective-C 文件中导入 `iVersion` 模块即可开始使用：

   ```swift
   import iVersion
   ```

7. **在代码中使用 iVersion**：现在可以在项目中调用 `iVersion` 库的功能。例如，您可以使用 `iVersion` 提供的方法来检查应用版本或构建版本号。

遵循以上步骤，即可在 iOS 项目中成功集成并使用 `iVersion` 依赖库。
