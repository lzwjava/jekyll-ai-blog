---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jekyll GitHub域名迁移限制
translated: true
type: note
---

问题：我能否在 Cloudflare Workers/Pages 上部署我的 Jekyll 博客，同时保留 `lzwjava.github.io` 域名？

回答：

不能——这个限制是根本性的，而不是配置问题。`*.github.io` 域名由 GitHub 拥有和控制。Cloudflare 无法在其不控制 DNS 的主机上提供服务，而你也无法将 `lzwjava.github.io` 指向除 GitHub Pages 以外的任何地方。

以下是为什么以及你实际可用的选项的详细说明。

**为什么不可能**

`lzwjava.github.io` 通过 GitHub 的 DNS（`github.io` 区域）解析，而不是你的。要将站点放在 Cloudflare Pages 后面，Cloudflare 需要是该区域的权威 DNS，或者在你拥有的域名下有一个指向 `your-project.pages.dev` 的 CNAME 记录。你既没有 `github.io` 的所有权，也没有其 DNS 控制权。GitHub 将 `<user>.github.io` 硬编码为从你的 Pages 仓库提供服务。你无法创建任何 DNS 记录来重定向它。

**你实际可以做什么**

自己构建 Jekyll 站点，然后将静态输出推送到 `lzwjava.github.io` 仓库。这可以保留域名，但将构建过程从 GitHub 托管的 Jekyll 迁移出来（这本身也是你想要的——自定义插件、更新的 Ruby 版本、更快的构建）：

```bash
# 在本地或 CI 中构建，然后将 _site 推送到 GitHub Pages 提供服务的分支
bundle exec jekyll build
# 将 _site 的内容提交到提供 gh-pages 服务的分支
```

更好的做法：让 GitHub Actions 构建，GitHub 提供服务。你可以在保留 `.github.io` 主机的同时完全控制工具链：

```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  push: { branches: [main] }
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with: { ruby-version: '3.3', bundler-cache: true }
      - run: bundle exec jekyll build
      - uses: actions/upload-pages-artifact@v3
        with: { path: _site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages }
    steps:
      - uses: actions/deploy-pages@v4
```

这是标准的“自带构建”模式——你完全摆脱了 GitHub 受限的 Jekyll 沙盒，同时仍然在 `lzwjava.github.io` 上提供服务。

**如果你真的想要 Cloudflare Pages**

你需要一个你拥有的域名（例如 `lzwjava.com`）。然后 Cloudflare Pages 为其提供服务，你也可以选择将 `lzwjava.github.io` 保留为重定向（一个很小的 GitHub Pages 仓库，使用 meta-refresh 或仅使用 JS 重定向到顶级域名）。这是大多数人最终会采取的做法——拥有顶级域名，将 `.github.io` 视为一个旧版重定向。自定义域名还让你完全脱离 GitHub，这与你的自主/自托管偏好非常契合。

所以真正的问题不是“Workers/Pages + github.io”（这不可能），而是“我是否要注册 `lzwjava.com` 并迁移？”考虑到你发表了大约 400 篇文章和 8000 条笔记，仅为了可移植性，拥有顶级域名每年花费 10 美元就非常值得——你将从此不再受限于任何服务商。