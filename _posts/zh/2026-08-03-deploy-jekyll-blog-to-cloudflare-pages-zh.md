---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Jekyll博客部署到Cloudflare Pages
translated: true
type: note
---

问题：如何部署一个类似 `lzwjava/jekyll-ai-blog` 的 Cloudflare 网站？

回答：

Jekyll 博客是一个**静态站点**，因此最佳的 Cloudflare 部署路径是：

```
GitHub 仓库
    |
    | 推送
    v
Cloudflare Pages 构建
    |
    | Jekyll 构建
    v
静态 HTML/CSS/JS
    |
    v
Cloudflare CDN + 自定义域名
```

无需虚拟专用服务器。

## 1. 准备 Jekyll 仓库

你的仓库：

```
https://github.com/lzwjava/jekyll-ai-blog
```

应包含如下内容：

```
.
├── _config.yml
├── _posts/
├── index.md
├── Gemfile
├── Gemfile.lock
├── assets/
└── _layouts/
```

本地测试：

```bash
git clone https://github.com/lzwjava/jekyll-ai-blog.git
cd jekyll-ai-blog

bundle install
bundle exec jekyll serve
```

打开：

```
http://localhost:4000
```

---

## 2. 创建 Cloudflare Pages 项目

访问：

Cloudflare 仪表盘 → Workers & Pages → 创建 → Pages → 连接到 Git

选择：

```
GitHub
    |
    └── lzwjava/jekyll-ai-blog
```

---

## 3. 配置构建设置

Cloudflare Pages 需要：

### 框架预设

选择：

```
Jekyll
```

或手动设置：

构建命令：

```bash
bundle exec jekyll build
```

输出目录：

```
_site
```

环境：

```
Ruby 版本：3.2
```

---

## 4. 添加 Ruby 依赖

你的 `Gemfile`：

```ruby
source "https://rubygems.org"

gem "jekyll"
gem "github-pages"
```

提交：

```bash
git add Gemfile
git commit -m "设置 cloudflare pages"
git push
```

Cloudflare 会自动重新构建。

---

## 5. 添加自定义域名

例如：

```
blog.example.com
```

Cloudflare 操作：

```
Pages
 |
 └── 自定义域名
        |
        └── 添加域名
```

Cloudflare 会自动创建：

```
CNAME

blog.example.com
        |
        v
your-project.pages.dev
```

---

## 6. 可选：改用 GitHub Actions

另一种架构：

```
GitHub Actions
      |
      | bundle exec jekyll build
      |
      v
_site/
      |
      v
Cloudflare Pages 部署
```

示例：

`.github/workflows/deploy.yml`

{% raw %}

```yaml
name: 部署

on:
  push:
    branches:
      - main

jobs:
  构建:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'

      - run: bundle install
      - run: bundle exec jekyll build

      - uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          accountId: ${{ secrets.CF_ACCOUNT_ID }}
          directory: ./_site
```

{% endraw %}

---

## 针对你的博客

你当前的架构：

```
Jekyll
+
GitHub
+
Cloudflare CDN
```

实际上是一个非常优秀的技术 AI 博客设置。

优势：

* 零服务器维护
* 全球 CDN
* 自动 HTTPS
* 基于 Git 的发布
* 成本极低
* 良好的 SEO

典型工作流程：

```bash
vim _posts/2026-08-03-vllm-kernel.md

git add .
git commit -m "编写 vllm 文章"
git push
```

随后：

```
GitHub webhook
       |
       v
Cloudflare Pages 重新构建
       |
       v
约 1 分钟内上线
```

对于 AI 工程师博客来说，这种部署方式可能与许多开源项目相同：**以 Git 为数据库，以静态构建为应用，以 CDN 作为运行时。**
