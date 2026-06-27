---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过Cloudflare Pages部署静态站点
translated: true
type: note
---

问题：如何使用 Cloudflare 部署一个简单的 `index.html`？

答案：

使用 **Cloudflare Pages**。它免费提供，可直接从仓库或直接上传提供静态文件，并为你分配一个 `*.pages.dev` 域名，还可选自定义域名——无需服务器。

## 最快方式：直接上传（无需 Git）

```bash
npm install -g wrangler
wrangler login            # 打开浏览器进行身份验证

mkdir my-site && cd my-site
echo "<h1>SEC EDGAR GPT</h1>" > index.html

# 将当前目录部署为 Pages 项目
wrangler pages deploy . --project-name=sec-edgar-gpt
```

输出会提供 `https://sec-edgar-gpt.pages.dev`。重新运行 `wrangler pages deploy .` 即可更新。

## 关联 Git（推送时自动部署）

控制面板 → Workers & Pages → 创建 → Pages → 连接到 Git → 选择 `lzwjava/sec-edgar-gpt`。

纯静态站点的构建设置：

```
框架预设：    无
构建命令：    （留空）
构建输出目录：/          # 如果 index.html 在 /docs 目录下，则填 /docs
```

每次向生产分支执行 `git push` 都会重新部署。访问地址为 `<项目名>.pages.dev`。

## 自定义域名

Pages → 你的项目 → 自定义域名 → 添加 `sec-edgar-gpt.lzwjava.com`。如果 `lzwjava.com` 的域名服务器已在 Cloudflare 上，DNS CNAME 记录会自动创建，HTTPS 也会自动配置。无需手动设置 A 记录或管理证书。

## Pages 与 Workers 的选择——选对工具

- **Cloudflare Pages** → 适用于静态 `index.html` 及资源文件。这正是你的场景。
- **Cloudflare Workers** → 如果你后续需要服务器端逻辑（例如 API 端点、为 EDGAR 工具提供的 LLM 代理）。Worker 也可以提供静态资源，但对于纯落地页，Pages 更简单。

## Pages 与 GitHub Pages 的选择——针对你的论文站点

两者都免费且支持静态内容。Cloudflare 的优势在于：需要更快的全球边缘缓存、已在使用 Cloudflare DNS、或后续需要接入 Worker（例如调用 LLM 的 `/query` 端点）。GitHub Pages 的优势在于：所有内容与仓库集中管理。对于 `sec-edgar-gpt` 这个具体项目——你可能希望有一个调用 LLM 的在线演示——我倾向于选择 Cloudflare，这样升级到 Worker 的路径只需一步。

参考资料：

- [Cloudflare Pages — 使用 Wrangler 直接上传](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Cloudflare Pages — Git 集成](https://developers.cloudflare.com/pages/get-started/git-integration/)