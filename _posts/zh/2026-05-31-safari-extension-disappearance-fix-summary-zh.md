---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Safari 扩展消失修复摘要
translated: true
type: note
---

========================================================
根本原因分析
========================================================

你的Safari扩展持续消失，原因有4点：

1. **从未安装到 /Applications/**
   扩展仅从Xcode的DerivedData中加载：
   ```
   ~/Library/Developer/Xcode/DerivedData/TabsKiller-xxx/...
   ```
   每次Xcode清理、重建或自动清除旧的DerivedData时，路径被破坏，Safari就会卸载该扩展。

2. **缺少扩展源文件**
   `TabsKiller Extension/` 目录从未提交到git。Xcode项目引用了3个关键文件，但这些文件并不存在：
   - `SafariWebExtensionHandler.swift`（原生消息处理器）
   - `Info.plist`（扩展bundle配置）
   - `Resources/`（popup.html、popup.js、manifest.json、css/、js/、img/）
   
   缺少这些文件，导致从干净的克隆中无法构建扩展目标。

3. **Bundle ID大小写不匹配**
   `project.pbxproj`中：`com.lzw.TabsKiller.Extension`（大写T、K）
   `ViewController.swift`中：`com.lzw.tabskiller.Extension`（全小写）
   Safari扩展是大小写敏感的——这导致了“未找到”错误。

4. **临时代码签名**
   应用没有设置DEVELOPMENT_TEAM，因此Xcode以临时签名方式签署。macOS 26上的Safari需要正确的Apple Development签名才能发现并加载扩展。

========================================================
我做了什么
========================================================

1. 创建了 `TabsKiller Extension/` 目录，包含：
   - `SafariWebExtensionHandler.swift` —— 通过 `NSExtensionRequestHandling + SFExtensionMessageKey` 处理Web扩展与宿主应用之间的原生消息通信。
   - `Info.plist` —— 声明 `NSExtensionPointIdentifier` 为 `com.apple.Safari.web-extension`，并指定主类。
   - `Resources/` —— 复制所有Web扩展文件（popup.html、popup.js、background.js、background.html、manifest.json、css/、js/、img/、app.build.js、README.md）。

2. 修复了 `ViewController.swift` 中的bundle ID：
   `com.lzw.tabskiller.Extension` → `com.lzw.TabsKiller.Extension`

3. 在 `project.pbxproj` 中添加了 `DEVELOPMENT_TEAM = 976YQN9M2D`（4处 —— 2个目标 × 2个构建配置）。

4. 通过 `xcodebuild -scheme TabsKiller -configuration Debug` 构建。

5. 将构建好的应用复制到 `/Applications/`：
   ```bash
   cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/
   ```

6. 从pluginkit中清理了过期的DerivedData注册信息：
   ```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData/TabsKiller-*
   pluginkit -r -i com.lzw.TabsKiller.Extension
   ```

7. 从 `/Applications/` 启动 `TabsKiller.app`，以稳定路径将扩展注册到Safari。

========================================================
保持不变的内容
========================================================

- `manifest.json`：仍为Manifest V2（Safari中MV2仍然可用）
- 扩展权限：`tabs`、`storage`
- 宿主应用：打开Safari扩展偏好设置的NSApplication
- 扩展行为：标签页过多时自动关闭最旧的标签页

========================================================
你需要记住的
========================================================

从Xcode重新构建后，始终执行：

```bash
cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/
```

或者使用单行命令：

```bash
cd ~/projects/tab-killer/safari-tab-killer && \
xcodebuild -scheme TabsKiller -configuration Debug build && \
rm -rf /Applications/TabsKiller.app && \
cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/
```

提交缺少的文件：

```bash
git add safari-tab-killer/TabsKiller\ Extension/
git commit -m "add Safari extension target files + fix bundle ID + signing"
```