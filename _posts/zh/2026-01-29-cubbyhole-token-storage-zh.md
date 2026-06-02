---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 暗室机密令牌作用域存储
translated: true
type: note
---

你想到的是 **Cubbyhole**，而不是 "chubbyhole"（这是一个常见的错误！）。

是的，你对其工作原理的理解基本正确。Cubbyhole secret engine 是 Vault 中基于每个 token 的独立 secret 存储空间。以下是它的特殊之处：

**核心特性：**

- **Token-scoped**：每个 token 都有自己私有的 cubbyhole，只有该 token 才能访问。
- **完全隔离**：即使是 root tokens 或其他高权限 tokens 也无法读取另一个 token 的 cubbyhole。
- **生命周期与 token 绑定**：当 token 过期或被 revoked 时，其 cubbyhole 及其所有 secrets 都会被自动删除。

**关于登录和消失的 secrets：**

当你“重新登录”时，你会获得一个 *new* token，这意味着获得了一个 *new* cubbyhole —— 所以是的，你之前 token 的 cubbyhole 中的 secrets 将会消失（它们在旧 token 过期/被 revoked 时就消失了）。你将无法访问旧 cubbyhole 的内容。

**常见用例：**

Cubbyhole 常用于安全的 secret 传递 —— 例如，在 response wrapping 中，Vault 将一个 secret 封装在一个单次使用的 token 中，该 token 的 cubbyhole 包含真正的 secret。一旦该 token 被用于 unwrap secret，该 token 就会被 revoked，cubbyhole 也会随之消失。

因此，它是刻意设计为 ephemeral（临时性）并与 token 的生命周期绑定的 —— 非常适合临时 secret 存储或安全交接，但不适用于长期 secret 存储。
