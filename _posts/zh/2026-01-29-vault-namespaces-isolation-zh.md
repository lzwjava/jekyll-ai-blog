---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 用于租户隔离的 Vault 命名空间
translated: true
type: note
---

Vault 中的 Namespaces 是一种在单个 Vault cluster 中创建隔离环境的方法。可以将它们视为独立的“租户”或分区，为不同的团队、applications 或业务部门提供逻辑隔离。

## Key Concepts

**Isolation**：每个 namespace 都有自己的一套 policies、secrets engines、auth methods 和 entities。一个 namespace 中发生的事情与其它 namespace 完全隔离。

**Hierarchical structure**：Namespaces 可以嵌套，创建父子关系。例如，你可以将 `engineering/` 作为父级 namespace，将 `engineering/app1/` 和 `engineering/app2/` 作为子级。

**Root namespace**：默认情况下，Vault 中的所有内容都存在于 root namespace 中。当你创建新的 namespaces 时，它们会从 root 分离出来。

## Common Use Cases

Namespaces 对于多租户环境特别有用，在这种环境中，你希望为团队或客户提供各自隔离的 Vault 环境，而无需运行多个 clusters。例如，服务提供商可能会为每个客户创建一个 namespace，或者企业可能会为不同的部门创建 namespaces。

## Basic Operations

你可以使用 `-namespace` 标志或 `VAULT_NAMESPACE` 环境变量与 namespaces 进行交互：

```bash
# Create a namespace
vault namespace create engineering

# List namespaces
vault namespace list

# Use a namespace for commands
vault secrets list -namespace=engineering
```

在嵌套的 namespaces 中工作时，需要使用完整路径，如 `engineering/app1`。

**Note**：Namespaces 是 Vault Enterprise 的功能，在开源版本中不可用。

关于 namespaces，你是否还有想进一步探索的特定方面，例如 access control、delegation 或实际的 implementation patterns？
