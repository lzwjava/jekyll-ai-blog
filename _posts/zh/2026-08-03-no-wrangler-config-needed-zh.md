---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无需Wrangler配置
translated: true
type: note
---

简短回答：**不需要——这个项目不需要它。**

## 原因

你的仓库是一个通过 GitHub Actions 部署到 **Cloudflare Pages** 的 Jekyll blog（参见 `.github/workflows/gh-pages.yml` 和你的文章 `deploy-jekyll-blog-to-cloudflare-pages`）。Pages 部署完全不使用 `wrangler.jsonc`——这个项目中没有 Worker（我检查过：仓库中不存在任何 `wrangler.*` 文件）。因此，这个配置块是无效配置。

## 如果你将来*确实*添加了 Worker

那么这个配置块仍然是**可选的**：

- 对于新的 Worker，Observability（Workers Logs + Trace Logs）是**默认启用**的——完全省略 `observability` 意味着日志记录是开启的。
- 你只需要这个配置来**禁用**它或**调整采样率**（例如，`head_sampling_rate: 0.1` 可以记录 10% 的请求以节省费用）。

## 你粘贴的配置块是矛盾的

```jsonc
"observability": {
  "enabled": false,          // ← master switch: turns EVERYTHING off
  ...
  "logs": { "enabled": true } // ← but this says logs on
  ...
}
```

顶层的 `enabled: false` 优先级更高——嵌套的 `logs.enabled: true` 被忽略。不要照搬这个配置。

如果你希望在未来的 Worker 上实现简单、合理的日志记录，请使用最简形式：

```jsonc
"observability": {
  "enabled": true,
  "head_sampling_rate": 1
}
```

**总结：** 这里跳过它。你的 Pages 站点已经在 Cloudflare dashboard 中免费获取了请求日志，无需任何配置。