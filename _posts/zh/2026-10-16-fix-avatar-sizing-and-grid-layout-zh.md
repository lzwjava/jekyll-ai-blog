---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复头像尺寸与网格布局
translated: true
type: note
---

## 构建通过。以下是问题原因和我所做的修改

## 根本原因

**`src/components/user-avatar.vue`** — `.avatar` 没有设置 **宽/高**，而它的子元素 `img` 是 `width: 100%; height: 100%`。这些百分比会相对于自动尺寸的父元素解析，因此会回退到图片的 **固有尺寸**——这就是那个占满整个页面的巨大圆形。

**`src/views/UsersView.vue`** — 样式块仍然针对 *旧* 标记（`li .avatar`），而 `.users-content`、`.user-list`、`.user-item`、`.username` 完全没有 **CSS**。其他每个页面（Invite、Intro、LiveItem、Profile……）都通过嵌套选择器显式设置了 `.avatar` 的尺寸，所以只有 `/live/:id/users` 出问题。

## 修复

**`src/components/user-avatar.vue`** — 添加安全默认值，避免此类问题再次发生：

- `.avatar` 增加 `width: 50px; height: 50px; overflow: hidden; flex-shrink: 0`（可被任何更具体的选择器覆盖，因此不影响现有页面）
- `img` → `display: block` + `object-fit: cover`（不变形，填满圆形）
- 字母回退 `span` → flex 居中（在任何头像尺寸下都能正常工作，不像固定 `line-height` 那样受限）

**`src/views/UsersView.vue`** — 用真正的布局替换过时的 `li` 规则：

- `.user-list`：CSS grid `repeat(auto-fill, minmax(64px, 1fr))` 并带间距 → 响应式头像网格
- `.user-item`：flex 列布局，头像居中显示在名字上方
- `.username`：12px，居中，单行省略号，使 `伯阳阳阳阳阳阳阳阳阳阳` 这样的长名字截断而不是溢出
- `.users-content`：网格周围加少量内边距

结果：每个用户显示为 50px 圆形头像，名字整齐地显示在下方，“点击加载更多”栏位于底部。
