---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wrangler 路由更新与部署
translated: true
type: note
---

已完成。以下是当前状态：

## ✅ `wrangler.jsonc` 已更新并验证

```jsonc
"routes": [
  { "pattern": "lzwjava.com", "custom_domain": true },
  { "pattern": "www.lzwjava.com", "custom_domain": true },
  { "pattern": "*.lzwjava.com/*", "zone_name": "lzwjava.com" }
]
```

三个有意为之的选择：

1. **两个 custom domains** — `www.lzwjava.com` 是缺失的部分；Cloudflare 会自动创建其 DNS 记录（这里没有冲突，因为 www 目前没有记录）。
2. **保留 wildcard route** — wrangler 在部署时会对 routes 进行 *覆盖*（全量同步）；如果没有该条目，现有的 `*.lzwjava.com/*` zone route 会在下次部署时被删除。
3. **添加 `zone_name`** — wrangler v4 会拒绝没有 zone 引用的普通 routes。

`npx wrangler deploy --dry-run` 顺利通过（7156 个文件，无绑定错误）。

## ⚠️ 现在不要在这台机器上运行 `wrangler deploy`

两个阻碍因素：

1. **`_site` 过期** — 最新内容是 2025-09-19，但 `_posts/` 里有 *今天* 的文章。直接部署会让线上网站回退约 10 个月。
2. **token 权限不足** — 它连 DNS 记录都无法 *读取*（auth error 10000），而创建 `www.lzwjava.com` custom domain 会自动创建 DNS 记录。这会在本地失败。

## 🚀 推荐路径（与您现有的 pipeline 匹配）

该项目通过 **Workers Builds** 部署（在 git push 时由 dashboard 侧执行 `bundle install && bundle exec jekyll build` —— 这里的 CI 只处理 GitHub Pages）。因此：

```bash
git add wrangler.jsonc
git commit -m "chore(worker): bind lzwjava.com and www.lzwjava.com custom domains"
git push origin main
```

Workers Builds 随后会：重新构建全新的 `_site` → 使用新 routes 进行部署 → 使用账户级权限（无 token 限制）创建 `www` custom domain。完成后（约 2–5 分钟），用以下命令验证：

```bash
curl -sI --max-time 15 https://www.lzwjava.com | head -5
```

需要我提交并推送到 `origin/main` 吗？
