---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare 部署带凭证检查
translated: true
type: note
---

已完成。`.github/workflows/deploy.yml` 中的工作流现在会在每次推送到 `main` 分支时自动部署到 Cloudflare，并且首先进行快速失败的凭据检查。

变更内容：

- **添加了 `env:` 块**，使得来自 GitHub secrets 的 `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` 可用于 shell 步骤。
- **添加了 `Verify Cloudflare credentials` 步骤**（你的确切代码片段）——直接调用 Workers API，并在 token/account 错误时以清晰的 `::error::` 消息中止，而不是 wrangler 模糊的 `[code: 10000]`。
- **保留了 `Deploy to Cloudflare Pages` 步骤**——我没有像你的代码片段那样切换到 `npx wrangler deploy`，因为那样会失败。你的代码片段来自 `jekyll-ai-blog` 项目：它依赖于 `wrangler.jsonc` 配置和 worker entry，而该仓库中不存在这些。这个仓库是一个静态的单个 `index.html`，所以 `wrangler pages deploy ./`（已经正常工作）是正确的机制。verify 步骤对两者都有效。

YAML 已验证。推送到 `main` 分支，它将自动运行检查 + 部署。
