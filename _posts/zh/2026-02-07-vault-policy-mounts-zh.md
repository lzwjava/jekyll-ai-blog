---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault 策略与挂载指南
translated: true
type: note
---

我将协助解释 Vault policy 和 `sys/mounts` 路径。

## Vault Policy

在 HashiCorp Vault 中，**policy** 是一组规则，用于定义用户或应用程序可以在 Vault 内的特定路径上执行哪些操作。Policy 使用 HashiCorp Configuration Language (HCL) 或 JSON 编写，并遵循 deny-by-default 模型——如果某项操作未被明确允许，则会被拒绝。

一个基础的 policy 如下所示：

```hcl
path "secret/data/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "sys/mounts" {
  capabilities = ["read"]
}
```

你可以授予的主要 capabilities 包括：
- `create` - 创建新数据
- `read` - 读取现有数据
- `update` - 修改现有数据
- `delete` - 删除数据
- `list` - 列出 keys/paths
- `sudo` - 允许访问受 root 保护的路径
- `deny` - 明确拒绝访问（优先级最高）

## The `sys/mounts` Path

`sys/mounts` 是 Vault 中的一个 **system backend path**，负责管理 secrets engines。具体而言：

- **作用**：该路径允许你查看、enable、disable 以及配置 Vault 中的 secrets engines (mount points)
- **重要性**：Secrets engines 是存储、生成或加密数据的组件。每种类型（如 KV, PKI, AWS, database）都会被 mount 在特定路径下

**在 `sys/mounts` 上的常见操作：**
- 在 `sys/mounts` 上执行 `read` - 列出所有已启用的 secrets engines
- 在 `sys/mounts/*` 上执行 `create`/`update` - enable 新的 secrets engines
- 在 `sys/mounts/*` 上执行 `delete` - disable secrets engines

例如，授予 read 权限允许用户查看已 mount 的 secrets engines，而 create/delete 权限则允许他们修改 Vault 的配置——这通常需要 admin 权限。
