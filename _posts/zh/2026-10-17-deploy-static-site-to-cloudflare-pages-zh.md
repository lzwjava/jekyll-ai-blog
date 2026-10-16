---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将静态站点部署到 Cloudflare Pages
translated: true
type: note
---

问题：如何将静态网站部署到 Cloudflare？

答案：使用 Cloudflare Pages。对于静态网站，例如 HTML/CSS/JS、Jekyll 博客或预构建的 React/Vite 应用，你有两个主要选项：

- GitHub → Cloudflare Pages：最适合持续部署。每次推送到生产分支都会触发构建和部署。
- CLI → Cloudflare Pages：最适合直接从终端部署，无需连接 Git 仓库。

两者都提供 `*.pages.dev` URL，并且你可以连接自己的域名。&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages 文档

+1



## 选项 1：从终端部署

如果你已经有一个静态站点，这是最快速的部署方式。

例如，假设你构建好的网站位于 `dist/`：

```
cd my-site

# Authenticate with Cloudflare
npx wrangler login

# Create the Pages project (first deployment only)
npx wrangler pages project create my-site

# Deploy your static files
npx wrangler pages deploy dist --project-name=my-site
```

将 `dist` 替换为你的实际输出目录。对于纯 HTML 网站，它可能是 `.` 或 `public/`；对于 Vite，通常是 `dist/`。

你的网站将在以下地址可用：

`https://my-site.pages.dev`

官方指南：[Cloudflare Pages Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/?utm_source=chatgpt.com)。&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+1



## 选项 2：从 GitHub 自动部署

如果你积极维护网站或博客，推荐使用此方式。

1. 将你的网站推送到 GitHub 仓库。
2. 打开 [Cloudflare Dashboard](https://dash.cloudflare.com/?utm_source=chatgpt.com)。
3. 转到 Workers & Pages → 创建应用程序 → Pages → 导入现有的 Git 仓库。
4. 选择你的仓库并配置构建。

典型设置：

| 设置                | 纯 HTML          | Vite            |
| ---------------------- | --------------- | --------------- |
| 生产分支      | `main`          | `main`          |
| 构建命令          | `exit 0`        | `npm run build` |
| 构建输出目录 | `.` 或 `public` | `dist`          |

对于 Jekyll 站点，请使用适当的 Ruby/Jekyll 构建命令以及生成的输出目录，通常是 `_site`。

部署后，每次推送到 `main` 都会自动发布更新后的站点。&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages 文档

+1



## 选项 3：连接你自己的域名

部署后：

1. 在 Cloudflare 中打开你的 Pages 项目。
2. 转到 Custom domains。
3. 选择 Set up a custom domain。
4. 输入你的域名并按照 DNS 说明进行操作。

例如，你可以将站点托管在 `example.com` 而不是 `my-site.pages.dev`。

参见 [Custom domains in Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/?utm_source=chatgpt.com)。

## 你应该选择哪种方式？

对于你的工作流程，我会在生产网站中使用 GitHub + Cloudflare Pages，因为它能提供可复现的构建、版本历史和自动部署。当你想要从脚本或 AI 代理发布生成的站点时，请使用 Wrangler CLI。

一个重要的细节：在创建项目时选择 Git 集成或 Direct Upload。Cloudflare 不允许你将现有的 Direct Upload 项目转换为 Git 集成项目；切换需要创建新项目。&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages 文档

+1



一个问题：你正在部署哪种静态站点？

纯 HTML/CSS/JS

Jekyll 博客

Vite / React

Next.js 静态导出

其他

部署方式

终端 / CLI

GitHub 自动部署

Dashboard 上传

显示确切的部署步骤