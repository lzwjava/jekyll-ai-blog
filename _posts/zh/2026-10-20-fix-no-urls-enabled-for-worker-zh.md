---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复工作进程未启用URL的问题
translated: true
type: note
---

**问题：** 为什么我的 Cloudflare Worker 显示“No URLs enabled”，以及如何为其绑定域名？

**回答：**

**为什么会出现“No URLs enabled”**

你的 worker（`zhiwei-software`）已部署并准备就绪，但没有任何路由或域名与之关联——因此没有 URL 可以接受请求。Cloudflare 不会自动分配公共 URL；你必须启用以下至少一个选项。

---

**选项 1 — 启用免费的 `workers.dev` 子域名（最快）**

1. 转到你的 Worker → **Settings** 选项卡
2. 找到 **Workers.dev subdomain**（或“Domains & Routes”）
3. 将其切换为 **On**
4. 你的 Worker 可以在 `https://zhiwei-software.<your-subdomain>.workers.dev` 访问

---

**选项 2 — 绑定你的自定义域名 `zhiweisoft.site`**

既然你的账户中已经有 `zhiweisoft.site`：

1. 打开你的 Worker → **Domains** 选项卡（或 **Settings → Domains & Routes**）
2. 点击 **Add** → 选择 **Custom Domain**
3. 输入 `zhiweisoft.site` 或一个子域名如 `api.zhiweisoft.site`
4. Cloudflare 会自动创建 DNS 记录并提供 TLS 证书——无需额外配置
5. 等待约 1–2 分钟传播生效；之后 Worker 将在该域名的所有路径（`/*`）上响应

> **注意：** 要使自定义域名生效，`zhiweisoft.site` 必须**通过 Cloudflare 代理**（DNS 设置中的橙色云），由于它已出现在你的 Cloudflare 账户中，所以已经符合条件。

---

**选项 3 — 添加路由（用于部分路径匹配）**

如果你只想让 Worker 处理特定路径（例如 `zhiweisoft.site/api/*`）：

1. Worker → **Domains** 选项卡 → **Add** → **Route**
2. 输入类似 `zhiweisoft.site/api/*` 的模式
3. 选择区域（`zhiweisoft.site`）

---

**差异总结：**

| 方法 | URL | 使用场景 |
| --- | --- | --- |
| workers.dev | `zhiwei-software.xxx.workers.dev` | 测试 / 无自定义域名 |
| Custom Domain | `zhiweisoft.site` | 生产环境，所有流量 |
| Route | `zhiweisoft.site/api/*` | 仅特定路径 |

对于生产环境，**自定义域名**（选项 2）是最简洁的方法。

**参考资料：**

- [Cloudflare Workers – Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [Cloudflare Workers – Routes](https://developers.cloudflare.com/workers/configuration/routing/routes/)
- [Get started with Workers (domains & routing)](https://developers.cloudflare.com/workers/get-started/guide/)
