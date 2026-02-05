---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 简单详解 Jenkins 凭据类型
translated: true
type: note
---

是的，没错！Jenkins credentials 支持多种 authentication 类型：

## Username and Password

- **Username with password** - 传统的 credentials，提供 username 和 password
- 安全地存储在 Jenkins 的 credential store 中
- 适用于基本的 authentication 场景

## Token/Secret Text

- **Secret text** - 用于存储单个 secret 值，例如 API tokens、OAuth tokens 或 access keys
- **Secret file** - 用于存储 credential 文件，例如 SSH keys 或 certificates

## Other Authentication Types

Jenkins 还支持：

- **SSH Username with private key** - 用于基于 SSH 的 authentication
- **Certificate** - 用于基于 certificate 的 authentication
- **Username with password**（在许多情况下也可用于 username + personal access token）

## Using Tokens as Passwords

许多现代系统（如 GitHub、GitLab、Bitbucket）现在更倾向于使用 personal access tokens 而非 passwords。你通常可以通过两种方式使用它们：

1. **Username with password credential** - 使用你的 username，并将 token 填入 password 字段
2. **Secret text credential** - 如果系统只需要 token，则仅存储 token

例如，对于 GitHub：
- Username: your-github-username
- Password: ghp_yourPersonalAccessToken

选择哪种方式取决于你正在进行 authentication 的系统要求。你需要帮助在 Jenkins 中设置特定类型的 credential 吗？