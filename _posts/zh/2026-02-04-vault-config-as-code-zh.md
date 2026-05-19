---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault 配置代码化指南
translated: true
type: note
---

我将详细介绍可以作为 GitHub 代码管理的 Vault 配置选项，涵盖 policies、mounts、auth methods 以及各种 engine 配置。

## 完整的 Vault Configuration as Code 结构

```
vault-config/
├── policies/
│   ├── terraform-secrets.hcl
│   ├── jenkins-auth.hcl
│   └── admin.hcl
├── terraform/
│   ├── main.tf
│   ├── auth-methods.tf
│   ├── secret-engines.tf
│   ├── policies.tf
│   ├── roles.tf
│   └── secrets.tf
└── scripts/
    └── apply-config.sh
```

## 1. 扩展 Policy 配置

```hcl
# policies/terraform-secrets.hcl

# 对 KV v2 中 Terraform secrets 的读取权限
path "secret/data/terraform/*" {
  capabilities = ["read", "list"]
}

# 列出 terraform secret 路径
path "secret/metadata/terraform/*" {
  capabilities = ["list"]
}

# 读取特定的 terraform 环境
path "secret/data/terraform/prod/*" {
  capabilities = ["read"]
}

path "secret/data/terraform/staging/*" {
  capabilities = ["read"]
}

path "secret/data/terraform/dev/*" {
  capabilities = ["read", "list"]
}

# 访问 database credentials engine
path "database/creds/terraform-role" {
  capabilities = ["read"]
}

# 访问 AWS dynamic credentials
path "aws/creds/terraform-role" {
  capabilities = ["read"]
}

# 访问用于证书的 PKI
path "pki/issue/terraform-cert" {
  capabilities = ["create", "update"]
}

# 读取 transit encryption keys
path "transit/encrypt/terraform-key" {
  capabilities = ["update"]
}

path "transit/decrypt/terraform-key" {
  capabilities = ["update"]
}

# 拒绝访问特定路径
path "secret/data/terraform/prod/root-password" {
  capabilities = ["deny"]
}
```

## 2. 综合 Terraform 配置

### Main 配置
```hcl
# terraform/main.tf

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 3.20"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-vault-config"
    key    = "vault/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "vault" {
  address = var.vault_address
  token   = var.vault_token  # 在生产环境中使用适当的身份验证方式
}

variable "vault_address" {
  description = "Vault server address"
  type        = string
  default     = "https://vault.company.com"
}

variable "vault_token" {
  description = "Vault authentication token"
  type        = string
  sensitive   = true
}
```

