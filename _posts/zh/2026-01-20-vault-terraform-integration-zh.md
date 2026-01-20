---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 将 HashiCorp Vault 与 Terraform 集成
translated: true
type: note
---

**Question:** HashiCorp Vault 与 tfvars 之间有什么关系？如何让 Terraform 与 HashiCorp Vault 配合工作？

**Answer:**

HashiCorp Vault 和 Terraform `.tfvars` 文件用途相似（都为 Terraform 配置提供输入值），但在 **Security**、**Lifecycle** 和 **Management** 方面有显著差异。

### HashiCorp Vault 与 tfvars 的关系

- **terraform.tfvars / *.auto.tfvars / custom.tfvars**
  这些是纯文本（或偶尔是 JSON）文件，用于为 Terraform variables 提供值。
  - 对于开发环境和小团队非常方便。
  - 对于生产环境的 secrets 非常 **dangerous** —— 它们很容易被提交到 Git、在 CI logs 中泄露或以不安全的方式存储。
  - 即使 `.tfvars` 被列入 gitignore 并通过 CI 传递，长期存在的 secrets 仍然是一个风险。

- **HashiCorp Vault**
  一个专门的 secrets management 系统，提供：
  - 集中化存储 + 强大的 access control (policies, auth methods)
  - **Dynamic secrets**（自动过期的短期凭证）
  - 自动 rotation (轮转) 和 leasing (租约)
  - Audit logging (审计日志)
  - Secrets 的版本控制（在某些 engines 中）

**对比总结**

| 维度 | .tfvars 文件 | HashiCorp Vault | 建议 |
|---------------------|----------------------------------------|----------------------------------------------|--------------------------|
| Security | 低–中（取决于处理方式） | 高（企业级） | 生产 secrets 使用 Vault |
| Dynamic / expiring | Static | 是（非常强大的功能） | Vault |
| Audit trail | 无 | 优秀 | Vault |
| Rotation automation | 手动 | 内置 | Vault |
| Ease for dev | 非常简单 | 需要 setup + auth | 本地开发使用 tfvars |
| Git safety | 有风险（即使被 gitignore） | 从不存储在 repo 中 | Vault |

2025–2026 年的最佳实践：
使用 `.tfvars` → 仅用于 **non-sensitive**（非敏感）或 **local development**（本地开发）的值。
使用 **Vault** → 用于 CI/CD pipelines 和生产环境中所有的真实 secrets。

### 如何将 Terraform 与 HashiCorp Vault 集成

主要有两种模式（通常结合使用）：

1. **从 Vault 读取 secrets 到 Terraform variables / resources 中**（最常见）

```hcl
# Configure the Vault provider
provider "vault" {
  address = "https://vault.example.com:8200"
  # 可以使用多种 auth methods —— token 对 demo 来说最简单
  token = var.vault_token   # 绝不要硬编码；使用环境变量或安全注入
}

# 读取一个 static secret (kv v2 engine)
data "vault_generic_secret" "db_creds" {
  path = "secret/data/prod/database"
}

# 使用 secret (记得将 output 标记为 sensitive!)
resource "aws_db_instance" "example" {
  ...
  password = data.vault_generic_secret.db_creds.data["password"]
  ...
}

# 或者传递给 variable (如果多处需要)
variable "db_password" {
  sensitive = true
}

locals {
  actual_db_password = data.vault_generic_secret.db_creds.data["password"]
}
```

2. **使用 Vault 为 Terraform providers 生成动态、短期的凭证**（非常安全 —— 推荐用于 AWS/Azure/GCP）

示例 —— 动态 AWS 凭证：

```hcl
data "vault_aws_access_credentials" "creds" {
  backend = "aws"
  role    = "terraform-role"
}

provider "aws" {
  access_key = data.vault_aws_access_credentials.creds.access_key
  secret_key = data.vault_aws_access_credentials.creds.secret_key
  token      = data.vault_aws_access_credentials.creds.security_token
}
```

Vault 仅在 `terraform apply` 期间创建临时 IAM 凭证，之后它们会自动过期。

### 快速设置步骤 (2025/2026 风格)

1. 运行 Vault（测试用 dev 模式）：`vault server -dev`
2. 启用 secrets engine：`vault secrets enable -path=secret kv-v2`
3. 写入一个 secret：`vault kv put secret/prod/database password=supersecret`
4. 为 Terraform 创建 policy 和 token/role
5. 在 CI/CD（GitHub Actions, GitLab CI 等）中：
   - 认证到 Vault (AppRole, JWT, OIDC 等)
   - 注入 Vault token 或使用短期 token
   - 运行 `terraform apply`

许多团队现在更倾向于 **Vault + Terraform Cloud/Enterprise dynamic provider credentials**（Vault 为每次运行自动生成凭证 —— workspace 中不需要存储 token）。

**永远不要**将真实的 secrets 放入签入版本控制的 `.tfvars` 文件中，或长期存储在 CI 变量中。Vault 是目前（2026年）最强大且对 Terraform 最原生的 secrets 解决方案之一。

**References:**

- [Vault Provider - Terraform Registry](https://registry.terraform.io/providers/hashicorp/vault/latest/docs)
- [Inject secrets into Terraform using the Vault provider](https://developer.hashicorp.com/terraform/tutorials/secrets/secrets-vault)
- [Integrate Terraform with Vault](https://developer.hashicorp.com/validated-patterns/terraform/terraform-integrate-vault)
- [Terraform security: 5 foundational practices](https://www.hashicorp.com/en/blog/terraform-security-5-foundational-practices)