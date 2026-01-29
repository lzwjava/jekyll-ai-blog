---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault Mounts Explained Simply
translated: false
type: note
---

I'll explain HashiCorp Vault mounts, which are a fundamental concept for organizing secrets and authentication methods.

## What is a Mount?

In Vault, a **mount** is like a filesystem mount point - it's a path where you attach a secrets engine or authentication method. Think of it as plugging different modules into specific locations in Vault's API path structure.

When you enable a secrets engine or auth method, you're "mounting" it at a specific path. All operations for that engine then happen under that path.

## Mount Structure

Vault's path structure looks like:
```
<mount_path>/<operation>
```

For example:
- `secret/data/myapp` - the `secret/` is the mount point for KV v2 engine
- `aws/creds/my-role` - the `aws/` is the mount point for AWS secrets engine
- `database/creds/my-role` - the `database/` is the mount point

## What is sys/mount?

`sys/mount` is a special **system backend** path used to manage secrets engine mounts. It's part of Vault's system backend (paths starting with `sys/`) which handles Vault's configuration and management.

**Key operations:**

**List all mounts:**
```bash
vault secrets list
# or via API
curl -H "X-Vault-Token: $TOKEN" $VAULT_ADDR/v1/sys/mounts
```

**Enable a new secrets engine:**
```bash
vault secrets enable -path=myapp kv
# or via API
curl -H "X-Vault-Token: $TOKEN" \
  -X POST \
  -d '{"type":"kv","options":{"version":"2"}}' \
  $VAULT_ADDR/v1/sys/mounts/myapp
```

**Disable/unmount:**
```bash
vault secrets disable myapp
# or via API
curl -H "X-Vault-Token: $TOKEN" \
  -X DELETE \
  $VAULT_ADDR/v1/sys/mounts/myapp
```

## Types of Mounts

**Secrets Engine Mounts** (`sys/mounts`):
- Dynamic secrets: AWS, database, SSH
- Static secrets: KV (key-value)
- Encryption as a service: Transit
- PKI: Certificate management

**Auth Method Mounts** (`sys/auth`):
- Similar concept but for authentication
- Examples: userpass, LDAP, Kubernetes, AppRole

## Example

When you enable the AWS secrets engine:
```bash
vault secrets enable -path=aws aws
```

You've created a mount at `aws/`. Now you can:
- Configure it: `vault write aws/config/root ...`
- Create roles: `vault write aws/roles/my-role ...`
- Generate credentials: `vault read aws/creds/my-role`

Each secrets engine type has its own API endpoints and operations, but they all work through this mount system.

Does this help clarify how mounts work? Let me know if you'd like me to explain any specific aspect in more detail!