### Secret Engines 配置
{% raw %}
```hcl
# terraform/secret-engines.tf

# 用于 Terraform 变量的 KV v2 Secrets Engine
resource "vault_mount" "terraform_secrets" {
  path        = "secret"
  type        = "kv-v2"
  description = "KV v2 secrets engine for Terraform variables"
  
  options = {
    version = "2"
    max_versions = "10"
    cas_required = "false"
    delete_version_after = "0"
  }
}

# 用于应用程序机密的附加 KV v2
resource "vault_mount" "app_secrets" {
  path        = "apps"
  type        = "kv-v2"
  description = "Application-specific secrets"
  
  options = {
    version = "2"
    max_versions = "5"
  }
}

# Database Secrets Engine
resource "vault_mount" "database" {
  path        = "database"
  type        = "database"
  description = "Dynamic database credentials"
  
  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 86400
}

# Database 连接配置
resource "vault_database_secret_backend_connection" "postgres" {
  backend       = vault_mount.database.path
  name          = "postgres-prod"
  allowed_roles = ["terraform-role", "app-role"]

  postgresql {
    connection_url = "postgresql://{{username}}:{{password}}@postgres.company.com:5432/mydb"
    username       = "vault-admin"
    password       = var.db_admin_password
    
    max_open_connections      = 5
    max_idle_connections      = 2
    max_connection_lifetime   = 300
  }
}

# 用于 Terraform 的 Database role
resource "vault_database_secret_backend_role" "terraform_db_role" {
  backend             = vault_mount.database.path
  name                = "terraform-role"
  db_name             = vault_database_secret_backend_connection.postgres.name
  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
  ]
  
  default_ttl = 3600
  max_ttl     = 86400
}

# AWS Secrets Engine
resource "vault_aws_secret_backend" "aws" {
  path        = "aws"
  description = "AWS dynamic credentials"
  
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = "us-east-1"
  
  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 43200
}

# 用于 Terraform 的 AWS role
resource "vault_aws_secret_backend_role" "terraform_aws_role" {
  backend         = vault_aws_secret_backend.aws.path
  name            = "terraform-role"
  credential_type = "iam_user"
  
  policy_document = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:*",
          "s3:*",
          "rds:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# PKI Secrets Engine (用于证书)
resource "vault_mount" "pki" {
  path                      = "pki"
  type                      = "pki"
  description               = "PKI secrets engine"
  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 87600  # 10 years
}

# 配置 PKI
resource "vault_pki_secret_backend_root_cert" "root" {
  backend              = vault_mount.pki.path
  type                 = "internal"
  common_name          = "company.com"
  ttl                  = "87600h"
  format               = "pem"
  private_key_format   = "der"
  key_type            = "rsa"
  key_bits            = 4096
  exclude_cn_from_sans = true
  ou                   = "Engineering"
  organization         = "Company Inc"
}

# 供 Terraform 管理的证书的 PKI role
resource "vault_pki_secret_backend_role" "terraform_cert" {
  backend          = vault_mount.pki.path
  name             = "terraform-cert"
  ttl              = 86400
  max_ttl          = 259200
  allow_ip_sans    = true
  key_type         = "rsa"
  key_bits         = 2048
  allowed_domains  = ["company.com", "dev.company.com"]
  allow_subdomains = true
  allow_any_name   = false
}

# Transit Secrets Engine (加密即服务)
resource "vault_mount" "transit" {
  path        = "transit"
  type        = "transit"
  description = "Encryption as a service"
}

# Transit 加密密钥
resource "vault_transit_secret_backend_key" "terraform_key" {
  backend          = vault_mount.transit.path
  name             = "terraform-key"
  type             = "aes256-gcm96"
  deletion_allowed = false
  
  # 密钥轮转
  auto_rotate_period = 2592000  # 30 days
}

# SSH Secrets Engine
resource "vault_mount" "ssh" {
  path        = "ssh"
  type        = "ssh"
  description = "SSH certificate authority"
}

# SSH CA role
resource "vault_ssh_secret_backend_ca" "ssh_ca" {
  backend              = vault_mount.ssh.path
  generate_signing_key = true
}

resource "vault_ssh_secret_backend_role" "ssh_role" {
  backend                 = vault_mount.ssh.path
  name                    = "terraform-ssh"
  key_type                = "ca"
  allow_user_certificates = true
  allowed_users           = "*"
  default_extensions = {
    permit-pty = ""
  }
  ttl     = "3600"
  max_ttl = "86400"
}

# TOTP Secrets Engine (用于 MFA)
resource "vault_mount" "totp" {
  path        = "totp"
  type        = "totp"
  description = "TOTP MFA tokens"
}
```
{% endraw %}

