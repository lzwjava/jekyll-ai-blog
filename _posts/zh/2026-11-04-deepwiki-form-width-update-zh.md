---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepWiki 表单宽度更新
translated: true
type: note
---

完成。DeepWiki 表单现在正好是 **26rem** 宽（并且限制在 `100%`，因此永远不会在小屏幕上溢出）。

编译后的 CSS 确认：
```css
.sort-container .deepwiki-link .deepwiki-form {
  width: 26rem;
  max-width: 100%;
  ...
}
```

构建通过。注意之前的 `.dark-mode` 覆盖未被触及，因此表单保留了其 dark-mode 样式。这些更改（以及之前的 badge 移除 + dark-mode 修复）仍然 **未提交** — 要我提交它们吗？