---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Xcode中启用Safari扩展
translated: true
type: note
---

当您从 Xcode 运行该应用时，它会向 Safari 注册扩展。接下来需要执行以下操作：

## 在 Safari 中启用

**Safari → 设置 (Cmd+,) → 扩展标签页**

您将在列表中看到“TabsKiller”。勾选复选框以启用它。

![Safari 扩展设置中显示 TabsKiller 复选框]

启用后，您会在 Safari 工具栏中看到 TabsKiller 图标——点击它即可打开弹出窗口，并配置最大标签页数/白名单。

## 如果没有显示

**首次使用时：** Xcode 会运行一次应用以注册扩展。您可能需要退出并重新打开 Safari，它才会出现在列表中。

**开发者模式：** Safari → 设置 → 高级 → 勾选“在菜单栏中显示‘开发’菜单”。然后选择 开发 → Web 扩展——您可以在那里查看并重新加载扩展。

**已构建的应用：** 应用位于 Xcode 的 DerivedData 中。您也可以直接拷贝它：

```bash
open /Users/lzwjava/Library/Developer/Xcode/DerivedData/TabsKiller-*/Build/Products/Debug/TabsKiller.app
```

从那里运行它，然后在 Safari 设置中启用。

---

或者，如果您希望立即看到效果，而不必每次都通过 Xcode 重新启动：

```bash
# 构建一次
cd /Users/lzwjava/projects/projects/TabsKiller
xcodebuild -project TabsKiller.xcodeproj -scheme TabsKiller -destination 'platform=macOS' build

# 找到并打开构建好的应用
open "$(xcodebuild -project TabsKiller.xcodeproj -scheme TabsKiller -showBuildSettings 2>/dev/null | grep BUILT_PRODUCTS_DIR | awk '{print $NF}')/TabsKiller.app"
```

这将启动应用，它会在菜单栏中短暂运行，注册扩展，然后 Safari 就会识别到它。
