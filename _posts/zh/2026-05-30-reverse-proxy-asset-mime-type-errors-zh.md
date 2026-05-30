---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 反向代理资产MIME类型错误
translated: true
type: note
---

**问题：** 为什么 `https://liber.davirain.xyz` 的 CSS 和 JS 资源会抛出 MIME 类型错误？

**回答：**

这是典型的**反向代理配置错误**或**资源路径路由错误**。具体原因如下：

## 根本原因

浏览器请求 `https://liber.davirain.xyz/assets/index-KsAjyADz.css` 时，服务器返回的是 `Content-Type: text/html` 而非 `text/css`。JS 文件同理——返回了 `text/html` 而非预期的 `application/javascript`。

这意味着服务器对于这些资源 URL **返回的是 HTML 页面**（很可能是 404 页面或 index.html 兜底页面），而非实际文件。

## 发生原因

**按可能性排序的最常见原因：**

### 1. SPA 兜底配置错误（最常见）
服务器存在捕获所有未匹配路由并返回 `index.html` 的规则——包括 `/assets/*` 路径。这是 Nginx/Caddy 中常见的 SPA 配置错误：

```nginx
# 错误：这条规则也会捕获 /assets/*
location / {
    try_files $uri $uri/ /index.html;
}
```

修复方案：资源应在兜底规则之前被处理：
```nginx
location /assets/ {
    root /var/www/dist;
    # 此处不要加 try_files 兜底
}

location / {
    try_files $uri /index.html;
}
```

### 2. 资源未部署/构建输出路径错误
`/assets/` 目录未上传，或构建输出目录配置错误。服务器找不到文件 → 返回 404 HTML 页面。

验证方法：`curl -I https://liber.davirain.xyz/assets/index-KsAjyADz.css`——如果返回 `200` 且 `Content-Type: text/html`，说明在返回 index.html。如果返回 `404`，则说明资源不存在。

### 3. CDN/代理剥离路径
反向代理（Cloudflare、Nginx 上游服务器）将 `/assets/...` 重写为 `/`，并返回根目录的 HTML。

### 4. Vite/构建配置中 `base` 设置错误
应用使用非根路径的 base（例如 `base: '/subpath/'`）构建，但部署在根路径下，导致资源 URL 解析到错误路径：

```js
// vite.config.js
export default {
  base: '/liber/'  // 资源路径变为 /liber/assets/... 但部署在 /
}
```

## 快速诊断

```bash
# 检查服务器对 CSS 文件的实际响应
curl -sv https://liber.davirain.xyz/assets/index-KsAjyADz.css 2>&1 | grep -E "content-type|HTTP/"

# 检查是否返回 HTML
curl -s https://liber.davirain.xyz/assets/index-KsAjyADz.css | head -5
```

如果输出以 `<!DOCTYPE html>` 开头——确认问题：服务器对资源请求返回了 index.html。

## 修复方案

取决于技术栈。如果是 Nginx 上的静态站点：

```nginx
server {
    listen 443 ssl;
    server_name liber.davirain.xyz;
    root /var/www/liber/dist;
    index index.html;

    # 直接处理静态资源
    location ~* \.(js|css|png|jpg|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;  # 返回 404，而非兜底到 index.html
    }

    # SPA 兜底仅针对 HTML 路由
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

如果托管在 GitHub Pages / Vercel / Netlify ——问题几乎肯定出在 `vite.config.js` 中的 `base` 配置，或构建产物未放置在正确目录。