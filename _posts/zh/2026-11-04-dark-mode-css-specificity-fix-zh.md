---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 暗色模式CSS特异性修复
translated: true
type: note
---

已修复并验证。以下是情况说明：

**根因 —— CSS 特异性 (specificity)，而非输入本身（你对包装器（wrapper）的直觉是对的）：**

- 浅色主题：`.sort-container .deepwiki-link .deepwiki-form` → **3 个类** → `background: #fff`
- 深色主题：`.dark-mode .deepwiki-link` → 只有 **2 个类** → `background: #2a2a2a`

拥有 3 个类的浅色规则覆盖了只有 2 个类的深色规则，因此在暗模式下，白色的药片背景（以及蓝色边框、阴影，甚至输入文本上的 `color: #333`）总是胜出。

**修复** 位于 `_sass/dark-mode.scss` 中：匹配完整的链加上 `.dark-mode` 祖先：

```scss
.sort-container .deepwiki-link .deepwiki-form {   // 在 .dark-mode 下 →
    background: #2a2a2a;                          // .dark-mode .sort-container .deepwiki-link .deepwiki-form
    border-color: #4f82e6;                        // 4 个类 > 3 个类 → 暗模式现在胜出
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    .deepwiki-input { color: #f0f0f0; ... }
}
```

**验证** 通过 `bundle exec jekyll build` (exit 0) — 编译后的 CSS 现在包含：

```css
.dark-mode .sort-container .deepwiki-link .deepwiki-form { background: #2a2a2a; ... }
.dark-mode .sort-container .deepwiki-link .deepwiki-form .deepwiki-input { color: #f0f0f0; ... }
```

重新加载开启了切换的页面，DeepWiki 药片应该会显示为深灰色 `#2a2a2a`，并带有浅色文本，而非白色。

注意：`_sass/dark-mode.scss` 现在也已修改，连同之前就未提交的 `_includes/sort.html` 和 `_sass/layout.scss`。要我提交这些文件（并推送，使用 HTTP/1.1 HTTPS 变通方法，因为通过代理的 SSH 不稳定）吗？