### Auth Methods 配置
{% raw %}
```hcl
# terraform/auth-methods.tf

# Jenkins 的 JWT Auth Method
resource "vault_jwt_auth_backend" "jenkins" {
  path               = "jwt-jenkins"
  type               = "jwt"
  description        = "JWT authentication for Jenkins"
  
  jwks_url           = "https://jenkins.company.com/jwtauth/jwks"
  bound_issuer       = "https://jenkins.company.com"
  default_role       = "jenkins-default"
  
  tune {
    default_lease_ttl  = "1h"
    max_lease_ttl      = "24h"
    token_type         = "default-service"
    listing_visibility = "unauth"
  }
}

# Jenkins Terraform 作业的 JWT role
resource "vault_jwt_auth_backend_role" "jenkins_terraform" {
  backend        = vault_jwt_auth_backend.jenkins.path
  role_name      = "jenkins-terraform"
  token_policies = ["terraform-secrets", "database-read", "aws-read"]
  
  role_type = "jwt"
  
  bound_claims = {
    jenkins_job_name = "terraform-*"
    jenkins_server   = "jenkins.company.com"
  }
  
  user_claim            = "sub"
  user_claim_json_pointer = false
  
  claim_mappings = {
    jenkins_job_name    = "job_name"
    jenkins_build_number = "build_number"
  }
  
  token_ttl             = 3600
  token_max_ttl         = 7200
  token_explicit_max_ttl = 0
  token_no_default_policy = false
  token_num_uses        = 0
  token_period          = 0
  token_type            = "default"
}

# GitHub Actions 的 OIDC Auth Method
resource "vault_jwt_auth_backend" "github_actions" {
  path        = "github"
  type        = "jwt"
  description = "GitHub Actions OIDC authentication"
  
  oidc_discovery_url = "https://token.actions.githubusercontent.com"
  bound_issuer       = "https://token.actions.githubusercontent.com"
  
  tune {
    default_lease_ttl = "1h"
    max_lease_ttl     = "12h"
  }
}

# GitHub Actions role
resource "vault_jwt_auth_backend_role" "github_terraform" {
  backend        = vault_jwt_auth_backend.github_actions.path
  role_name      = "github-terraform"
  token_policies = ["terraform-secrets"]
  
  role_type = "jwt"
  
  bound_audiences = ["https://github.com/yourorg"]
  
  bound_claims = {
    repository = "yourorg/terraform-infrastructure"
  }
  
  user_claim = "actor"
  
  claim_mappings = {
    repository = "repository"
    workflow   = "workflow"
  }
}

# AppRole Auth Method
resource "vault_auth_backend" "approle" {
  type = "approle"
  path = "approle"
  
  tune {
    default_lease_ttl = "1h"
    max_lease_ttl     = "24h"
  }
}

# 自动化服务的 AppRole
resource "vault_approle_auth_backend_role" "terraform_automation" {
  backend        = vault_auth_backend.approle.path
  role_name      = "terraform-automation"
  token_policies = ["terraform-secrets", "database-read"]
  
  secret_id_ttl          = 600
  secret_id_num_uses     = 10
  token_num_uses         = 0
  token_ttl              = 3600
  token_max_ttl          = 7200
  secret_id_bound_cidrs  = ["10.0.0.0/8"]
  token_bound_cidrs      = ["10.0.0.0/8"]
}

# Kubernetes Auth Method
resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
  path = "kubernetes"
}

resource "vault_kubernetes_auth_backend_config" "k8s_config" {
  backend            = vault_auth_backend.kubernetes.path
  kubernetes_host    = "https://kubernetes.company.com"
  kubernetes_ca_cert = file("${path.module}/ca.crt")
  token_reviewer_jwt = var.k8s_token_reviewer_jwt
}

resource "vault_kubernetes_auth_backend_role" "terraform_k8s" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = "terraform"
  bound_service_account_names      = ["terraform"]
  bound_service_account_namespaces = ["infrastructure"]
  token_policies                   = ["terraform-secrets"]
  token_ttl                        = 3600
}

# LDAP Auth Method
resource "vault_ldap_auth_backend" "ldap" {
  path        = "ldap"
  url         = "ldaps://ldap.company.com"
  userdn      = "ou=Users,dc=company,dc=com"
  groupdn     = "ou=Groups,dc=company,dc=com"
  groupfilter = "(&(objectClass=group)(member={{.UserDN}}))"
  binddn      = var.ldap_binddn
  bindpass    = var.ldap_bindpass
  
  token_ttl     = 3600
  token_max_ttl = 7200
}

# LDAP group 映射
resource "vault_ldap_auth_backend_group" "terraform_team" {
  backend  = vault_ldap_auth_backend.ldap.path
  groupname = "terraform-team"
  policies  = ["terraform-secrets", "database-read"]
}
```
{% endraw %}

### Policies 配置
```hcl
# terraform/policies.tf

# 导入 HCL policy 文件
resource "vault_policy" "terraform_secrets" {
  name   = "terraform-secrets"
  policy = file("${path.module}/../policies/terraform-secrets.hcl")
}

resource "vault_policy" "database_read" {
  name = "database-read"
  
  policy = <<EOT
# Read database credentials
path "database/creds/*" {
  capabilities = ["read"]
}

# List available database roles
path "database/roles" {
  capabilities = ["list"]
}
EOT
}

resource "vault_policy" "aws_read" {
  name = "aws-read"
  
  policy = <<EOT
# Generate AWS credentials
path "aws/creds/terraform-role" {
  capabilities = ["read"]
}

# Read AWS role configuration
path "aws/roles/terraform-role" {
  capabilities = ["read"]
}
EOT
}

resource "vault_policy" "admin" {
  name = "admin"
  
  policy = <<EOT
# Full access to all paths
path "*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
EOT
}

# PKI 操作的 Policy
resource "vault_policy" "pki_operations" {
  name = "pki-operations"
  
  policy = <<EOT
# Issue certificates
path "pki/issue/terraform-cert" {
  capabilities = ["create", "update"]
}

# Revoke certificates
path "pki/revoke" {
  capabilities = ["update"]
}

# List certificates
path "pki/certs" {
  capabilities = ["list"]
}
EOT
}
```

