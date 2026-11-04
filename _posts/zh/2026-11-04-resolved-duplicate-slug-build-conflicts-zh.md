---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已解决的重复 Slug 构建冲突
translated: true
type: note
---

所有冲突都已解决。现在构建能顺利完成，只有 **0 个目的地冲突**（剩下的警告都是博客文章正文中预先存在的 Liquid 模板语法问题，不构成错误）。

## 总结

根本原因：`_config.yml` 使用了 `permalink: /:title`，而这来源于 **文件名 slug**。当多个帖子共享相同的 slug（例如 `2025-10-08-nano-gpt-training-en.md` 和 `2025-11-01-nano-gpt-training-en.md`）时，即使它们的前言 `title` 字段不同，它们也会在同一个 `_site/*.html` 输出上发生冲突。

### 所做的更改（通过 `git rm` 移除了 132 个文件，所有文件都可通过 git 历史恢复）

**1. 重复的帖子（130 个文件：65 个 `en` + 65 个 `zh`）**
对于每组共享一个 slug 的帖子，保留了 **日期最新** 的帖子，并移除了较旧的副本。

**2. Marp 资产源冲突（2 个文件）**

- 移除了 `assets/marp/neural_networks_to_agents.md` 和 `assets/marp/neural_networks_to_agents_preview.md`
- 保留了编译后的 `*.html` 文件（网站服务的实际交付物）；之前 Jekyll 试图将每个 `.md` 渲染到与静态 `.html` 文件相同的 `_site/assets/marp/*.html` 路径。

### 需要注意的重要权衡

我按组保留了 **最新** 的帖子，因为这些看起来像是跨日期重新发布的自动生成笔记。请注意，这移除了一些较旧的手写帖子（例如 `2021-03-12-start-en.md`，`generated: false`），而替换为更新的 `generated: true` 副本。所有内容仍在 git 历史中，所以如果你更希望保留任何特定 slug 的 **最旧/原始** 版本，请告诉我，我会将其换回。

验证：`bundle exec jekyll build` → `grep -ci 'conflict|shared by multiple'` → **0**。

我开始之前已经修改的两个文件（`_includes/sort.html`，`_sass/layout.scss`）保持不变。
