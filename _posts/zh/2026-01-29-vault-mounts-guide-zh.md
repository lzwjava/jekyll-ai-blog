---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 简单详解库位上架方式
translated: true
type: note
---

我将为您解释 HashiCorp Vault mounts，这是组织 secrets 和 authentication method 的基本概念。

## 什么是 Mount？

在 Vault 中，**mount** 就像文件系统挂载点一样——它是您附加 secrets engine 或 authentication method 的路径。您可以将其想象为将不同的模块插入到 Vault API 路径结构的特定位置。

当您启用 secrets engine 或 auth method 时，您正在将其“挂载”到特定路径。该 engine 的所有操作随后都在该路径下进行。

## Mount 结构

Vault 的路径结构如下：

```
<mount_path>/<operation>
```

例如：
- `secret/data/myapp` - `secret/` 是 KV v2 engine 的挂载点
- `aws/creds/my-role` - `aws/` 是 AWS secrets engine 的挂载点
- `database/creds/my-role` - `database/` 是挂载点

## 什么是 sys/mount？

`sys/mount` 是一个特殊的 **system backend** 路径，用于管理 secrets engine mounts。它是 Vault 的 system backend（以 `sys/` 开头的路径）的一部分，负责处理 Vault 的配置和管理。

**关键操作：**

**列出所有 mounts：**

```bash
vault secrets list
# 或者通过 API
curl -H "X-Vault-Token: $TOKEN" $VAULT_ADDR/v1/sys/mounts
```

**启用新的 secrets engine：**

```bash
vault secrets enable -path=myapp kv
# 或者通过 API
curl -H "X-Vault-Token: $TOKEN" \
  -X POST \
  -d '{"type":"kv","options":{"version":"2"}}' \
  $VAULT_ADDR/v1/sys/mounts/myapp
```

**禁用/卸载：**

```bash
vault secrets disable myapp
# 或者通过 API
curl -H "X-Vault-Token: $TOKEN" \
  -X DELETE \
  $VAULT_ADDR/v1/sys/mounts/myapp
```

## Mount 的类型

**Secrets Engine Mounts** (`sys/mounts`):
- Dynamic secrets: AWS, database, SSH
- Static secrets: KV (key-value)
- Encryption as a service: Transit
- PKI: Certificate management

**Auth Method Mounts** (`sys/auth`):
- 概念类似，但用于身份验证
- 示例：userpass, LDAP, Kubernetes, AppRole

## 示例

当您启用 AWS secrets engine 时：

```bash
vault secrets enable -path=aws aws
```

您已在 `aws/` 创建了一个 mount。现在您可以：
- 配置它：`vault write aws/config/root ...`
- 创建 roles：`vault write aws/roles/my-role ...`
- 生成 credentials：`vault read aws/creds/my-role`

每种 secrets engine 类型都有自己的 API endpoints 和操作，但它们都通过这个 mount 系统工作。

这是否有助于澄清 mounts 的工作原理？如果您希望我更详细地解释任何特定方面，请告诉我！