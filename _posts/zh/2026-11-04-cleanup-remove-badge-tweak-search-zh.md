---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理：移除徽章，调整搜索
translated: true
type: note
---

全部完成并已验证。以下是更改内容：

## 所做的更改

**1. `_includes/sort.html`** — 移除了 `Ask DeepWiki` 徽章链接（`<a class="deepwiki-badge">`）。搜索表单被**保留**，因此 `?q=如何学英语` 查询流程仍然保持不变。

**2. `_sass/layout.scss`** — 删除了现在未使用的 `.deepwiki-badge` / `:hover` 样式。

**3. `_sass/dark-mode.scss`** — 为搜索表单添加了 dark-mode 样式，使其在暗色模式下不再显得像刺眼的白框：

- form background → `#2a2a2a` (dark)
- input text → `#f0f0f0`, placeholder → `#9a9a9a`
- softer border (`#4f82e6`) and deeper shadow

## 验证

- Incremental Jekyll build 成功（仅剩下预先存在的、无关的 Sass deprecation warning）。
- 渲染的输出中 **0** 个 `deepwiki-badge` 出现。
- 编译后的 CSS 现在包含 `.dark-mode .deepwiki-form` 规则（带有 `#2a2a2a` 背景），并且 form/input/submit 样式保持完整。

注意：我**没有**改动 `_includes/header.html` 中单独的 "Devin" header icon-button，该按钮也链接到 DeepWiki — 如果您也想要移除它，请告诉我。

这些编辑尚未提交。要我执行 `git add` + commit（并 push）吗？另外，提醒一下：之前 `git push origin main` 到 GitHub 的操作被中止了，因此之前的提交仍然不在 GitHub 远程仓库中。
