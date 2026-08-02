---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wrangler 10000 错误需要读取作用域
translated: true
type: note
---

问题：Wrangler 在 `/workers/services/...` 上的 `code: 10000` 认证错误是否需要读取范围（read scopes），而不仅仅是编辑范围？

答案：是的。代码 10000 是一个通用的 catch-all 错误——Cloudflare 不会告诉你具体缺少哪个权限，因此通常不是 Workers Edit 权限本身的问题，而是缺少 Wrangler 在启动会话时（甚至在调用部署之前）所需的读取级别范围。

Wrangler 使用的自定义 API 令牌的最小工作范围集：

```
Account Settings: Read     ← wrangler 调用 /accounts 解析 account_id
User Details: Read         ← wrangler 调用 /user 获取登录时的邮箱
Workers Scripts: Edit      ← 实际部署权限
Workers Routes: Edit       （如果使用 routes）
Workers KV Storage: Edit   （如果绑定 KV）
```

`User Details: Read` 是最容易被遗漏的——存在一个已知的 Wrangler 错误/行为：当缺少该范围时，它会以 `10000` 静默失败，而不是显示实际的“你是否缺少 User->User Details->Read 权限？”警告，尤其是在 CI/非交互式环境中，该警告会被吞掉。

快速检查令牌实际拥有什么以及需要什么的方法：

```bash
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer <CLOUDFLARE_API_TOKEN>" | jq
```

如果该请求返回 200，但 Wrangler 仍然在 `/workers/services/...` 上返回 10000，则几乎总是缺少 `Account Settings:Read` 或 `User Details:Read`——而不是 Workers 编辑范围，因为你能访问到特定服务端点，说明你显然已经拥有该权限。

最快的修复方法——不要手动选择范围，使用 Cloudflare 自己的模板，该模板正确捆绑了读写集合：

```
Dashboard → My Profile → API Tokens → Create Token
→ "Edit Cloudflare Workers" 模板
```

该模板包含 Account:Read、User:Read、Workers Scripts:Edit、Workers Routes:Edit、Workers KV:Edit、Zone:Read——其他遇到相同 10000 错误的用户通过从手动范围令牌切换到“Edit Cloudflare Workers”模板修复了该问题。

参考：

- [GitHub issue #2611 - 自定义令牌 10000](https://github.com/cloudflare/wrangler2/issues/2611)
- [Cloudflare Community - Wrangler Deploy 10000，通过模板修复](https://community.cloudflare.com/t/wrangler-deploy-workflows-10000-error/827149)
- [Cloudflare Community - Authentication 10000](https://community.cloudflare.com/t/authentication-10000/821086)
