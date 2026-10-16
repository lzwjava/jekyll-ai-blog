---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Namecheap域名连接到Cloudflare Pages
translated: true
type: note
---

你可以继续在 Namecheap 注册你的域名，并将静态网站托管在 Cloudflare Pages 上。你无需转移域名或更换注册商。

有两种方法：

- 推荐：保留 Namecheap 作为注册商，将 nameservers 改为 Cloudflare，并通过 Cloudflare 管理 DNS。
- 保留 Namecheap DNS，并将记录指向 Cloudflare Pages。这种方式较为受限：对于 apex 域名（如 `example.com`），Pages 自定义域名通常要求该域名是 Cloudflare 区域。对于 subdomain（如 `www.example.com`），你可以使用 CNAME 指向你的 Pages 站点。

## 第 1 步 — 将你的域名添加到 Cloudflare

1. 打开 [Cloudflare Dashboard](https://dash.cloudflare.com/?utm_source=chatgpt.com)。
2. 选择 Add a domain（或 Onboard a domain）。
3. 输入你的域名，例如 `example.com`。
4. 选择一个套餐；Free 套餐对于大多数静态网站来说已经足够。
5. 查看 Cloudflare 从 Namecheap 导入的 DNS 记录。

重要：在更改 nameservers 之前，请检查现有的 DNS 记录，尤其是邮件记录（MX、SPF、DKIM）以及任何现有的 subdomain。缺少记录可能会导致这些服务中断。

## 第 2 步 — 在 Namecheap 中更改 nameservers

当 Cloudflare 为你分配了两个 nameservers 之后：

1. 登录 [Namecheap Domain List](https://ap.www.namecheap.com/Domains/DomainList?utm_source=chatgpt.com)。
2. 点击你域名旁边的 Manage。
3. 在 Nameservers 下，选择 Custom DNS。
4. 输入 Cloudflare 分配给你的两个 nameservers。
5. 保存更改。

   [image](https://www.google.com/s2/favicons?domain=https://www.namecheap.com\&sz=32)

   Namecheap

   +1

不要从其他域名复制 nameservers；请使用 Cloudflare 分配给你的确切的一对。

## 第 3 步 — 将域名附加到 Pages

一旦 Cloudflare 显示你的域名为 Active：

1. 在 Cloudflare 中进入 Workers & Pages。
2. 打开你的 Pages 项目。
3. 选择 Custom domains → Set up a domain。
4. 输入你的域名，例如 `example.com`，然后按照提示操作。

Cloudflare 将配置必要的 DNS 记录并为该域名提供 HTTPS。

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1

## 第 4 步 — 验证一切

在终端中运行以下命令，将示例域名替换为你的域名：

```
dig NS example.com +short
dig example.com
curl -I https://example.com
```

检查以下事项：

- nameservers 是 Cloudflare 分配的那些。
- 域名能够正确解析。
- HTTPS 返回成功的响应，通常是 `200` 或类似 `301` 的重定向。

Nameserver 更改可能需要一段时间才能生效。

我的建议：保留 Namecheap 作为你的注册商，Cloudflare 作为你的 DNS/CDN，以及 Cloudflare Pages 作为你的静态托管。对于个人网站、文档站点或 AI 项目落地页来说，这是一个简洁的配置。

我还可以帮助你设置 `www` → apex-domain 重定向，并配置缓存规则，使你的静态网站拥有唯一的 canonical URL。
