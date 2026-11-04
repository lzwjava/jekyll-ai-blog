---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 推送到原始主分支的干净操作
translated: true
type: note
---

已推送至 `origin/main`。

- 所有内容均已提交至 `682eb03`（工作树干净，没有新内容添加）。
- 推送至 `git@github.com:lzwjava/hugo-ai-blog.git`，新分支 `main`，上游跟踪已设置。
- 验证：远程 `refs/heads/main` = `682eb03`，本地分支同步（`## main`，无超前/滞后标记）。

注意：`public/`、`resources/_gen/` 和 `hugo_stats.json` 被 git 忽略，因此只有源文件被推送——网站需要由您的主机（Netlify/Cloudflare Pages/GitHub Actions）构建，而不是提交。