---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 层差异导致分析分歧
translated: true
type: note
---

**问题：** 为什么 GoatCounter 和 Cloudflare Web Analytics 对同一个网站显示的结果差异如此之大？

**答案：**

它们在堆栈的不同层面衡量截然不同的东西。以下是对比分析：

## 层差异——这是核心原因

| | GoatCounter | Cloudflare 分析 |
| --- | --- | --- |
| **层** | 应用层（JavaScript） | 网络层（CDN 边缘） |
| **统计内容** | 通过 JS 执行获取的页面浏览量 | 到达 Cloudflare 的 HTTP 请求 |
| **运行位置** | 浏览器 | Cloudflare 的边缘节点 |

Cloudflare 能看到**每一个 HTTP 请求**——机器人、爬虫、健康检查、预取、资源获取、API 调用。而 GoatCounter 只在**用户浏览器执行 JavaScript 并且页面实际加载**时才会触发。

## 差异的具体原因

**Cloudflare 计数高于 GoatCounter：**

- **机器人和爬虫**——Googlebot、Bingbot、抓取工具都会发起 HTTP 请求。Cloudflare 会统计它们，但 GoatCounter 的 JS 不会运行。
- **静态资源请求**——每个 `.css`、`.js`、`.png`、`.woff2` 文件，Cloudflare 都会记录，而 GoatCounter 统计为零。
- **健康检查/在线监控**——比如 UptimeRobot 之类的工具每分钟都会访问你的网站。纯 HTTP 请求，没有 JS。
- **CDN 资源缓存命中**——一个包含 30 个资源的页面 = Cloudflare 记录 31 个请求，GoatCounter 记录 1 个事件。
- **链接预取**——浏览器和搜索引擎会在不“访问”的情况下推测性地获取 URL。
- **JavaScript 被屏蔽**——使用 uBlock、NoScript 或严格隐私设置的用户会屏蔽跟踪脚本。Cloudflare 仍然能看到他们的请求。

**GoatCounter 计数高于 Cloudflare（罕见但可能）：**

- **带有客户端路由的 SPA 应用**——如果你为每个路由变化都触发跟踪，GoatCounter 可能会对单个“页面”多次触发。Cloudflare 只看到最初的 HTML 请求。
- **手动调用 `count()`**——如果不小心重复触发了跟踪器。

## 你会看到的典型差距

对于一个典型的静态站点 / GitHub Pages / Jekyll 博客：

- Cloudflare 显示的“请求数”可能是 GoatCounter 页面浏览量的 **3–10 倍**
- 如果你看 Cloudflare 的**独立访客数**（而不是请求数），差距会缩小，但由于机器人流量和按 IP 分组的资源请求，仍然会有差异。

## 各自的实际用途

**GoatCounter** → 真实的用户页面浏览量、跳出率、真实用户的来源。更准确地反映“有多少人阅读了这篇文章”。

**Cloudflare** → 带宽、攻击检测、缓存命中率、机器人流量规模、CDN 性能。适合回答基础设施层面的问题。

## 如何让它们更具可比性

在 Cloudflare 中，过滤条件设置为：

- **仅 HTML 请求**（Content-Type: text/html）
- 排除已知的机器人 User-Agent
- 专门查看“页面浏览量”指标（而不是总请求数）

即便如此，Cloudflare 仍然会更高，因为它还会统计：

- JavaScript 被禁用的用户
- 屏蔽了 GoatCounter 域名的用户
- 从未实际渲染的预取请求

## 快速理解模型

```
Cloudflare 计数
= 人类页面浏览量
+ 机器人请求
+ 资源请求（CSS/JS/图片）
+ 健康检查
+ 预取请求
+ JS 被屏蔽的用户

GoatCounter 计数
= 人类页面浏览量（JS 成功执行）
- 屏蔽了跟踪器的用户
- 禁用 JS 的用户
```

对于你的博客 `lzwjava.github.io`，差距很可能主要来自 **Googlebot 和其他爬虫**（技术博客通常会被大量索引）以及**资源请求**（如果 Cloudflare 代理了所有内容，包括静态文件）。
