---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare Worker 上线部署
translated: true
type: note
---

**已解决 — https://truthlab.cc/ 已上线并部署了最新内容。**

调查发现你的站点实际上已是一个名为 `truth-lab` 的 **Cloudflare Worker**（route 为 `*.truthlab.cc/*`），而非 Pages 项目。因此，你原来的 `npx wrangler deploy` snippet 是正确的，而我之前错误地 deploy 了一个 Pages 项目。具体变更如下：

1. **`wrangler.jsonc`**（新增） — `name: truth-lab`, `assets: ./` 用于提供 static repo root 的内容，`workers_dev: false` 确保不会在 workers.dev subdomain 下 spawn 任何内容。
2. **`src/index.js`**（新增） — 最小的 entry point；static assets 在此之前由 Workers Static Assets 自动 serve。
3. **Workflow** — 现在流程简化为：checkout → verify credentials (fail-fast) → `npx --yes wrangler deploy`。现有的 `*.truthlab.cc/* → truth-lab` route 意味着每次向 `main` push 都会自动 update truthlab.cc。
4. **Cleanup** — 删除了意外创建的 `truth-lab` Pages project（`truth-lab.pages.dev`，即你原本不需要的），并 purge 了 Cloudflare cache。

验证结果：`curl https://truthlab.cc/` 返回的 SHA-256 值（`86e950f2…`）与 repo 中 `index.html` 的 byte 完全一致，返回 HTTP 200。当前 deploy version 为 `db2412b4`。

一点说明：两次较早的 probe 操作仍作为 commits 保留在 git history 中，并且 workflow file 现已精简到最简状态。domain 的 apex（`truthlab.cc`）已设置为 proxy 状态并位于 Cloudflare 的 DNS 上，因此 HTTPS 和 edge caching 都能直接开箱即用。