---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Safari扩展路径和配置问题
translated: true
type: note
---

找到了。以下是完整的诊断：

========================================================
根本原因：扩展从Xcode DerivedData加载，从未安装
========================================================

你的Safari扩展注册在：

  ~/Library/Developer/Xcode/DerivedData/TabsKiller-fxpnluewboejtagbipylkghpxpjx/Build/Products/Debug/TabsKiller.app/Contents/PlugIns/TabsKiller Extension.appex

TabsKiller.app **不在** /Applications/ 中。

这就是为什么它不断消失。Safari的扩展注册表指向DerivedData内的一个路径。每当发生以下**任何**情况时，该路径就会失效，Safari会卸载它：

  1. 你在Xcode中执行"Clean Build Folder"（清理构建文件夹）
  2. Xcode自动清除旧的DerivedData（它会定期执行此操作）
  3. 你重新构建，Xcode创建一个哈希值不同的新DerivedData文件夹
  4. macOS更新或Safari更新
  5. 系统重启（启动时Safari会重新验证扩展路径）

该扩展从未被**正确安装**——你一直是从Xcode的调试版本中运行它，而调试版本本质上是临时的。

========================================================
次要问题（同样存在问题）
========================================================

1. 缺少文件——"TabsKiller Extension/"目录（SafariWebExtensionHandler.swift + extension的Info.plist）**从未**提交到git。Xcode项目引用了它们，但它们并不存在于磁盘上。这意味着从干净的克隆中无法构建扩展目标。

2. Bundle ID大小写不匹配：
   - project.pbxproj：com.lzw.TabsKiller.Extension
   - ViewController.swift：com.lzw.tabskiller.Extension（小写！）
   Safari扩展是大小写敏感的。这可能导致"extension not found"（扩展未找到）错误。

3. 在macOS 26上使用Manifest V2——你的manifest.json使用了manifest_version: 2（browser_action, background.page）。macOS 26 Tahoe上的Safari可能需要Manifest V3（action, service_worker）。Safari会定期弃用MV2 API，并可能禁用MV2扩展。

========================================================
解决方案
========================================================

要永久修复此问题，你需要：

1. 重建Xcode项目（由于Extension目标文件缺失，创建一个全新的Safari Web Extension项目，或者使用Xcode的"Safari Web Extension"模板重新生成）

2. **归档**该应用（Xcode中 Product → Archive），然后：
   - 导出为"Developer ID"签名的应用
   - 将TabsKiller.app复制到/Applications/
   - 从/Applications/启动一次以注册扩展

3. 或者快速修复：在Xcode中构建，然后手动将构建的应用复制过去：
   ```bash
   cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/
   ```
   然后从/Applications/启动一次。

4. 如果目标系统是macOS 26，将manifest.json更新为Manifest V3。

**复制到Applications**这一步是关键。一旦.appex位于一个稳定的路径（/Applications/TabsKiller.app/Contents/PlugIns/），Safari就不会丢失它。