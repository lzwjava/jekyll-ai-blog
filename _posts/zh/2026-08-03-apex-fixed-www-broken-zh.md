---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 顶点修复，网络损坏
translated: true
type: note
---

## 结论：修复**已生效** — `lzwjava.com` 完全正常工作。但 `www.lzwjava.com` **仍然有问题**（无 DNS 记录）

我端到端验证了实时状态。以下是证据：

### ✅ 主域名 `lzwjava.com` — 已修复且正常工作

| 检查项 | 结果 |
| --- | --- |
| 名称服务器 | `barbara.ns.cloudflare.com` / `dion.ns.cloudflare.com` → Cloudflare 权威（陷阱 #2 不适用） |
| 自定义域名绑定 | 存在于 Worker：`lzwjava.com` → `jekyll-ai-blog`，`enabled: true`，`cert_id` 已签发 |
| 主域名 DNS | 代理的 A/AAAA 记录（104.21.62.122 / 172.67.223.135 — Cloudflare IP）→ 冲突记录已删除，Cloudflare 自动创建了自己的记录 |
| TLS 证书 | `CN=lzwjava.com`，SAN `lzwjava.com` + `*.lzwjava.com`，由 Google Trust Services 签发（Cloudflare 通用 SSL） |
| HTTP | `http://lzwjava.com` → **301** → `https://lzwjava.com` → **200 OK**，`server: cloudflare`，`cf-cache-status: HIT` |
| 内容 | 提供博客服务：`<title>李智维 | truth freedom</title>` |

### ❌ `www.lzwjava.com` — 仍然无法工作

- 完全没有 DNS 记录（即使直接查询 `barbara.ns.cloudflare.com` 也返回空结果）→ `www.lzwjava.com` 无法解析，无 TLS，无连接。
- 该区域有一条 **路由** `*.lzwjava.com/*` → `jekyll-ai-blog`，因此*路由*会起作用，但旧路由不会像自定义域名那样自动创建 DNS 记录。通配符证书 `*.lzwjava.com` 已经存在，因此唯一缺失的就是 DNS 记录。

### 关于我发现的情况说明

- 你仓库中的 `wrangler.jsonc` **尚未包含 `routes`/`custom_domain` 条目** — 主域名的绑定一定是通过仪表板或一次性部署完成的。Git 历史显示你已经记录过这个完整的过程（`60bfdf2eb` "custom domain DNS conflict fix"，`6f5284659` "enabling HTTPS on Cloudflare"）。
- 环境变量中的 API 令牌（`CLOUDFLARE_API_TOKEN`）**缺少 DNS 权限** — `dns_records` 返回 `Authentication error`（代码 10000）— 因此我通过公共 DNS 验证了记录状态。之前的 `dig` 超时只是由于本地 `127.0.0.1:7890` 代理环境的干扰。

### 完成 `www` 的配置（2 个选项）

```jsonc
// wrangler.jsonc — 推荐，与你的修复记录路径相同
"routes": [
  { "pattern": "lzwjava.com", "custom_domain": true },
  { "pattern": "www.lzwjava.com", "custom_domain": true }
]
```

或者，如果你只想要一个简单的重定向：添加一条 **代理的** `CNAME www → lzwjava.com` 记录（现有的 `*.lzwjava.com` 路由 + 通配符证书处理其余部分）。注意你需要一个具有 DNS 编辑权限的令牌，因为当前的令牌无法操作记录。

需要我更新 `wrangler.jsonc` 添加路由，和/或检查从此处运行 `npx wrangler deploy` 是否安全吗？
