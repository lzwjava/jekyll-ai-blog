---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Cloud Foundry 中的 CredHub 使用方法
translated: true
type: note
---

Question: 如何在 Cloud Foundry 中使用 CredHub？

Answer:

**CredHub** 是许多 Cloud Foundry 部署（特别是 Tanzu Application Service / VMware Tanzu Platform, PAS, PCF）中的集中化 secrets management 组件。它安全地存储和管理 credentials，例如 passwords, certificates, keys, JSON blobs 等。

开发者与 CredHub 交互主要有两种方式：

1. **间接方式 (推荐大多数应用使用)** — 通过 CredHub Service Broker（创建/绑定 service instances，通过 `VCAP_SERVICES` 向应用交付 secrets，而不会在 `cf env` 中泄露它们）。
2. **直接方式** — 使用 CredHub CLI 或 API（适用于管理员、自动化或高级用例）。

### 1. 通过 Service Broker 使用 CredHub (最常用的应用程序方案)

在安装了 **CredHub Service Broker** 的环境中（在 Tanzu Application Service 中很常见），请按照以下步骤操作：

- 列出可用服务（查找类似 `credhub`, `credhub-secrets` 或类似的服务）：

  ```bash
  cf marketplace
  ```

- 创建一个 CredHub service instance：

  ```bash
  # 示例：创建一个简单的 value secret
  cf create-service credhub default my-secret-service \
    -c '{"type":"value", "name":"/my-org/my-app/api-key", "value":"sk_live_xyz123"}'

  # 或者自动生成一个 password
  cf create-service credhub default my-db-password \
    -c '{"type":"password", "name":"/my-org/my-app/db-pass", "length":32}'
  ```

  常见的 credential 类型：`value`, `password`, `certificate`, `rsa`, `ssh`, `user`, `json`。

- 将服务绑定到你的应用：

  ```bash
  cf bind-service my-app my-secret-service
  cf restage my-app
  ```

- 在你的应用程序中，从 `VCAP_SERVICES` 读取（credentials 出现在类似 user-provided 的结构下，但由 CredHub 支持）：

  ```json
  {
    "credhub": [
      {
        "name": "my-secret-service",
        "credentials": {
          "credential": "/my-org/my-app/api-key",
          "version": "..."
        }
      }
    ]
  }
  ```

  许多现代 buildpacks / libraries 会在运行时使用 instance credentials（来自 `/etc/cf-instance-credentials/` 的 mTLS cert/key）自动从 CredHub 插值 (interpolate) 真实值。

  **注意：** 在某些设置中，你只能在 `VCAP_SERVICES` 中看到引用（`/path/to/secret`）。应用容器会通过平台自动进行 CredHub 插值。

### 2. 使用 CredHub CLI (直接访问 – 管理 / 调试 / 脚本)

安装 CredHub CLI：

```bash
# macOS (Homebrew)
brew install cloudfoundry/tap/credhub-cli

# 或从 https://github.com/cloudfoundry-incubator/credhub-cli/releases 下载二进制文件
```

身份验证（指向你的 CredHub 实例）：

```bash
# 通常由你的平台团队提供（通常与 cf login 的 UAA 相同）
credhub login --client-id <uaa-client-id> --client-secret <uaa-client-secret>
# 或者使用 cf oauth-token 作为 bearer
credhub api https://credhub.service.cf.internal:8844   # 内部 URL (从 CF 内部访问)
credhub login --token "$(cf oauth-token | cut -d' ' -f2)"
```

常用命令：

```bash
# 设置一个简单的 value
credhub set -n /my-org/my-app/api-key -t value -v "sk_live_xyz123"

# 生成一个随机 password
credhub generate -n /my-org/my-app/db-pass -t password -l 32

# 生成一个 certificate
credhub generate -n /my-org/my-app/cert -t certificate \
  --common-name myapp.example.com --alternative-names "*.example.com"

# 获取一个 credential
credhub get -n /my-org/my-app/api-key

# 查找 credentials
credhub find -p /my-org/my-app/

# 删除
credhub delete -n /my-org/my-app/old-key
```

### 快速比较：User-Provided vs CredHub

| 特性 | User-Provided Service (`cf cups`) | CredHub (通过 Broker 或直接访问) |
| -------------------------- | ------------------------------------ | -------------------------------- |
| 在 `cf env` 中的可见性 | 已遮蔽 (大部分) | 仅显示引用或已插值 |
| Rotation 支持 | 手动 | 内置 regeneration |
| 中央审计 (Central auditing) | 否 | 是 |
| 生成能力 (passwords, certs) | 否 | 是 |
| 最适用于 | 简单的非企业级设置 | 企业级、合规性要求 |

咨询你的平台运维人员：

- 你的 marketplace 中是否有 CredHub Service Broker 可用？
- 正确的 service offering 名称是什么？
- 直接使用 CLI 访问需要哪些 UAA client credentials 或 mTLS 设置？

参考资料：

- [CredHub Documentation – Cloud Foundry Docs](https://docs.cloudfoundry.org/credhub/index.html)
- [Use CredHub Secrets Management – Broadcom Techdocs](https://techdocs.broadcom.com/us/en/vmware-tanzu/platform/credhub-secrets-management/services/credhub/using.html)
- [CredHub CLI Releases](https://github.com/cloudfoundry-incubator/credhub-cli/releases)
- [CredHub API Reference](https://docs.cloudfoundry.org/api/credhub)
