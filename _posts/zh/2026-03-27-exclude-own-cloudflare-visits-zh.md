---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从 Cloudflare 解析中排除自己的访问
translated: true
type: note
---

**Question:** 我可以在 Safari 中（或在我的机器上）安装插件或扩展程序，以便在我的博客中排除 Cloudflare Web Analytics 统计我自己的访问吗？

**Answer:**

遗憾的是，**Cloudflare 并没有提供官方插件或内置功能来从 Web Analytics 中排除你自己的访问**。根据 Cloudflare community 的说法，目前无法直接在 dashboard 内部原生排除你对 Cloudflare Web Analytics 的访问。

不过，根据你的设置，有几种实用的 workaround：

---

## Method 1: 使用 Ad Blocker (Safari 最简单的方法)

Cloudflare Web Analytics 的 beacon script (`https://static.cloudflareinsights.com/beacon.min.js`) 会被 uBlock Origin 等 ad blockers 以及 Brave 等注重隐私的 browsers 拦截。这意味着如果你在 Safari 上安装了 ad blocker，它将阻止 beacon 发送数据，你的访问也将不再被统计。

- **Mac 上的 Safari:** 安装 [AdGuard for Safari](https://adguard.com/en/adguard-safari/overview.html) 或开启 Safari 内置的 **Intelligent Tracking Prevention**。许多 filter lists（如 EasyPrivacy）已经屏蔽了 `cloudflareinsights.com`。
- **iOS Safari:** 从 App Store 下载 content blocker 应用（例如 AdGuard, 1Blocker），并在 Safari Settings → Extensions 中启用它。

> ⚠️ 注意：Cloudflare 知道 analytics beacon 会被 ad blockers 拦截。但是，Cloudflare 的 **edge analytics**（适用于 Pro/Business/Enterprise plans）无法被拦截，因为它们是在 network 层级测量每一次请求的。因此，此方法仅适用于基于 JS beacon 的 Web Analytics（免费版）。

---

## Method 2: 通过机器上的 `/etc/hosts` 或 DNS 进行屏蔽

在你的 Mac 上，你可以在系统层级屏蔽 Cloudflare analytics domain：

1. 以 root 身份编辑 `/etc/hosts`：
   ```
   sudo nano /etc/hosts
   ```
2. 添加以下行：
   ```
   0.0.0.0 cloudflareinsights.com
   0.0.0.0 static.cloudflareinsights.com
   ```
3. 保存并刷新 DNS cache：
   ```
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   ```

这将屏蔽你机器上所有 browsers 的 beacon。

---

## Method 3: 修改博客代码 (localStorage Flag)

一种 developer 友好的方法是在你的博客上创建一个私有路由（例如 `/donottrack`），用于设置 `localStorage` flag。当该 flag 存在时，不将 Cloudflare Analytics script 添加到页面中，从而防止跟踪你的访问。从未访问过此路由的普通访客不会受到影响。

JavaScript 中的逻辑如下所示：

```javascript
if (!localStorage.getItem("notrack")) {
  // 正常添加 Cloudflare beacon script
  const script = document.createElement("script");
  script.src = "https://static.cloudflareinsights.com/beacon.min.js";
  script.setAttribute("data-cf-beacon", '{"token": "YOUR_TOKEN"}');
  document.body.appendChild(script);
}
```

访问一次 `/donottrack` 来设置 flag，你的 browser 在以后的访问中将停止发送 analytics 数据。如果你想重新为自己启用跟踪，还可以添加一个清除 flag 的按钮 (`localStorage.removeItem("notrack")`)。

---

## Summary Table

| Method | Effort | Works on Safari | Blocks All Browsers |
|---|---|---|---|
| Ad blocker extension | Low | ✅ Yes | ❌ Per browser |
| `/etc/hosts` block | Medium | ✅ Yes | ✅ Whole machine |
| localStorage flag in code | Medium-High | ✅ Yes | ✅ Per device (once set) |

**Ad blocker** 是最快的解决方案。**`/etc/hosts`** 方法在系统范围内最彻底。如果你能控制博客的源代码，**localStorage** 方案则是最优雅的。

---

**References:**

- [Cloudflare Community – Excluding own visits](https://community.cloudflare.com/t/how-to-eclude-my-own-visits-from-web-analytics/812198)
- [Cloudflare Web Analytics FAQ](https://developers.cloudflare.com/web-analytics/faq/)
- [Hide your own visits from Cloudflare Analytics with JavaScript](https://www.shedloadofcode.com/blog/hide-your-own-site-visits-from-cloudflare-analytics-with-javascript/)