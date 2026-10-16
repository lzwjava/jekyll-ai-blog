---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更高的页眉且链接不换行
translated: true
type: note
---

改动已生效。以下是我在 `style.css` 中调整的内容：

1. **顶部导航栏加高** — `.nav__inner` 高度从 `64px` 增加至 `80px`，并在品牌名称与链接组之间添加了 `gap: 16px` 间距，使品牌在左侧有呼吸空间，语言切换按钮在右侧也不再拥挤。

2. **英文不再自动换行** — `.nav__links` 现在启用了 `white-space: nowrap`，并将间距从 `22px` 缩小至 `18px`，确保所有英文项目（如“Services · AI Services · AI Team · Tech Stack · Portfolio · Finance · Clients · Team · Contact”）保持在同一行，不会换行。

由于链接不再换行，加高的导航栏提供了更宽敞的头部空间，让 logo/品牌名称远离左边缘，中/EN 切换按钮也远离右边缘。移动端的响应式隐藏功能依然正常工作。
