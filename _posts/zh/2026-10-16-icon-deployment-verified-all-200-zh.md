---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 图标部署已验证，全部200
translated: true
type: note
---

所有 8 个图标引用均返回 **200**。已部署并验证。以下是摘要：

## 发生了什么

该项目的部署目标是 **GCP VM `live-server`**（34.150.108.243），而不是旧部署脚本指向的 AWS 机器。在 VM 上，移动端 SPA 通过 docker stack 运行：

- `/home/lzw/live-mobile-web` — 此仓库的源代码副本
- `docker compose --profile frontend run --rm frontend` — 将 vite 构建输出（`VITE_BASE_URL=/static/`）构建到 `live-server_frontend-dist` volume 中，该 volume 挂载到 `nginx` container 内（`/var/www/html/public/static`），服务于 `funlive.io`

## 所做的更改

| 文件 | 更改 |
| --- | --- |
| `index.html` | 添加了 8 个 favicon 链接（SVG、32/48/64/128/256 PNG、apple-touch-icon），使用仓库的根路径模式（如现有的 `/logo.png`） |
| `public/logo.png` | 替换为新图标（256px）— 同时在本地同步到 `static/logo.png` |
| `public/fun-live-icon/` | 完整图标集（32–1024 PNG + SVG） |
| `public/apple-touch-icon.png` | 180×180，用于 iOS |
| VM `nginx.conf` | 在两个移动端 server block 中添加了根路径别名 `location = /apple-touch-icon.png` 和 `location ^~ /fun-live-icon/`（备份保存为 `nginx.conf.bak.funlive-icon`），然后 `nginx -t` ✓ + reload |

## 在线验证（全部 200）

- `https://funlive.io/` — 已提供新的 HTML
- `/logo.png`、`/apple-touch-icon.png`（根路径获取，包括 iOS 自动请求）
- `/fun-live-icon/fun-live-icon.svg` + 所有尺寸引用
- 所提供的 `index.html` 中的每个图标 `href`

一点说明：在验证过程中，我发现 vite 会将内置 HTML 中的根图标引用重写为 `/static/...`（由现有的 `/static/` location 提供服务）。我添加的 nginx root aliases 仍然值得保留——iOS Safari 直接向根路径请求 `/apple-touch-icon.png`，绕过了 HTML 链接。
