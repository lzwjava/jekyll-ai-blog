---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Cloudflare Secrets添加到GitHub
translated: true
type: note
---

你当前未在本机上登录 wrangler，因此最快的方式是通过控制面板：

1. 前往 **dash.cloudflare.com** 并登录
2. 查看控制面板的**右侧边栏**——你会看到一个显示你账户名称和 **Account ID**（32字符十六进制字符串）的区域，旁边有复制按钮

这就是你要的值。将其与 API token 一起作为仓库机密添加到 GitHub 中：

- GitHub 仓库 → **Settings → Secrets and variables → Actions → New repository secret**
- 名称：`CLOUDFLARE_ACCOUNT_ID` → 值：你的 32 字符 Account ID
- 名称：`CLOUDFLARE_API_TOKEN` → 值：从 **My Profile → API Tokens → Create Token**（模板 "Edit Cloudflare Workers"）获取的 token

一旦两个机密都设置好，工作流中的 `npx wrangler deploy` 就会使用该 token 进行身份验证，并准确知道要更新哪个账户下的 `jekyll-ai-blog` Worker。
