---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM 注册表身份验证指南
translated: true
type: note
---

是的，你可以使用 `npm config set` 来配置 npm registry 的身份验证。以下是它的工作原理：

## Basic Usage

```bash
# 用于 _authToken (推荐)
npm config set //registry.npmjs.org/:_authToken "your-token-here"

# 用于 _auth (旧版)
npm config set //registry.npmjs.org/:_auth "base64-encoded-credentials"
```

注意语法：它是 `//registry.org/:_auth`（在 `_auth` 前有一个冒号），而不是 `//registry.org/_auth`。

## Difference between _auth and_authToken

**`_authToken`** (现代方法):

- 直接接收一个明文 authentication token
- 被大多数现代 registries 使用 (npm, GitHub Packages 等)
- token 将原样存储在你的 `.npmrc` 文件中
- 示例: `//registry.npmjs.org/:_authToken=npm_abc123xyz...`

**`_auth`** (旧版方法):

- 需要 `username:password` 格式的 base64 编码凭据
- 较旧的身份验证方法，现已较少使用
- 你需要自行对其进行编码：`echo -n "username:password" | base64`
- 示例: `//registry.npmjs.org/:_auth=dXNlcm5hbWU6cGFzc3dvcmQ=`

## Practical Example

对于像 GitHub Packages 这样的私有 registry：

```bash
npm config set //npm.pkg.github.com/:_authToken "ghp_yourGitHubToken"
```

对于 scoped packages，你可能还需要：

```bash
npm config set @yourscope:registry https://npm.pkg.github.com
```

大多数现代工作流使用 `_authToken`，因为它更简单且适用于基于 token 的身份验证系统。`_auth` 方法主要用于仍在使用用户名/密码验证的旧系统。
