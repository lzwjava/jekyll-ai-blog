---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenRouter API密钥过期修复
translated: true
type: note
---

原因很清楚：

**您的 OpenRouter API 密钥已失效/过期。** API 返回：

```
HTTP 401 — {"error":{"message":"User not found.","code":401}}
```

这意味着存储在 `OPENROUTER_API_KEY` 中的密钥在 OpenRouter 端已不存在——它可能已被撤销、过期，或者账户被删除/重建。

**解决方法：**
1. 前往 https://openrouter.ai/settings/keys
2. 生成新的 API 密钥
3. 更新您的 `.env` 文件：
   ```
   OPENROUTER_API_KEY=***
   ```
4. 请重新加载文件（`source .env`）或重启 shell，然后重试 `ww note`。

代理（`HTTP_PROXY=http://127.0.0.1:7890`）运行正常——请求能通过并收到响应。401 错误完全是密钥本身的认证问题。