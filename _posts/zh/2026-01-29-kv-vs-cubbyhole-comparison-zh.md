---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: KV 与 Cubbyhole 机密引擎对比
translated: true
type: note
---

HashiCorp Vault 中 KV (Key-Value) 和 Cubbyhole secrets engines 之间的主要区别如下：

## Scope and Access

**KV Engine**：共享存储，多个 tokens/users 可以根据 ACL policies 进行访问。如果你拥有正确的权限，你可以读取他人写入的 secrets。

**Cubbyhole**：私有的、基于 token-scoped 的存储。每个 token 都有自己隔离的 cubbyhole，只有该特定 token 能够访问——即使是 root token 也无法读取另一个 token 的 cubbyhole。

## Lifecycle

**KV Engine**：Secrets 的持久化独立于 tokens。无论 token 的生命周期如何，它们都会保留在 Vault 中，直到被显式删除。

**Cubbyhole**：与 token 的生命周期绑定。当 token 过期或被 revoked 时，其 cubbyhole 中的所有数据都会被自动销毁。

## Use Cases

**KV Engine**：用于应用程序的通用 secret 存储、共享 credentials、configuration data，以及需要被多个实体访问的 secrets。

**Cubbyhole**：临时 secret 存储、response wrapping（为安全传递而包装 secrets）、进程间的安全 secret handoff，以及存储不应超过特定 session 寿命的 ephemeral data。

## Versioning

**KV Engine**：有两个版本——KV v1（无 versioning）和 KV v2（支持 versioning、soft deletes 和可配置的 retention）。

**Cubbyhole**：没有 versioning 能力——它始终是一个简单的 key-value store。

## Example Scenario

如果你使用 response wrapping 安全地将 database password 传递给应用程序，Vault 会创建一个 single-use token 并将 wrapped secret 存储在该 token 的 cubbyhole 中。一旦应用程序检索到它，token 就会耗尽，cubbyhole 数据也会随之消失——这对于安全的一次性 secret 传递非常完美。
