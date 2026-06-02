---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding Vault CLI Errors and Commands
translated: false
type: note
---

**Question:** Explain the Vault commands and output in this terminal session (why there was an HTTPS error first, what changed after exporting VAULT_ADDR, and what the kv put / kv get output means)

**Answer:**

This is a typical beginner-to-intermediate HashiCorp Vault workflow demonstration showing:

1. How Vault client discovers the server address
2. The very common TLS/http protocol mismatch error
3. Writing and reading a secret using KV v2 engine

Here’s a step-by-step explanation of what happened:

### 1. First command – failure

```bash
vault kv put secret/prod/database password=supersecret
```

**Error:**

```
WARNING! VAULT_ADDR and -address unset. Defaulting to https://127.0.0.1:8200.
Get "https://127.0.0.1:8200/v1/sys/internal/ui/mounts/secret/prod/database": http: server gave HTTP response to HTTPS client
```

**What happened:**

- When you do **not** set the environment variable `VAULT_ADDR`, the Vault CLI defaults to `https://127.0.0.1:8200`
- But in your local/dev setup, Vault is most likely running in **insecure mode** (HTTP, not HTTPS)
- The client tries HTTPS → server answers with plain HTTP → Go HTTP client refuses the response (modern security behavior)

This is the #1 most common error when someone starts Vault in dev mode:

```bash
vault server -dev
# → listens on http://127.0.0.1:8200 (no TLS)
```

### 2. Fix – tell Vault client to use HTTP

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
```

After this, the client knows it should speak plain HTTP → connection succeeds.

Many people add one of these lines permanently to `~/.zshrc` / `~/.bashrc`:

```bash
export VAULT_ADDR=http://127.0.0.1:8200
# or when using docker / different port
# export VAULT_ADDR=http://localhost:18200
```

### 3. Successful write – KV v2

```bash
vault kv put secret/prod/database password=supersecret
```

**Output:**

```
====== Secret Path ======
secret/data/prod/database

======= Metadata =======
Key              Value
---              -----
created_time     2026-01-20T12:05:18.810307Z
custom_metadata  <nil>
deletion_time    n/a
destroyed        false
version          1
```

Key points:

- Path shown is `secret/data/prod/database`
  → this proves you are using **KV version 2** engine
  (KV v1 would show just `secret/prod/database`)
- Vault automatically added `/data/` in the API path for KV v2
- Version = 1 → this was the first write to this path
- No TTL shown → default (usually 0 = no expiration in dev mode)

### 4. Reading the secret back

```bash
vault kv get -mount="secret" "prod/database"
```

Two important observations:

1. You used the **modern/recommended** syntax (2021+):

   ```bash
   vault kv get -mount=secret prod/database
   ```

   This is the preferred way since Vault 1.10+ and clearly separates mount point from secret path.

2. But the output is incomplete in your paste
   (you cut it off before the actual data)

   Expected full output should look like:

   ```
   ====== Data ======
   Key         Value
   ---         -----
   password    supersecret
   ```

   If you don’t see the data, possible reasons:

   - you pressed Ctrl+C too early
   - your terminal truncated output
   - you are using very old Vault CLI (< 1.4) that behaves differently

### Summary – Quick Reference Table

| Action                              | Command style (2024–2026 recommended)       | Internal API path                  | Engine   |
|-------------------------------------|-----------------------------------------------|------------------------------------|----------|
| Write secret                        | `vault kv put -mount=secret prod/db pass=abc` | `secret/data/prod/db`              | KV v2    |
| Old style (still works)             | `vault kv put secret/prod/db pass=abc`        | `secret/data/prod/db`              | KV v2    |
| Read secret                         | `vault kv get -mount=secret prod/db`          | `secret/data/prod/db`              | KV v2    |
| Very old KV v1 (not recommended)    | `vault kv put secret/prod/db pass=abc`        | `secret/prod/db`                   | KV v1    |

### Quick Fix Checklist for next time

1. Always set `VAULT_ADDR` when using dev server
   `export VAULT_ADDR=http://127.0.0.1:8200`

2. Use `-mount=` syntax — it’s clearer and more future-proof

3. Check engine version:
   `vault kv metadata get -mount=secret prod/database`
   or look whether `/data/` appears in the path

Hope this clears up the whole sequence!

**References:**

- None (explanation based on standard Vault behavior and error messages)
