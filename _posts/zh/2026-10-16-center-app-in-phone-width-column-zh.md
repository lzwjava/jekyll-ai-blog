---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在手机宽度列中居中应用
translated: true
type: note
---

是的——我将整个应用在桌面端限制为一个居中的、手机宽度的列。用 `npm run build` 编译一切顺利。

## 问题出在哪里

页面以 `width: 100%` 拉伸到整个显示器。另外，有两个栏使用了 `position: fixed`（`.tab-bar`、`.attend-section`），它们的 `100%` 是相对于 **viewport** 解析的，因此即使外层容器设置了 max-width 也无法包含它们。

## 更改

**`src/stylus/variables.styl`** —— 列宽的唯一来源：
```stylus
$app-max-width = 480px
```

**`src/App.vue`** —— 约束并居中 `#wrapper` 列：
```stylus
#wrapper
  position relative
  width 100%
  max-width $app-max-width
  margin 0 auto
  min-height 100%
  background-color #e7e7e7

// Desktop: make the centered column read like a phone screen.
@media screen and (min-width: 481px)
  #wrapper
    box-shadow 0 0 24px rgba(0, 0, 0, .35)
    min-height 100vh
```
由于 `.view` 在 `#wrapper` 内部是 `position: absolute; width: 100%`，所有路由（`/lives`、个人资料、房间…）也会自动被限制。

**`src/components/Tabbar.vue`** —— 固定的底部标签栏（之前是 `max-width: 700px` 但相对于 viewport 左对齐）现在居中于该列：
```stylus
.tab-bar
  position fixed
  left 50%
  transform translateX(-50%)
  width 100%
  ...
  max-width $app-max-width
```

**`src/views/IntroView.vue`** —— `.attend-section` 原本有一个无效的 media query（`margin: 0 auto` 无法居中 fixed 元素）；已替换为同样的 `left: 50%` + `translateX(-50%)` + `max-width $app-max-width` 模式。

## 结果

- 移动端（≤480px viewport）：不变，全宽。
- 桌面端：一个 480px 宽的居中列，带有细微阴影，tab bar 和 attend 栏与其精确对齐——在灰色背景上看起来像手机屏幕。
- Overlay/toast 保持 viewport 居中（modal 遮罩覆盖整个屏幕），这是常见的桌面端行为。

注意：`$app-max-width` 定义在 `variables.styl` 中，因此如果你想要不同的尺寸（例如 `414px` 类似 iPhone，或 `600px` 更宽敞），更改那一行并重新构建即可。