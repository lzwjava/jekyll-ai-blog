---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nginx 配置修复前后端 API 前缀
translated: true
type: note
---

## 完成 — `funlive.io` 现在可以渲染 Vue 应用了

```html
HTTP/1.1 200 OK
Content-Type: text/html
<title>趣直播 - 知识直播平台</title>
<div id="app">
<script src="/static/assets/index-CgRn8J2L.js">
```

已通过你的浏览器路径（代理）、直接 IP 以及虚拟机本地验证通过。

## 我发现的阻塞问题

前端和后端对 API 前缀的配置不一致。构建后的 bundle 中写死了 `baseURL:"/api"`，但 CI4 的路由中**没有**前缀：

```
/topics     → 200 {"status":"success"}     ← 实际后端路由
/api/topics → 404 Can't find a route for 'GET: api/topics'
```

如果我仅仅把 `/` 切到 SPA，那么所有 API 调用都会返回 404。原有的 `website.conf` 已经通过 `proxy_pass http://api.quzhiboapp.com/;` 解决了这个问题——末尾的斜杠会去掉 `/api/`。我复刻了这个方案，但需要做一些调整：CI4 4.7.5 从 `REQUEST_URI`（`uriProtocol = 'REQUEST_URI'`，会去掉 `SCRIPT_NAME`）读取路由，而不是 `PATH_INFO`，所以普通的 `proxy_pass` 去前缀会导致 CI4 看到的是 `api/topics`。配置文件会将去掉前缀后的路径作为 `REQUEST_URI` 传入。

## 对 `/home/lzw/live-server/nginx.conf` 的修改

已备份到 `nginx.conf.bak-1792096592`。共四个块：`/static/`（SPA 静态资源）、`/api/`（去掉前缀 → PHP-FPM）、`location = /`（SPA 入口），以及一个兜底的 `try_files` 规则，确保旧的无前缀路径仍然可以到达 CI4。在优雅执行 `nginx -s reload` 之前已通过 `nginx -t` 验证——无需重启容器。

| 测试 | 结果 |
| ------ | -------- |
| `/` → SPA HTML | 200，`text/html`，1897 字节 |
| `/api/topics`（前端的 baseURL） | 200 JSON ✅ 之前是 404 |
| `/topics`（旧的无前缀路径） | 200 JSON — 已保留 |
| JS / CSS / logo | 200，类型正确 |
| `/api/lives/count`、`?query` | 200 |
| **POST** `/api/login` 带请求体 | 200 — 请求体在重写后完好 |
| 未知的 `/api/*` | CI4 返回 404 JSON（正确，不是 SPA） |

路由基于 hash（`createWebHashHistory`），所以不需要服务端 SPA 兜底——浏览器只会请求 `/`。

## 仍未解决的问题

1. **Apex 域名 DNS** — `162.255.119.114` **仍然**指向 `funlive.io`。请在 Namecheap 中删除；目前大约 75% 的 apex 访问会得到 302 而不是站点内容。`www.funlive.io` 是干净的。
2. **`CI_ENVIRONMENT=development`**（第 25 行）— 仍在公网环境输出 Debugbar 头和堆栈跟踪信息，且 `DB_PASS` 硬编码在同一个文件中。我保留了它，因为你可能仍然需要错误详情，但它不应该进入生产环境。
3. **没有 HTTPS** — 443 端口没有监听；只有 `http://` 可用。
4. 次要问题：`/index.php?/topics` 可以直接访问。目前不可利用，但通常你应该阻止直接访问前端控制器。

注意：卷中的 bundle 构建于 10 月 15 日 18:27。如果你之后编辑过 `~/projects/live-mobile-web`，请使用 `docker compose --profile frontend up frontend` 重新构建——或者告诉我，我来执行。
