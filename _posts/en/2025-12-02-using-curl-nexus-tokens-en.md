---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Using Nexus User Tokens with curl
translated: false
type: note
---

Question: In Nexus Repository, can I use `-H "Authorization: Basic ..."` directly instead of `-u` when authenticating with a user access token?

Answer: Yes, you can manually use the `-H "Authorization: Basic …"` header with a Nexus user access token. It works exactly the same as `-u`, because Nexus user tokens are designed to be used with **HTTP Basic Authentication**.

### How to construct it manually

A Nexus user token consists of two parts:

- **name code** (e.g., `abc123XYZ`) → acts as the “username”
- **pass code** (e.g., `def456UVW789`) → acts as the “password”

You combine them as `name_code:pass_code`, Base64-encode that string, and send it in the Authorization header.

#### Method 1: Let curl do the encoding (recommended, same as `-u`)

```bash
curl -u abc123XYZ:def456UVW789 \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

#### Method 2: Manually add the Authorization header (explicit Basic)

```bash
# One-liner (Linux/macOS)
TOKEN="abc123XYZ:def456UVW789"
AUTH_HEADER="Authorization: Basic $(echo -n "$TOKEN" | base64 -w 0)"

curl -H "$AUTH_HEADER" \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

Or written out fully:

```bash
curl -H "Authorization: Basic YWJjMTIzWFlaOmRlZjQ1NlVWVzc4OQ==" \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

(Where `YWJjMTIzWFlaOmRlZjQ1NlVWVzc4OQ==` is the Base64 of `abc123XYZ:def456UVW789`)

#### Method 3: Using printf + base64 on any system

```bash
curl -H "Authorization: Basic $(printf 'abc123XYZ:def456UVW789' | base64)" \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

### Summary: Which should you use?

| Method                          | Recommended? | When to use it                                   |
|---------------------------------|--------------|--------------------------------------------------|
| `curl -u name_code:pass_code`   | Yes          | Everyday use, scripts, Maven settings.xml, etc.  |
| `-H "Authorization: Basic …"`   | Yes          | When you already have the Base64 string or need full control (e.g., some CI tools) |

Both methods are 100% equivalent for Nexus user tokens.
Never use `Authorization: Bearer` with Nexus user tokens — that is reserved for future OAuth/OIDC integrations and will always return 401.

- [Nexus User Token Documentation](https://help.sonatype.com/repomanager3/nexus-repository-administration/user-management/user-tokens)
- [Nexus REST API Authentication](https://help.sonatype.com/repomanager3/rest-and-integration-api)
