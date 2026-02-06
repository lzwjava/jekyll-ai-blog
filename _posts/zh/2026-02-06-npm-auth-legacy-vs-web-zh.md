---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: npm 身份验证：传统模式与 Web 流模式比较
translated: true
type: note
---

npm 有两种 authentication types，决定了你如何登录和管理 credentials：

## `auth-type=legacy`

这是传统的 authentication 方法，npm 会将你的 credentials 以明文形式存储在本地的 `.npmrc` 文件中。当你运行 `npm login` 时，它会提示你输入 username、password 和 email，然后直接在 `.npmrc` 中存储一个 auth token，如下所示：

```
//registry.npmjs.org/:_authToken=npm_xxxxxxxxxxxxx
```

该 token 保存在用户主目录的 `.npmrc` 文件中，并用于随后所有向 registry 发起的经过身份验证的请求。这非常适合自动化系统和 CI/CD pipelines 等需要简单 token-based 方法的场景。

## `auth-type=web` (自 npm 9 起的默认值)

这是现代的基于浏览器（browser-based）的 authentication 流程。当你运行 `npm login` 时，它会：

1. 打开你的默认 web browser
2. 将你引导至 npmjs.com 的登录页面
3. 你通过网站进行身份验证（支持 2FA、SSO 等）
4. 网站将 auth token 发回给你的 npm CLI
5. token 像 legacy auth 一样存储在 `.npmrc` 中

这种方法更安全，因为你的 password 永远不会接触 command line，并且它支持更先进的身份验证方式，如 single sign-on 和 multi-factor authentication。

你可以在 `.npmrc` 中配置使用哪种方法：

```
auth-type=web    # 或 legacy
```

大多数用户应该使用 `web`，除非正在设置无法进行交互式浏览器登录的 automation。