---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Cubbyhole Secrets Token Scoped Storage
translated: false
type: note
---

You're thinking of **Cubbyhole**, not "chubbyhole" (common mistake!).

Yes, you're mostly right about how it works. The Cubbyhole secret engine is a per-token secret storage in Vault. Here's what makes it special:

**Key characteristics:**

- **Token-scoped**: Each token gets its own private cubbyhole that only that token can access
- **Completely isolated**: Even root tokens or other privileged tokens cannot read another token's cubbyhole
- **Lifecycle tied to token**: When the token expires or is revoked, the cubbyhole and all its secrets are automatically deleted

**About login and disappearing secrets:**

When you "login again," you get a *new* token, which means a *new* cubbyhole - so yes, the secrets from your previous token's cubbyhole will be gone (they disappeared when the old token expired/was revoked). You won't have access to the old cubbyhole's contents.

**Common use case:**

Cubbyhole is often used for secure secret delivery - for example, in response wrapping, where Vault wraps a secret in a single-use token whose cubbyhole contains the actual secret. Once that token is used to unwrap the secret, the token is revoked and the cubbyhole disappears.

So it's intentionally ephemeral and tied to the token's lifecycle - perfect for temporary secret storage or secure handoffs, but not for long-term secret storage.
