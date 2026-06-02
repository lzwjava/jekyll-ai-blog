---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: KV vs Cubbyhole Secrets Engines Compared
translated: false
type: note
---

The key differences between KV (Key-Value) and Cubbyhole secrets engines in HashiCorp Vault are:

## Scope and Access

**KV Engine**: Shared storage that multiple tokens/users can access based on ACL policies. If you have the right permissions, you can read secrets that others have written.

**Cubbyhole**: Private, token-scoped storage. Each token gets its own isolated cubbyhole that only that specific token can access - even the root token cannot read another token's cubbyhole.

## Lifecycle

**KV Engine**: Secrets persist independently of tokens. They remain in Vault until explicitly deleted, regardless of token lifecycle.

**Cubbyhole**: Tied to the token's lifecycle. When the token expires or is revoked, all data in its cubbyhole is automatically destroyed.

## Use Cases

**KV Engine**: General-purpose secret storage for applications, shared credentials, configuration data, and secrets that need to be accessed by multiple entities.

**Cubbyhole**: Temporary secret storage, response wrapping (wrapping secrets for secure delivery), secure secret handoff between processes, and storing ephemeral data that shouldn't outlive a specific session.

## Versioning

**KV Engine**: Has two versions - KV v1 (no versioning) and KV v2 (versioning, soft deletes, and configurable retention).

**Cubbyhole**: No versioning capability - it's always a simple key-value store.

## Example Scenario

If you use response wrapping to securely deliver a database password to an application, Vault creates a single-use token and stores the wrapped secret in that token's cubbyhole. Once the application retrieves it, the token is used up and the cubbyhole data vanishes - perfect for secure one-time secret delivery.
