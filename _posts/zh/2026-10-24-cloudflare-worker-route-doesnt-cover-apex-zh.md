---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare Worker 路由未覆盖根域名
translated: true
type: note
---

**问题：** 为什么Cloudflare无法访问 `http://truthlab.cc`，即使已经配置了Worker route？

**回答：**

查看你的Cloudflare dashboard，有**两个可能的原因**：

---

### 1. ⚠️ Route Pattern未覆盖Apex Domain（主要问题）

你当前的Route是：

```
*.truthlab.cc/*
```

`*.` wildcard **仅匹配subdomains**（例如 `www.truthlab.cc`, `api.truthlab.cc`），但**不**匹配root/apex domain `truthlab.cc` 本身。因此访问 `http://truthlab.cc` 将无法匹配任何Worker route。

**Fix:** 为apex添加第二条route（或Custom Domain）：

| 添加内容 | 类型 |
|---|---|
| `truthlab.cc/*` | Route |

或者，更好的做法是从Routes切换到 **Custom Domains**，并添加两者：

- `truthlab.cc`
- `*.truthlab.cc`

Custom Domains更简单——Cloudflare会自动处理DNS并包含HTTPS。

---

### 2. DNS必须Proxied（Orange Cloud）Routes才能工作

如果你使用Routes（而不是Custom Domains），你的Cloudflare中 `truthlab.cc` 的DNS record必须是：

- **Proxied**（orange cloud ☁️），而不是DNS-only（grey cloud）
- 指向任意IP（例如 `192.0.2.1` 作为placeholder即可——Cloudflare会拦截它）

---

### 快速修复步骤

1. 前往 **Workers & Pages → truth-lab → Settings → Domains & Routes**
2. 点击 **Add** → 选择 **Custom Domain**
3. 输入 `truthlab.cc`（apex domain）
4. 可选，添加 `*.truthlab.cc` 作为第二个Custom Domain

Cloudflare会自动provision SSL并配置DNS。

---

**参考：**

- [Cloudflare Workers Routes vs Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/)
- [How route matching works (wildcard patterns)](https://developers.cloudflare.com/workers/configuration/routing/routes/#matching-behavior)
- [Custom Domains for Workers](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
