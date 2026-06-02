---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault Namespaces for Tenant Isolation
translated: false
type: note
---

Namespaces in Vault are a way to create isolated environments within a single Vault cluster. Think of them as separate "tenants" or compartments that provide logical isolation for different teams, applications, or business units.

## Key Concepts

**Isolation**: Each namespace has its own set of policies, secrets engines, auth methods, and entities. What happens in one namespace is completely isolated from others.

**Hierarchical structure**: Namespaces can be nested, creating a parent-child relationship. For example, you might have `engineering/` as a parent namespace with `engineering/app1/` and `engineering/app2/` as children.

**Root namespace**: By default, everything in Vault exists in the root namespace. When you create new namespaces, they branch off from root.

## Common Use Cases

Namespaces are particularly useful for multi-tenant environments where you want to provide teams or customers with their own isolated Vault environment without running multiple clusters. For example, a service provider might create a namespace for each customer, or an enterprise might create namespaces for different departments.

## Basic Operations

You interact with namespaces using the `-namespace` flag or the `VAULT_NAMESPACE` environment variable:

```bash
# Create a namespace
vault namespace create engineering

# List namespaces
vault namespace list

# Use a namespace for commands
vault secrets list -namespace=engineering
```

When working in nested namespaces, you use the full path like `engineering/app1`.

**Note**: Namespaces are a Vault Enterprise feature and aren't available in the open-source version.

Is there a specific aspect of namespaces you'd like to explore further, like access control, delegation, or practical implementation patterns?
