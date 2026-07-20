---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Google OAuth 令牌过期与续期
translated: true
type: note
---

问题：`ww gen-video upload` 使用的 Google OAuth 授权何时过期，能否延长？

回答：

根据这条日志：

```
scope=https://www.googleapis.com/auth/youtube
access_type=offline
```

你使用的是 **Google OAuth 2.0 离线访问模式**。

存在两种不同的过期机制：

1. **访问令牌 (Access token)**

    * 通常约 **1 小时** 后过期。
    * 如果你的上传成功后又等待了半小时，它仍然有效。
    * 通常不需要 **手动延长** 它。

2. **刷新令牌 (Refresh token)**

    * 这是 `access_type=offline` 赋予你的机制。
    * 它可以长期有效（通常数月/数年），用于自动获取新的访问令牌。
    * 它没有固定的 "30 分钟" 过期时间。

所以如果你的问题是：

> "半小时后，我还能继续上传吗？"

是的。半小时不算什么；访问令牌很可能仍然有效。

如果你的问题是：

> "我能让令牌的有效期超过 1 小时吗？"

不，访问令牌不行。正确的设计是：

```
refresh_token
      |
      v
Google OAuth token endpoint
      |
      v
new access_token (1 hour)
      |
      v
YouTube Data API upload
```

你的 CLI 工具应当安全地存储刷新令牌并自动刷新：

```python
creds = Credentials(
    token=access_token,
    refresh_token=refresh_token,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/youtube"],
)

if creds.expired:
    creds.refresh(Request())
```

对于像 `ww` 这样的个人 CLI 工具，常规工作流程是：

```
首次运行：
    浏览器 OAuth 登录
    保存刷新令牌

后续运行：
    无需浏览器
    自动刷新
    上传视频
```

还有一点：如果你看到此前的错误：

```
Access blocked: ZhiweiTextToSpeech has not completed the Google verification process
```

这与令牌有效期无关。这是 **OAuth 同意屏幕/测试用户问题**。对于个人 YouTube 上传工具，请将应用保留在 **测试** 模式，并将你的 Google 账号添加为测试用户；如果需要其他用户授权，则需发布 OAuth 应用。
