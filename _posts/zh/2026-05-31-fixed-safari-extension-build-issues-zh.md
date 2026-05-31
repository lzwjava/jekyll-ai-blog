---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复了Safari扩展构建问题
translated: true
type: note
---

已解决。以下是操作概要：

========================================================
已修复
========================================================

1. 重新创建了缺失的 `TabsKiller Extension/` 目录：
   - SafariWebExtensionHandler.swift
   - Info.plist（扩展包配置）
   - Resources/（所有 web 扩展文件）

2. 修复了 bundle ID 大小写不匹配的问题：
   - 原为：com.lzw.tabskiller.Extension（小写）
   - 现为：com.lzw.TabsKiller.Extension（与 pbxproj 一致）

3. 通过 `xcodebuild` 构建成功

4. 安装至稳定路径：
   /Applications/TabsKiller.app/Contents/PlugIns/TabsKiller Extension.appex

========================================================
下一步操作
========================================================

打开 Safari → 设置（⌘,）→ 扩展标签页 → 启用 "TabsKiller Extension"。

该扩展将**不再消失**，因为 .appex 位于
/Applications/（稳定路径）而非 DerivedData（临时路径）。

========================================================
请记住
========================================================

每次从 Xcode 重新构建后，还需运行：

  cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

或者一步完成 xcodebuild 构建并拷贝：

  cd ~/projects/tab-killer/safari-tab-killer && \
  xcodebuild -scheme TabsKiller -configuration Debug build && \
  rm -rf /Applications/TabsKiller.app && \
  cp -R ~/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app /Applications/

========================================================
提交缺失的文件
========================================================

`TabsKiller Extension/` 目录从未加入 git。你应该提交它：

  git add safari-tab-killer/TabsKiller\ Extension/
  git commit -m "添加缺失的 Safari 扩展目标文件"