---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chevron修复与iOS滚动指示器
translated: true
type: note
---

新构建已安装并在 **lzwjava13** 上重新启动。目前情况如下：

## 我为首页修复的内容

行之前使用了激进的通栏布局（`leading: 0` 内边距 + 全宽白色卡片），没有为 `NavigationLink` 的 chevron 留下干净的空间。在你设备的屏幕宽度下，这导致 ">" 渲染为**被压扁的灰色碎片**（"不完整"），并留下看起来破碎的边缘。

新布局（已部署）：

```swift
.listRowInsets(EdgeInsets(top: 6, leading: 12, bottom: 6, trailing: 20))
.listRowBackground(Color.clear)
```

此外，每一行现在是干净的**圆角白色卡片**（`clipShape(RoundedRectangle(cornerRadius: 10))`），像一个正常的矩形，chevron 干净地放在自己的空间里。

我在模拟器上验证过：行现在是紧凑的白色圆角卡片，带有小巧完整的 ">" chevron，没有裁剪伪影。

## 关于右侧边缘的灰色条

那条细灰色垂直条（在你的两张截图中都能看到，分别在 **My** 页面和 **Live** 页面——后者是 `ScrollView`，不是 `List`——而且旧版本中也有）**不是行/chevron 问题**。这是 iOS 26 设备级别的渲染伪影——很可能是滚动指示器在滚动中途被捕获（iOS 26 会在开始/结束滚动时将其渲染为右侧边缘的长圆角条）。它会出现在所有可滚动屏幕上，但不会出现在模拟器中。前端没有设置可以控制它而不损害滚动提示。

## 请重新检查

在手机上打开应用 → **直播** 标签页，下拉刷新：

- 行现在应该是干净的圆角白色卡片，右侧有正常的灰色 ">" chevron。
- 破碎/不完整的 chevron 碎片应该消失了。

如果右侧边缘的灰色条在*不*滚动时仍然困扰你，请再发一张截图——但如果它只在滚动期间/刚滚动后出现，那就是正常的 iOS 滚动条。
