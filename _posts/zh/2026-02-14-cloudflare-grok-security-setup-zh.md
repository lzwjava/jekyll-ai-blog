---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如同 Grok 设置般的 Cloudflare 安全配置
translated: true
type: note
---

Question: 如何集成像 Grok 网站那样的 Cloudflare 安全检查？

Answer: 

正如 xAI 官方的 trust/security 声明中所述，Grok 网站 (grok.x.ai) 主要使用 **Cloudflare WAF** (Web Application Firewall) 进行整体安全防护，包括 bot detection、DDoS protection 和威胁拦截。

然而，当人们提到类似于 Grok 等现代 AI/聊天网站的“安全检查”（特别是登录、注册、聊天输入框或 API endpoints）时，通常是指实现 **Cloudflare Turnstile**。这是 Cloudflare 推出的一种隐私友好型 CAPTCHA 替代方案，它通过运行不可见或非侵入式的检查来区分人类和 bot，而无需用户解答烦人的拼图。

Grok.x.ai 可能结合使用了 Cloudflare WAF managed rules + bot fight mode + 在敏感表单/操作上部署 Turnstile（这是 2025–2026 年高流量 AI 网站非常常见的模式）。

### Grok 最可能使用的配置（以及如何复制它）

1. **Cloudflare WAF + Bot Management**（核心防护 —— xAI 官方提到的内容）
   - 将你的域名通过 Cloudflare 进行 Proxy
   - 启用 Bot Fight Mode 或 Super Bot Fight Mode（免费/付费计划）
   - 开启 AI-specific bot blocking（自 2025 年年中以来，Cloudflare 默认拦截许多 AI scrapers）
   - 创建 WAF custom rules 来 challenge 或 block 可疑流量

2. **Cloudflare Turnstile**（用于表单/登录/聊天安全检查 —— 不可见的 bot detection）
   - 这就是大多数人在 2025–2026 年语境下所说的“像 Grok 网站一样”的功能

### 分步指南：集成 Cloudflare Turnstile（推荐用于表单/聊天保护）

**Step 1: 在 Cloudflare 中创建 Turnstile widget**
- 前往 dash.cloudflare.com → Turnstile
- 点击 "Add widget"
- 选择模式：
  - **Managed**（推荐 —— 大部分时间不可见）
  - **Non-interactive**（完全不可见）
  - **Interactive**（仅在可疑时显示）
- 添加你的域名
- 复制 **Site Key**（公钥）和 **Secret Key**（私钥）

**Step 2: 在前端添加 Turnstile (client-side)**
最常见的方法：

**A. 显式渲染（最灵活 —— 推荐用于聊天/输入表单）**

```html
<!-- 添加此脚本一次 -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- 在你想要放置 widget 的地方（登录、注册、消息输入等） -->
<form id="your-form">
  ...
  <div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY" data-callback="onTurnstileSuccess"></div>
  ...
</form>

<script>
function onTurnstileSuccess(token) {
  document.getElementById("cf-token").value = token; // 隐藏输入框
  // 或自动提交表单 / 启用按钮
}
</script>

<!-- 用于发送 token 的隐藏输入框 -->
<input type="hidden" name="cf-turnstile-response" id="cf-token">
```

**B. 用于 React / Next.js / Vue / 等** —— 使用官方 widgets 或 @marsidev/react-turnstile, cloudflare-turnstile-react 等库。

**Step 3: 在服务端验证 (非常重要！)**
将 token 发送到你的 backend 并进行校验：

**示例 —— Node.js / Express**

```js
const express = require('express');
const fetch = require('node-fetch');

app.post('/submit', async (req, res) => {
  const token = req.body['cf-turnstile-response'];
  if (!token) return res.status(400).json({ error: 'Missing token' });

  const verifyUrl = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
  const secret = 'YOUR_SECRET_KEY';

  const formData = new URLSearchParams();
  formData.append('secret', secret);
  formData.append('response', token);
  // 可选: formData.append('remoteip', req.ip);

  const result = await fetch(verifyUrl, {
    method: 'POST',
    body: formData,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

  const outcome = await result.json();

  if (outcome.success) {
    // Token 有效 → 处理表单/聊天消息
    res.json({ success: true });
  } else {
    res.status(400).json({ error: 'Verification failed', codes: outcome['error-codes'] });
  }
});
```

**Python (Flask/FastAPI), PHP, Go 等** —— 原理相同：向 `/siteverify` 发送带有 secret + token 的 POST 请求。

**Step 4: 可选 —— 结合 WAF**
- 在 Cloudflare dashboard → Security → WAF → Create rule
- 字段：`cf.turnstile.score < 0.3` → 操作：Block / Managed Challenge
- 这让 Cloudflare 能够自动 challenge 低置信度的访问者

通过这种配置，你可以获得类似于 2026 年知名 AI 网站（很可能也包括 Grok）所使用的不可见/类人安全检查。

References:  

- [xAI Trust Statement — 提到 Cloudflare WAF](https://x.ai/security)
- [Cloudflare Turnstile Official Documentation](https://developers.cloudflare.com/turnstile)
- [Turnstile Get Started Guide](https://developers.cloudflare.com/turnstile/get-started)