### Entity 和 Group 配置
```hcl
# terraform/entities.tf

# 为 service account 创建 entity
resource "vault_identity_entity" "terraform_service" {
  name     = "terraform-service"
  policies = ["terraform-secrets", "database-read"]
  
  metadata = {
    environment = "production"
    team        = "infrastructure"
  }
}

# JWT auth 的 Entity alias
resource "vault_identity_entity_alias" "terraform_jenkins" {
  name           = "terraform-pipeline"
  mount_accessor = vault_jwt_auth_backend.jenkins.accessor
  canonical_id   = vault_identity_entity.terraform_service.id
}

# 创建 identity group
resource "vault_identity_group" "terraform_users" {
  name     = "terraform-users"
  type     = "internal"
  policies = ["terraform-secrets"]
  
  metadata = {
    version = "1.0"
  }
}

# 将 entity 添加到 group
resource "vault_identity_group_member_entity_ids" "terraform_members" {
  group_id          = vault_identity_group.terraform_users.id
  member_entity_ids = [vault_identity_entity.terraform_service.id]
  exclusive         = false
}
```

### Namespace 配置 (Vault Enterprise)
```hcl
# terraform/namespaces.tf

resource "vault_namespace" "engineering" {
  path = "engineering"
}

resource "vault_namespace" "terraform" {
  namespace = vault_namespace.engineering.path
  path      = "terraform"
}

# 在 namespace 中挂载 secrets engine
resource "vault_mount" "terraform_ns_secrets" {
  namespace = "${vault_namespace.engineering.path}/${vault_namespace.terraform.path}"
  path      = "secrets"
  type      = "kv-v2"
}
```

### Audit 配置
```hcl
# terraform/audit.tf

# File audit 设备
resource "vault_audit" "file" {
  type = "file"
  
  options = {
    file_path = "/vault/logs/audit.log"
    log_raw   = "false"
    hmac_accessor = "true"
    mode      = "0600"
    format    = "json"
  }
}

# Syslog audit 设备
resource "vault_audit" "syslog" {
  type = "syslog"
  
  options = {
    facility = "AUTH"
    tag      = "vault"
  }
}

# Socket audit 设备
resource "vault_audit" "socket" {
  type = "socket"
  
  options = {
    address     = "127.0.0.1:9090"
    socket_type = "tcp"
  }
}
```

### Secrets Data 配置
```hcl
# terraform/secrets.tf

# 将 Terraform 变量存储为 secrets
resource "vault_kv_secret_v2" "terraform_prod" {
  mount = vault_mount.terraform_secrets.path
  name  = "terraform/prod/aws"
  
  data_json = jsonencode({
    aws_region      = "us-east-1"
    instance_type   = "t3.large"
    vpc_cidr        = "10.0.0.0/16"
    availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  })
  
  custom_metadata {
    max_versions = 10
    cas_required = false
    
    data = {
      environment = "production"
      team        = "infrastructure"
      managed_by  = "terraform"
    }
  }
}

resource "vault_kv_secret_v2" "terraform_staging" {
  mount = vault_mount.terraform_secrets.path
  name  = "terraform/staging/aws"
  
  data_json = jsonencode({
    aws_region    = "us-west-2"
    instance_type = "t3.medium"
    vpc_cidr      = "10.1.0.0/16"
  })
}

resource "vault_kv_secret_v2" "database_config" {
  mount = vault_mount.terraform_secrets.path
  name  = "terraform/prod/database"
  
  data_json = jsonencode({
    db_host     = "postgres.company.com"
    db_port     = 5432
    db_name     = "production"
    db_username = "app_user"
  })
}
```

### 配置调优
```hcl
# terraform/tuning.tf

# 配置最大请求持续时间
resource "vault_mount" "tuned_kv" {
  path = "tuned-secret"
  type = "kv-v2"
  
  options = {
    version = "2"
  }
  
  # 调优参数
  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 86400
  
  # 审计设置
  audit_non_hmac_request_keys  = ["key1", "key2"]
  audit_non_hmac_response_keys = ["response_key"]
  
  # 列表可见性
  listing_visibility = "unauth"
  
  # 透传请求头
  passthrough_request_headers = ["X-Custom-Header"]
  
  # 允许的响应头
  allowed_response_headers = ["X-Response-Header"]
}
```

上述综合配置涵盖了大多数 Vault engine 类型、auth methods、policies 以及可以作为 GitHub 代码管理的运行配置。