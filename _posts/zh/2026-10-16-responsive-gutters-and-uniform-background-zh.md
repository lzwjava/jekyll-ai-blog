---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 响应式间距与统一背景
translated: true
type: note
---

完成。先回答你的设计问题：**在主容器上使用 `max-width`，而不是固定的 `margin-left/right: 300px`**。固定边距在较小的窗口下会出问题（它们可能超出视口导致横向滚动），而 `max-width` + `margin: 0 auto` 是流式的，能自动调整。应用已经将 `#wrapper` 限制在 480px——实际上“不行”的是卡片/图片在列内会 edge-to-edge（没有 gutter），并且桌面端列周围显示了两种不同的灰色。

**更改：**

`src/App.vue`
- `.view`（每个路由视图的根元素）现在会获得响应式侧边 gutter：手机上是 `padding 0 12px`，481px 以上是 `0 28px`。这会在一个地方应用到整个应用——介绍页、列表、个人资料、表单——因此没有任何内容会碰到屏幕边缘，你也不需要为每个视图单独设置 margin。
- `.live-view` 选择退出（`padding 0`），因为直播间是全屏视频+聊天的布局。
- 移除了沉重的桌面端 box-shadow，因为现在背景是统一的。

`src/stylus/base.styl`
- `body` 背景从 `#D2D2D2` 改为 `#e7e7e7`（与 `#wrapper` 相同），这样在桌面端，居中的列会与页面融合，而不是显示双色调的灰色边框。

CSS 盒模型的一个很好的副作用：绝对定位的 full-bleed 元素（直播视频播放器、个人资料头部条、固定底栏）会相对于 padding box 解析，因此它们仍然会自动横跨整个列——不需要额外代码。

已通过 headless Chromium 在 390px、768px 和 1280px 宽度下截图验证：介绍页卡片带有干净的 gutter 内缩，桌面端列保持居中且最大 480px，直播播放器仍然 edge-to-edge。生产构建通过。