---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: HashiCorp Vault 全面指南
translated: true
type: note
---

**Question:** 提供一份关于使用 HashiCorp Vault 的全面指南？

**Answer:**

这里有一份针对 **HashiCorp Vault** 的实用且最新的（2025–2026 时代）全面使用指南。

### 1. Vault 解决了哪些问题？

- 存储和分发 **secrets**（密码、API keys、证书、Encryption keys、Tokens）
- **Dynamic secrets** —— 根据需求按需创建并自动撤销的凭据
- **Short-lived credentials** —— 2025 年强烈推荐的安全模型
- **集中式访问控制 + Audit logging**
- **Encryption as a service**（加密即服务）
- **Identity-based security**（代码/CI 中不再有长期存在的静态凭据）

### 2. 核心概念 —— 必须掌握

| 概念 | 2025–2026 Vault 中的含义 |
| :--- | :--- |
| Secret Engine | 了解如何生成/存储/撤销 secrets 的插件 (kv, database, aws, pki, …) |
| Mount path | Engine “居住”的路径 (`secret/`, `database/`, `pki/int-ca/`, …) |
| Auth Method | 用户/机器如何进行身份验证 (jwt, kubernetes, approle, userpass, oidc, …) |
| Policy | 使用 HCL 编写的 ACL —— 粒度非常细 (`path "secret/data/prod/*" { capabilities = ["read"] }`) |
| Token | 身份验证的主要方式（可以是 short-lived, periodic, orphan 等） |
| Identity | Vault 内部的 Entity + Aliases，将多种 Auth Method 链接到一个身份 |
| Lease | Dynamic secrets 的 TTL + 可续约合同 |

### 3. 快速上手 (Dev Mode – 2025 风格)

```bash
# 以开发模式运行（不安全 —— 仅用于学习）
vault server -dev -dev-root-token-id=root

# 或开启 UI 并禁用 TLS（2026 年本地开发中仍然常用）
vault server -dev -dev-root-token-id=root -dev-listen-address="0.0.0.0:8200"

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN=root
```

打开浏览器 → <http://127.0.0.1:8200/ui>

### 4. 最常见的 Secret Engines (2025–2026 排名)

| Engine | 现在的用例 | Dynamic? | Revocable? | 推荐的 Mount path |
| :--- | :--- | :--- | :--- | :--- |
| kv-v2 | 静态应用 secrets, config | No | No | `secret/` |
| database | MySQL/PostgreSQL/Redis/… 临时账号 | Yes | Yes | `database/` |
| aws | AWS IAM 凭据 (access key / session) | Yes | Yes | `aws/` |
| pki | 内部和公网 TLS 证书 | Yes | Yes | `pki/` 或 `pki/int/` |
| transit | 加密 / 签名即服务 | — | — | `transit/` |
| ssh | SSH 客户端 & OTP / 签名证书 | Yes | Yes | `ssh-client` / `ssh-host` |
| kubernetes | Kubernetes service account JWT 验证 | — | — | (auth method, not engine) |
| jwt / oidc | GitHub Actions, GitLab CI, workload identity | — | — | (auth method) |

### 5. 典型的 2025–2026 生产架构

1. **Vault cluster** —— 3 或 5 个节点 (Raft storage)
2. **Auto-unseal** —— AWS KMS / GCP KMS / Azure Key Vault / Transit
3. **External storage** —— 集成 Raft (最常用), Consul, etcd
4. **TLS everywhere** —— 强制要求
5. **Separate PKI mount** —— 用于中间 CA (Intermediate CA)
6. **Multiple KV mounts** —— `apps/team-a/`, `infra/prod/`, `ci/`
7. **AppRole** 或 **JWT/OIDC** —— 用于大多数工作负载
8. **Kubernetes auth** + **Vault Agent Injector** / **CSI driver**

### 6. 分步指南 – 现实的现代工作流 (Kubernetes + AppRole + KV + Database)

{% raw %}

```bash
# 1. 启用 engines
vault secrets enable -path=apps kv-v2
vault secrets enable -path=database database

# 2. 配置 PostgreSQL engine (示例)
vault write database/config/my-pg \
    plugin_name=postgresql-database-plugin \
    allowed_roles="myapp" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/myapp" \
    username="vault_admin" \
    password="super-secret-admin-pass"

vault write database/roles/myapp \
    db_name=my-pg \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# 3. 为应用程序创建 policy
cat > myapp-policy.hcl <<EOF
path "apps/data/myapp/*" {
  capabilities = ["read", "list"]
}
path "apps/metadata/myapp/*" {
  capabilities = ["list"]
}
path "database/creds/myapp" {
  capabilities = ["read"]
}
EOF

vault policy write myapp myapp-policy.hcl

# 4. 创建 AppRole + 绑定 policy
vault auth enable approle
vault write auth/approle/role/myapp \
    token_policies="myapp" \
    token_ttl=20m \
    token_max_ttl=60m \
    secret_id_ttl=30m

# 获取 RoleID & SecretID
vault read auth/approle/role/myapp/role-id
vault write -f auth/approle/role/myapp/secret-id
```

{% endraw %}

### 7. 2025–2026 最佳实践

- **切勿**提交 `VAULT_TOKEN` 或 `VAULT_ROLE_ID`/`SECRET_ID` 键值对
- 在 Kubernetes 中使用 **Vault Agent** 或 **Vault CSI Provider**
- 为动态凭证优先使用 **Short TTL**（分钟 → 小时）
- **轮转 Root token** 并创建 **Recovery keys**
- 针对大型组织使用 **Namespaces**
- 启用 **Audit logging** → 全部发送至 SIEM
- 针对非常敏感的初始 secret 分发使用 **Response-wrapping**
- 优先选择 **Identity-based** 安全，而非 IP 白名单

### 8. 常用客户端模式 (2025)

| 语言 / 工具 | 推荐的库 / 方法 | 2026 年的状态 |
| :--- | :--- | :--- |
| Go | 官方 hashicorp/vault/api | 非常好 |
| Python | hvac | 非常流行 |
| Java | spring-vault / 官方 Java 客户端 | 好 |
| Node.js | node-vault | 好 |
| .NET | VaultSharp | 好 |
| Terraform | 内置 provider + remote state backend | 标准做法 |
| Kubernetes | Vault Agent Injector / CSI secrets store | 主流 |
| GitHub Actions | hashicorp/vault-action (JWT auth) | 非常流行 |

### 9. 常用故障排查命令

```bash
vault status                  # 是否已初始化？是否处于 sealed 状态？
vault operator raft list-peers
vault token lookup -accessor $ACCESSOR
vault lease lookup database/creds/myapp/abc123
vault audit list
vault path-help aws/creds/my-role
```

**参考文献：**

- <https://developer.hashicorp.com/vault/docs>
- <https://developer.hashicorp.com/vault/tutorials>
- <https://developer.hashicorp.com/vault/docs/concepts>
- <https://developer.hashicorp.com/vault/docs/secret-engines>
- <https://developer.hashicorp.com/vault/docs/auth>_
