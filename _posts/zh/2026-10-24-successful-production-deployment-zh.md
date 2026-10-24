---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 成功的生产部署
translated: true
type: note
---

🎉 **成功部署到生产环境** — 解析到 `prod` 环境机密，并且站点已上线：

- **URL:** <https://truth-lab.pages.dev> (HTTP 200，标题：*Truth Lab — 一个单人 AI 研究实验室*)
- **部署预览:** <https://66b2ffaa.truth-lab.pages.dev>
- **运行:** `40088249315` — 成功，34 秒（验证凭证 → 创建项目 → 部署）

实际过程中按顺序出现的问题：

1. **机密为空** → 原本作为 `prod` *环境*机密存储，但作业未声明 `environment: prod` → 添加了该声明。
2. **命令重复** → `wrangler-action@v3` 会添加前缀 `npx wrangler`，因此 `command: wrangler pages deploy ...` 实际上执行了 `wrangler wrangler pages deploy ...` → 删除了开头的 `wrangler`，后来改用简单的 `run:` 步骤，使用 `npx --yes wrangler`（也避免了该 action 不稳定的 npx 安装提示）。
3. **Pages 项目不存在** → 临时创建项目：`wrangler pages project create truth-lab --production-branch=main`（幂等 — 未来运行中无操作）。

站点：**<https://truth-lab.pages.dev>** — 已部署到 `prod` 环境并提供你的内容。现在每次推送到 `main` 分支都将自动验证并部署。
