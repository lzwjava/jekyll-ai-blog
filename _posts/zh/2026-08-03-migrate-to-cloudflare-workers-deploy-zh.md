---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 迁移到 Cloudflare Workers 部署
translated: true
type: note
---

已完成。以下是完整情况：

## 我所做的更改

**`.github/workflows/gh-pages.yml`**（提交 `17f9a67b6`）：

- ✅ 保留了所有自动化功能：语言翻译、笔记翻译、表格修复、Markdown 格式检查、测试、发布哈希——这些必须保留在 GitHub Actions 中，因为它们会将提交推送回仓库（Cloudflare 的构建会导致无限循环：推送 → 构建 → 推送 → ……）
- ❌ 移除了 GitHub Pages 步骤（`configure-pages`、`upload-pages-artifact`、`deploy-pages`）和 `github-pages` 环境
- ➕ 添加了 `部署到 Cloudflare Workers` 步骤：`npx wrangler deploy`——读取 `wrangler.jsonc` 并将新构建的 `_site` 上传到您的 `jekyll-ai-blog` Worker
- ➕ 从密钥中添加了 `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` 环境变量

## 您必须执行 2 项操作

**1. 添加 GitHub 密钥**（否则部署步骤会失败）：

- `CLOUDFLARE_API_TOKEN` — 在 dash.cloudflare.com → **我的资料 → API 令牌 → 创建令牌** → 模板 **"编辑 Cloudflare Workers"**（Workers 脚本：编辑）中创建。复制它。
- `CLOUDFLARE_ACCOUNT_ID` — dash.cloudflare.com → 右侧边栏显示您的账户 ID。
- 然后：GitHub 仓库 → **设置 → 密钥和变量 → Actions → 新建仓库密钥**，为每个密钥创建。

**2. 在 Cloudflare 面板中断开 Workers 构建**（Worker → **设置 → 构建 → 断开仓库连接**）。否则每次推送会同时触发 *GitHub Actions* 和 *Workers 构建* → 重复部署和版本混乱。GitHub Actions 成为唯一的部署工具；Worker 本身保持不变。

## 注意事项

- ⚠️ **您的 `lzwjava.github.io` 将停止更新**——此工作流之前负责部署它。如果您希望保留 Pages 作为备用，可以将其保留为第二步；请告知。
- 🌐 现在网站将位于 `jekyll-ai-blog.<your-subdomain>.workers.dev`（或者在 Worker → 设置 → 域和路由中添加自定义域名）。如果从不同域名提供服务，请在 `_config.yml` 中更新 `url:`——站点地图/SEO/订阅源会使用它。
- ⏰ 部署按 2 小时间隔运行 + 手动 `workflow_dispatch`（您之前移除了 `push:` 触发器以停止自取消循环——机器人提交会在下一个计划运行时部署，这是预期的行为）。

准备就绪后推送 `17f9a67b6`（以及之前的 `c33f924ca`）——并手动触发工作流（`Actions → 部署 Jekyll → 运行工作流`）以验证首次 Cloudflare 部署。
