---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Integrating HashiCorp Vault with Terraform
translated: false
type: note
---

**Question:** How does HashiCorp Vault relate to tfvars? How to let Terraform work with HashiCorp Vault together?

**Answer:**

HashiCorp Vault and Terraform `.tfvars` files serve similar purposes (providing input values to Terraform configurations), but they differ significantly in **security**, **lifecycle**, and **management**.

### Relationship between HashiCorp Vault and tfvars

- **terraform.tfvars / *.auto.tfvars / custom.tfvars**
  These are plain-text (or occasionally JSON) files that supply values to Terraform variables.
  - Very convenient for development and small teams.
  - Very **dangerous** for production secrets — they are easily committed to git, leaked in CI logs, or stored insecurely.
  - Even when `.tfvars` is gitignored and passed via CI, long-lived secrets remain a risk.

- **HashiCorp Vault**
  A dedicated secrets management system offering:
  - Centralized storage + strong access control (policies, auth methods)
  - **Dynamic secrets** (short-lived credentials that auto-expire)
  - Automatic rotation & leasing
  - Audit logging
  - Versioning of secrets (in some engines)

**Summary comparison**
| Aspect              | .tfvars files                          | HashiCorp Vault                              | Recommendation          |
|---------------------|----------------------------------------|----------------------------------------------|--------------------------|
| Security            | Low–Medium (depends on handling)       | High (enterprise-grade)                      | Vault for prod secrets  |
| Dynamic / expiring  | Static                                 | Yes (very strong feature)                    | Vault                   |
| Audit trail         | None                                   | Excellent                                    | Vault                   |
| Rotation automation | Manual                                 | Built-in                                     | Vault                   |
| Ease for dev        | Very easy                              | Requires setup + auth                        | tfvars for local dev    |
| Git safety          | Risky (even gitignored)                | Never stored in repo                         | Vault                   |

Best practice in 2025–2026:
Use `.tfvars` → only for **non-sensitive** or **local development** values.
Use **Vault** → for all real secrets in CI/CD pipelines and production.

### How to integrate Terraform with HashiCorp Vault

There are two main patterns (often used together):

1. **Read secrets from Vault into Terraform variables / resources** (most common)

```hcl
# Configure the Vault provider
provider "vault" {
  address = "https://vault.example.com:8200"
  # Several auth methods possible — token is simplest for demos
  token = var.vault_token   # NEVER hard-code; use env var or secure injection
}

# Read a static secret (kv v2 engine)
data "vault_generic_secret" "db_creds" {
  path = "secret/data/prod/database"
}

# Use the secret (mark output sensitive!)
resource "aws_db_instance" "example" {
  ...
  password = data.vault_generic_secret.db_creds.data["password"]
  ...
}

# Or pass to variable (if needed in many places)
variable "db_password" {
  sensitive = true
}

locals {
  actual_db_password = data.vault_generic_secret.db_creds.data["password"]
}
```

2. **Use Vault to generate dynamic, short-lived credentials for Terraform providers** (very secure — recommended for AWS/Azure/GCP)

Example — dynamic AWS credentials:

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

Vault creates temporary IAM credentials only for the duration of the `terraform apply`, then they expire automatically.

### Quick setup steps (2025/2026 style)

1. Run Vault (dev mode for testing): `vault server -dev`
2. Enable a secrets engine: `vault secrets enable -path=secret kv-v2`
3. Write a secret: `vault kv put secret/prod/database password=supersecret`
4. Create policy & token/role for Terraform
5. In CI/CD (GitHub Actions, GitLab CI, etc.):
   - Authenticate to Vault (AppRole, JWT, OIDC, etc.)
   - Inject Vault token or use short-lived token
   - Run `terraform apply`

Many teams now prefer **Vault + Terraform Cloud/Enterprise dynamic provider credentials** (Vault generates credentials automatically per run — no token needed in workspace).

**Never** put real secrets in `.tfvars` files checked into version control or long-lived in CI variables. Vault is currently (2026) one of the strongest and most Terraform-native solutions for secrets.

**References:**

- [Vault Provider - Terraform Registry](https://registry.terraform.io/providers/hashicorp/vault/latest/docs)
- [Inject secrets into Terraform using the Vault provider](https://developer.hashicorp.com/terraform/tutorials/secrets/secrets-vault)
- [Integrate Terraform with Vault](https://developer.hashicorp.com/validated-patterns/terraform/terraform-integrate-vault)
- [Terraform security: 5 foundational practices](https://www.hashicorp.com/en/blog/terraform-security-5-foundational-practices)
