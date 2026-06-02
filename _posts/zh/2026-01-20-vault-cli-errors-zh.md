---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 了解 Vault CLI 错误及命令
translated: true
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

- 当你没有设置环境变量 `VAULT_ADDR` 时，Vault CLI 默认指向 `https://127.0.0.1:8200`
- 但在你的 local/dev 设置中，Vault 极有可能运行在 **insecure mode** (HTTP，而非 HTTPS)
- client 尝试 HTTPS → server 返回 plain HTTP → Go HTTP client 拒绝该响应 (现代安全行为)

这是在 dev 模式下启动 Vault 时最常见的 #1 错误：

```bash
vault server -dev
# → listens on http://127.0.0.1:8200 (no TLS)
```

### 2. Fix – tell Vault client to use HTTP

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
```

在此之后，client 知道它应该使用 plain HTTP → 连接成功。

许多人会将其中一行永久添加到 `~/.zshrc` / `~/.bashrc` 中：

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

- 显示的 Path 是 `secret/data/prod/database`
  → 这证明你正在使用 **KV version 2** engine
  (KV v1 仅会显示 `secret/prod/database`)
- Vault 自动在 KV v2 的 API path 中添加了 `/data/`
- Version = 1 → 这是对该路径的第一次写入
- 未显示 TTL → 默认值 (在 dev 模式下通常为 0 = 永不过期)

### 4. Reading the secret back

```bash
vault kv get -mount="secret" "prod/database"
```

Two important observations:

1. 你使用了 **modern/recommended** 语法 (2021+):

   ```bash
   vault kv get -mount=secret prod/database
   ```

   这是 Vault 1.10+ 之后的首选方式，它清晰地将 mount point 与 secret path 分开。

2. 但在你粘贴的内容中输出是不完整的
   (你在实际数据出现前截断了它)

   预期的完整输出应如下所示：

   ```
   ====== Data ======
   Key         Value
   ---         -----
   password    supersecret
   ```

   如果你没有看到数据，可能的原因：

   - 你过早按下了 Ctrl+C
   - 你的 terminal 截断了输出
   - 你正在使用行为不同的旧版 Vault CLI (< 1.4)

### Summary – Quick Reference Table

| Action                              | Command style (2024–2026 recommended)       | Internal API path                  | Engine   |
|-------------------------------------|-----------------------------------------------|------------------------------------|----------|
| Write secret                        | `vault kv put -mount=secret prod/db pass=abc` | `secret/data/prod/db`              | KV v2    |
| Old style (still works)             | `vault kv put secret/prod/db pass=abc`        | `secret/data/prod/db`              | KV v2    |
| Read secret                         | `vault kv get -mount=secret prod/db`          | `secret/data/prod/db`              | KV v2    |
| Very old KV v1 (not recommended)    | `vault kv put secret/prod/db pass=abc`        | `secret/prod/db`                   | KV v1    |

### Quick Fix Checklist for next time

1. 使用 dev server 时务必设置 `VAULT_ADDR`
   `export VAULT_ADDR=http://127.0.0.1:8200`

2. 使用 `-mount=` 语法 — 它更清晰且更具前瞻性

3. 检查 engine 版本：
   `vault kv metadata get -mount=secret prod/database`
   或者观察路径中是否出现了 `/data/`

希望这能解释清楚整个过程！

**References:**

- None (explanation based on standard Vault behavior and error messages)
