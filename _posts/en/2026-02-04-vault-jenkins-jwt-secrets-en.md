---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault Jenkins JWT for Terraform Secrets
translated: false
type: note
---

I'll help you understand how HashiCorp Vault's Jenkins JWT auth method can be used to read Terraform variables from GitHub, including configuration for the KV secrets engine.

## Overview of the Integration

This integration typically involves:

1. Jenkins authenticating to Vault using JWT tokens
2. Vault granting access based on JWT claims
3. Jenkins reading secrets (like Terraform variables) stored in Vault's KV engine
4. These secrets might reference configurations stored in GitHub

## Setting Up Jenkins JWT Auth in Vault

First, enable and configure the JWT auth method in Vault:

```bash
# Enable JWT auth
vault auth enable jwt

# Configure JWT auth for Jenkins
vault write auth/jwt/config \
    jwks_url="https://your-jenkins-server/jwtauth/jwks" \
    bound_issuer="https://your-jenkins-server"
```

## Create a Vault Policy for Terraform Variables

```hcl
# terraform-read-policy.hcl
path "secret/data/terraform/*" {
  capabilities = ["read", "list"]
}

path "kv/data/terraform/*" {
  capabilities = ["read", "list"]
}
```

Apply the policy:

```bash
vault policy write terraform-read terraform-read-policy.hcl
```

## Configure JWT Role

Create a role that maps Jenkins JWT tokens to Vault policies:

```bash
vault write auth/jwt/role/jenkins-terraform \
    role_type="jwt" \
    bound_claims='{"jenkins_job_name":"terraform-*"}' \
    user_claim="sub" \
    policies="terraform-read" \
    ttl=1h
```

## Store Terraform Variables in Vault KV Engine

```bash
# Enable KV v2 secrets engine
vault secrets enable -path=secret kv-v2

# Store terraform variables
vault kv put secret/terraform/prod \
    aws_region="us-east-1" \
    instance_type="t3.medium" \
    vpc_cidr="10.0.0.0/16"
```

## Jenkins Pipeline Configuration

Here's how your Jenkinsfile would authenticate and retrieve secrets:

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

## Using HashiCorp Vault Plugin for Jenkins

Alternatively, use the official Vault plugin for cleaner integration:

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

## Vault KV Engine Configuration Structure

Your KV engine might be organized like this:

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

## GitHub Integration

If you're storing Vault configuration in GitHub (as code), you might have:

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

This setup allows Jenkins to authenticate to Vault using JWT, read Terraform variables from the KV engine, and use those alongside configuration files from GitHub repositories.
