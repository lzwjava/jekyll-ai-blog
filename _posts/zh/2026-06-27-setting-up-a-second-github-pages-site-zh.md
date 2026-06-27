---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 搭建第二个 GitHub Pages 站点
translated: true
type: note
---

问题：我已经有一个 `*.github.io` 站点（我的博客）。我想为我的 `sec-edgar-gpt` 仓库创建第二个 GitHub Pages 站点，并通过不同的 URL 提供服务。该怎么做？

答案：

你混淆了两个概念。GitHub 提供 **一个用户站点**（`lzwjava.github.io`），但 **无限的项目站点**。你的 `sec-edgar-gpt` 仓库会自动获得一个项目站点，地址为：

```
https://lzwjava.github.io/sec-edgar-gpt
```

这是同一域名下的一个 *路径*，而不是新的子域名。GitHub Pages 不会为你提供 `sec-edgar-gpt.github.io` —— 每个账户只有 `<username>.github.io`。

## 选项 1：项目页面（零额外成本，请先尝试此方案）

在仓库上启用 Pages：

```bash
# 仓库 Settings → Pages → Source: deploy from branch (main, /root 或 /docs)
# 或者推送 gh-pages 分支
```

如果你有 `index.html` 或 `docs/` 文件夹，请相应设置源。完成 —— 地址为 `lzwjava.github.io/sec-edgar-gpt`。

## 选项 2：自定义域名（你真正想要的）

购买一个域名（或使用你拥有的域名的子域名），并将其指向项目仓库。每个仓库可以通过 `CNAME` 文件拥有**各自的自定义域名**。

```bash
# 在 sec-edgar-gpt 仓库根目录（或 /docs）
echo "sec-edgar-gpt.lzwjava.com" > CNAME
git add CNAME && git commit -m "custom domain" && git push
```

DNS 方面——对于**子域名**，在你的 DNS 提供商处添加 CNAME 记录：

```
类型   名称             值
CNAME  sec-edgar-gpt    lzwjava.github.io.
```

对于**根域名**（`example.com`），则应使用指向 GitHub IP 的 A 记录：

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

然后在仓库 Settings → Pages → Custom domain 中输入域名，待证书配置完成后（大约需要 15 分钟到几小时），勾选 "Enforce HTTPS"。

## 需要了解的关键限制

你的博客已经作为 **用户站点** 占用了 `lzwjava.github.io`。为某个 *项目* 仓库添加自定义域名不会影响它——它们是独立的。你可以为每个项目赋予自己的子域名（`sec-edgar-gpt.lzwjava.com`、`ww.lzwjava.com` 等），全部来自同一个 DNS 区域。

## 针对你的发展路径的建议

既然你维护知识库并发布很多工具，建议设置通配符模式：拥有 `lzwjava.com`，通过独立的 CNAME 将 `*.lzwjava.com` 指向 `lzwjava.github.io`，并为每个项目分配一个子域名。简洁、可扩展，论文站点可以变成 `sec-edgar-gpt.lzwjava.com`。

如果你不想购买域名，只需使用选项 1——`lzwjava.github.io/sec-edgar-gpt` 对于论文落地页来说也完全够用。

参考：

- [GitHub Pages — 站点类型](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)
- [为 GitHub Pages 站点管理自定义域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
