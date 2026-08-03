---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 直接GitHub Pages部署工作流
translated: true
type: note
---

已完成。工作流程现在在此仓库中构建 `_site`，并通过标准的 GitHub Pages 操作进行部署，而不是推送到 `lzwjava/lzwjava.github.io`。

**`.github/workflows/gh-pages.yml` 中的更改：**

- 移除了 `Check out destination repo` 和 `Sync built site to destination repo` 步骤（不再使用 PAT_TOKEN / rsync 推送到第二个仓库）
- 在 `Build with Jekyll`（已输出 `./_site`）之后添加了标准的 Pages 部署链：
  - `actions/configure-pages@v5` → `actions/upload-pages-artifact@v3` (路径 `_site`) → `actions/deploy-pages@v4`
- 启用了对 `main` 分支的 `push` 触发（根据您的模板），保留了每 2 小时的定时计划和 `workflow_dispatch`
- 从部署步骤输出中设置环境 URL，并发组现在为 `pages`

**`_config.yml`：**

- 设置 `baseurl: "/jekyll-ai-blog"` — 由于站点现在位于此仓库中，GitHub Pages 将在 `https://lzwjava.github.io/jekyll-ai-blog/` 提供服务。如果没有此设置，所有资产/链接/永久链接路径都会出错。

需要注意两点：

1. 在仓库的 **Settings → Pages** 中，将 Source 设置为 **GitHub Actions**（如果之前设置为某个分支）。
2. 此工作流程不再使用 `PAT_TOKEN` 密钥。

请记住，翻译步骤会提交并推送到 `main`，因此使用新的 push 触发时，每次提交都会重新运行流水线（翻译是幂等的，因此它在无操作运行后会稳定下来，仅重新构建/部署）。
