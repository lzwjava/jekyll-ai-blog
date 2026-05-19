---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault Configuration as Code Guide
translated: false
type: note
---

I'll expand on Vault configuration options that can be managed as code in GitHub, covering policies, mounts, auth methods, and various engine configurations.

## Complete Vault Configuration as Code Structure

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

## 1. Expanded Policy Configuration

```hcl
# policies/terraform-secrets.hcl

# Read access to Terraform secrets in KV v2
path "secret/data/terraform/*" {
  capabilities = ["read", "list"]
}

# List terraform secret paths
path "secret/metadata/terraform/*" {
  capabilities = ["list"]
}

# Read specific terraform environments
path "secret/data/terraform/prod/*" {
  capabilities = ["read"]
}

path "secret/data/terraform/staging/*" {
  capabilities = ["read"]
}

path "secret/data/terraform/dev/*" {
  capabilities = ["read", "list"]
}

# Access to database credentials engine
path "database/creds/terraform-role" {
  capabilities = ["read"]
}

# Access to AWS dynamic credentials
path "aws/creds/terraform-role" {
  capabilities = ["read"]
}

# Access to PKI for certificates
path "pki/issue/terraform-cert" {
  capabilities = ["create", "update"]
}

# Read transit encryption keys
path "transit/encrypt/terraform-key" {
  capabilities = ["update"]
}

path "transit/decrypt/terraform-key" {
  capabilities = ["update"]
}

# Deny certain paths
path "secret/data/terraform/prod/root-password" {
  capabilities = ["deny"]
}
```

## 2. Comprehensive Terraform Configuration

### Main Configuration
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
  token   = var.vault_token  # Use appropriate auth in production
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

### Secret Engines Configuration
{% raw %}
```hcl
# terraform/secret-engines.tf

# KV v2 Secrets Engine for Terraform variables
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

# Additional KV v2 for application secrets
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

# Database connection configuration
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

# Database role for Terraform
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

# AWS role for Terraform
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

# PKI Secrets Engine (for certificates)
resource "vault_mount" "pki" {
  path                      = "pki"
  type                      = "pki"
  description               = "PKI secrets engine"
  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 87600  # 10 years
}

# Configure PKI
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

# PKI role for Terraform-managed certificates
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

# Transit Secrets Engine (encryption as a service)
resource "vault_mount" "transit" {
  path        = "transit"
  type        = "transit"
  description = "Encryption as a service"
}

# Transit encryption key
resource "vault_transit_secret_backend_key" "terraform_key" {
  backend          = vault_mount.transit.path
  name             = "terraform-key"
  type             = "aes256-gcm96"
  deletion_allowed = false
  
  # Key rotation
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

# TOTP Secrets Engine (for MFA)
resource "vault_mount" "totp" {
  path        = "totp"
  type        = "totp"
  description = "TOTP MFA tokens"
}
```
{% endraw %}

### Auth Methods Configuration
{% raw %}
```hcl
# terraform/auth-methods.tf

# JWT Auth Method for Jenkins
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

# JWT role for Jenkins Terraform jobs
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

# OIDC Auth Method for GitHub Actions
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

# AppRole for automated services
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

# LDAP group mapping
resource "vault_ldap_auth_backend_group" "terraform_team" {
  backend  = vault_ldap_auth_backend.ldap.path
  groupname = "terraform-team"
  policies  = ["terraform-secrets", "database-read"]
}
```
{% endraw %}

### Policies Configuration
```hcl
# terraform/policies.tf

# Import HCL policy files
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

# Policy for PKI operations
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

### Entity and Group Configuration
```hcl
# terraform/entities.tf

# Create entity for service account
resource "vault_identity_entity" "terraform_service" {
  name     = "terraform-service"
  policies = ["terraform-secrets", "database-read"]
  
  metadata = {
    environment = "production"
    team        = "infrastructure"
  }
}

# Entity alias for JWT auth
resource "vault_identity_entity_alias" "terraform_jenkins" {
  name           = "terraform-pipeline"
  mount_accessor = vault_jwt_auth_backend.jenkins.accessor
  canonical_id   = vault_identity_entity.terraform_service.id
}

# Create identity group
resource "vault_identity_group" "terraform_users" {
  name     = "terraform-users"
  type     = "internal"
  policies = ["terraform-secrets"]
  
  metadata = {
    version = "1.0"
  }
}

# Add entity to group
resource "vault_identity_group_member_entity_ids" "terraform_members" {
  group_id          = vault_identity_group.terraform_users.id
  member_entity_ids = [vault_identity_entity.terraform_service.id]
  exclusive         = false
}
```

### Namespace Configuration (Vault Enterprise)
```hcl
# terraform/namespaces.tf

resource "vault_namespace" "engineering" {
  path = "engineering"
}

resource "vault_namespace" "terraform" {
  namespace = vault_namespace.engineering.path
  path      = "terraform"
}

# Mount secrets engine in namespace
resource "vault_mount" "terraform_ns_secrets" {
  namespace = "${vault_namespace.engineering.path}/${vault_namespace.terraform.path}"
  path      = "secrets"
  type      = "kv-v2"
}
```

### Audit Configuration
```hcl
# terraform/audit.tf

# File audit device
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

# Syslog audit device
resource "vault_audit" "syslog" {
  type = "syslog"
  
  options = {
    facility = "AUTH"
    tag      = "vault"
  }
}

# Socket audit device
resource "vault_audit" "socket" {
  type = "socket"
  
  options = {
    address     = "127.0.0.1:9090"
    socket_type = "tcp"
  }
}
```

### Secrets Data Configuration
```hcl
# terraform/secrets.tf

# Store Terraform variables as secrets
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

### Configuration Tuning
```hcl
# terraform/tuning.tf

# Configure max request duration
resource "vault_mount" "tuned_kv" {
  path = "tuned-secret"
  type = "kv-v2"
  
  options = {
    version = "2"
  }
  
  # Tuning parameters
  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 86400
  
  # Audit settings
  audit_non_hmac_request_keys  = ["key1", "key2"]
  audit_non_hmac_response_keys = ["response_key"]
  
  # Listing visibility
  listing_visibility = "unauth"
  
  # Passthrough request headers
  passthrough_request_headers = ["X-Custom-Header"]
  
  # Allowed response headers
  allowed_response_headers = ["X-Response-Header"]
}
```

This comprehensive configuration covers most Vault engine types, auth methods, policies, and operational configurations that can be managed as code in GitHub.