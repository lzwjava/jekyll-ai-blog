---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Terraform 机密管理的 Vault Jenkins JWT 认证
translated: true
type: note
---

我将帮助你了解如何使用 HashiCorp Vault 的 Jenkins JWT auth method 从 GitHub 读取 Terraform variables，包括 KV secrets engine 的配置。

## 集成概述

此集成通常涉及：
1. Jenkins 使用 JWT tokens 向 Vault 进行身份验证
2. Vault 根据 JWT claims 授予访问权限
3. Jenkins 读取存储在 Vault KV engine 中的 secrets（如 Terraform variables）
4. 这些 secrets 可能会引用存储在 GitHub 中的配置

## 在 Vault 中设置 Jenkins JWT Auth

首先，在 Vault 中启用并配置 JWT auth method：

```bash
# Enable JWT auth
vault auth enable jwt

# Configure JWT auth for Jenkins
vault write auth/jwt/config \
    jwks_url="https://your-jenkins-server/jwtauth/jwks" \
    bound_issuer="https://your-jenkins-server"
```

## 为 Terraform Variables 创建 Vault Policy

```hcl
# terraform-read-policy.hcl
path "secret/data/terraform/*" {
  capabilities = ["read", "list"]
}

path "kv/data/terraform/*" {
  capabilities = ["read", "list"]
}
```

应用该 Policy：
```bash
vault policy write terraform-read terraform-read-policy.hcl
```

## 配置 JWT Role

创建一个将 Jenkins JWT tokens 映射到 Vault policies 的 Role：

```bash
vault write auth/jwt/role/jenkins-terraform \
    role_type="jwt" \
    bound_claims='{"jenkins_job_name":"terraform-*"}' \
    user_claim="sub" \
    policies="terraform-read" \
    ttl=1h
```

## 在 Vault KV Engine 中存储 Terraform Variables

```bash
# Enable KV v2 secrets engine
vault secrets enable -path=secret kv-v2

# Store terraform variables
vault kv put secret/terraform/prod \
    aws_region="us-east-1" \
    instance_type="t3.medium" \
    vpc_cidr="10.0.0.0/16"
```

## Jenkins Pipeline 配置

以下是你的 Jenkinsfile 进行身份验证并获取 secrets 的方式：

```groovy
pipeline {
    agent any
    
    environment {
        VAULT_ADDR = 'https://vault.yourcompany.com'
    }
    
    stages {
        stage('Authenticate to Vault') {
            steps {
                script {
                    // Jenkins JWT plugin generates the token
                    def jwtToken = readJSON(text: sh(
                        script: 'curl -s http://localhost:8080/jwtauth/token',
                        returnStdout: true
                    ))
                    
                    // Login to Vault with JWT
                    def vaultLogin = sh(
                        script: """
                            curl -s -X POST ${VAULT_ADDR}/v1/auth/jwt/login \
                            -d '{"jwt": "${jwtToken.token}", "role": "jenkins-terraform"}'
                        """,
                        returnStdout: true
                    )
                    
                    env.VAULT_TOKEN = readJSON(text: vaultLogin).auth.client_token
                }
            }
        }
        
        stage('Read Terraform Variables') {
            steps {
                script {
                    // Read from KV engine
                    def secrets = sh(
                        script: """
                            curl -s -H "X-Vault-Token: ${VAULT_TOKEN}" \
                            ${VAULT_ADDR}/v1/secret/data/terraform/prod
                        """,
                        returnStdout: true
                    )
                    
                    def tfVars = readJSON(text: secrets).data.data
                    
                    // Write to terraform.tfvars
                    writeFile file: 'terraform.tfvars', text: """
aws_region = "${tfVars.aws_region}"
instance_type = "${tfVars.instance_type}"
vpc_cidr = "${tfVars.vpc_cidr}"
                    """
                }
            }
        }
        
        stage('Checkout Config from GitHub') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourorg/terraform-config.git',
                    credentialsId: 'github-token'
            }
        }
        
        stage('Run Terraform') {
            steps {
                sh '''
                    terraform init
                    terraform plan -var-file=terraform.tfvars
                '''
            }
        }
    }
}
```

## 使用适用于 Jenkins 的 HashiCorp Vault Plugin

或者，使用官方 Vault plugin 进行更简洁的集成：

```groovy
pipeline {
    agent any
    
    options {
        vault(
            vaultUrl: 'https://vault.yourcompany.com',
            vaultCredentialId: 'vault-jwt-auth',
            engineVersion: 2
        )
    }
    
    stages {
        stage('Read Secrets') {
            steps {
                script {
                    def secrets = [
                        [
                            path: 'secret/terraform/prod',
                            engineVersion: 2,
                            secretValues: [
                                [envVar: 'AWS_REGION', vaultKey: 'aws_region'],
                                [envVar: 'INSTANCE_TYPE', vaultKey: 'instance_type']
                            ]
                        ]
                    ]
                    
                    withVault([vaultSecrets: secrets]) {
                        sh 'echo "AWS Region: $AWS_REGION"'
                        // Use secrets in terraform
                    }
                }
            }
        }
    }
}
```

## Vault KV Engine 配置结构

你的 KV engine 可能会这样组织：

```
secret/
├── terraform/
│   ├── dev/
│   │   ├── aws-config
│   │   └── database-config
│   ├── staging/
│   └── prod/
│       ├── aws-config
│       ├── database-config
│       └── github-config
```

## GitHub 集成

如果你将 Vault 配置（以代码形式）存储在 GitHub 中，你可能会有：

```hcl
# github-repo: vault-config/terraform-secrets.hcl
path "secret/data/terraform/*" {
  capabilities = ["read", "list"]
}

# KV engine mount configuration
resource "vault_mount" "terraform_secrets" {
  path = "secret"
  type = "kv-v2"
  
  options = {
    version = "2"
  }
}
```

此设置允许 Jenkins 使用 JWT 向 Vault 进行身份验证，从 KV engine 中读取 Terraform variables，并将其与来自 GitHub 仓库的配置文件结合使用。