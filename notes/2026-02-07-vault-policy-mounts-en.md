---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault Policy and Mounts Guide
translated: false
type: note
---

I'll help explain Vault policy and the `sys/mounts` path.

## Vault Policy

In HashiCorp Vault, a **policy** is a set of rules that defines what operations a user or application can perform on specific paths within Vault. Policies are written in HashiCorp Configuration Language (HCL) or JSON and follow a deny-by-default model—if something isn't explicitly allowed, it's denied.

A basic policy looks like this:

```hcl
path "secret/data/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "sys/mounts" {
  capabilities = ["read"]
}
```

The main capabilities you can grant are:
- `create` - Create new data
- `read` - Read existing data
- `update` - Modify existing data
- `delete` - Delete data
- `list` - List keys/paths
- `sudo` - Allows access to root-protected paths
- `deny` - Explicitly denies access (takes precedence)

## The `sys/mounts` Path

`sys/mounts` is a **system backend path** in Vault that deals with secrets engines management. Specifically:

- **What it does**: This path lets you view, enable, disable, and configure secrets engines (mount points) in Vault
- **Why it matters**: Secrets engines are components that store, generate, or encrypt data. Each type (like KV, PKI, AWS, database) gets mounted at a specific path

**Common operations on `sys/mounts`:**
- `read` on `sys/mounts` - List all enabled secrets engines
- `create`/`update` on `sys/mounts/*` - Enable new secrets engines
- `delete` on `sys/mounts/*` - Disable secrets engines

For example, granting read access allows someone to see what secrets engines are mounted, while create/delete would let them modify Vault's configuration—typically requiring admin privileges.