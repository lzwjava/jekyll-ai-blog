---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工人修复牧马人
translated: true
type: note
---

完成。以下是发生的情况以及修复方式：

## 根本原因

您的仓库通过 GitHub Actions 部署到 **GitHub Pages** 是正常的。但您粘贴的错误来自一个 **单独的 Cloudflare Workers Builds 连接**——Cloudflare 的 CI 会运行 `npx wrangler deploy`，而由于该仓库没有 wrangler 配置，wrangler 缺少 Worker 名称 (`"undefined"`) 和 `compatibility_date`，导致硬失败。

## 已做的更改（提交为 `c33f924ca`）

**1. `wrangler.jsonc`（新建，位于仓库根目录）**——按照文档中 SSG/静态资源模式声明 Worker：
```jsonc
{
  "name": "jekyll-ai-blog",
  "compatibility_date": "2026-08-02",
  "assets": {
    "directory": "./_site",
    "not_found_handling": "404-page",
    "html_handling": "auto-trailing-slash"
  }
}
```
- `name` 修复了 "undefined" 警告；`compatibility_date` 修复了硬错误
- 没有 `main` 脚本——这是一个纯静态站点 Worker，提供 Jekyll 的 `_site` 输出
- 通过 `wrangler deploy --dry-run` 验证：读取了 7156 个文件，没有错误

**2. `_config.yml`**——排除了 `assets/epub/lzwjava-blog-en.epub`（31.8 MiB > Workers 的 25 MiB/文件限制；且未被任何地方引用）。实际上它已被 gitignore，因此不会影响 CI——这只是本地构建的一个无害安全网。

## ⚠️ 一个必需的仪表板步骤（无法通过仓库完成）

Workers Builds **不会从 `wrangler.jsonc` 读取构建命令**（文档已说明此限制）。由于 `_site` 被 gitignore，CI 克隆的仓库中没有构建好的站点。请在 Cloudflare 仪表板中操作：

> **您的 Worker → 设置 → 构建 → 构建命令：**
> ```
> bundle install && bundle exec jekyll build
> ```

Ruby 3.4.4 和 bundler 已预装在 Workers Builds 镜像中，因此 Jekyll 可以正常构建。（可选：启用 **构建缓存** 以加速 `bundle install`。）

## 然后

1. 执行 `git push`（修复内容必须在 Cloudflare 构建的仓库中）
2. 在仪表板中重试失败的构建（Workers Builds → 重试）——或者推送会触发新构建

## 注意

- 您的 GitHub Pages 工作流不受影响。
- 您博客中的两篇文章现在包含过时的建议：*"No Wrangler Config Needed"*（2026-08-03）和 *"Wrangler auto config causes Hugo error"*（2026-06-27）——它们得出的结论是 Workers 不需要配置，但 Workers Builds 特别需要。需要我更新它们吗？