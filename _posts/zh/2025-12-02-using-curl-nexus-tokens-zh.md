---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Nexus 用户令牌与 curl
translated: true
type: note
---

问题：在 Nexus Repository 中，当我使用用户访问令牌进行身份验证时，可以直接使用 `-H "Authorization: Basic ..."` 而不是 `-u` 吗？

回答：是的，你可以手动使用带有 Nexus 用户访问令牌的 `-H "Authorization: Basic …"` 头部。它的工作方式与 `-u` 完全相同，因为 Nexus 用户令牌旨在与 **HTTP 基本认证** 一起使用。

### 如何手动构建它

Nexus 用户令牌由两部分组成：
- **名称代码**（例如 `abc123XYZ`）→ 作为“用户名”
- **通行码**（例如 `def456UVW789`）→ 作为“密码”

将它们组合为 `name_code:pass_code`，对该字符串进行 Base64 编码，并在 Authorization 头部中发送。

#### 方法 1：让 curl 进行编码（推荐，与 `-u` 相同）
```bash
curl -u abc123XYZ:def456UVW789 \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

#### 方法 2：手动添加 Authorization 头部（显式 Basic）
```bash
# 单行命令 (Linux/macOS)
TOKEN="abc123XYZ:def456UVW789"
AUTH_HEADER="Authorization: Basic $(echo -n "$TOKEN" | base64 -w 0)"

curl -H "$AUTH_HEADER" \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

或完整写出：
```bash
curl -H "Authorization: Basic YWJjMTIzWFlaOmRlZjQ1NlVWVzc4OQ==" \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```
（其中 `YWJjMTIzWFlaOmRlZjQ1NlVWVzc4OQ==` 是 `abc123XYZ:def456UVW789` 的 Base64 编码）

#### 方法 3：在任何系统上使用 printf + base64
```bash
curl -H "Authorization: Basic $(printf 'abc123XYZ:def456UVW789' | base64)" \
     "http://your-nexus.example.com/service/rest/v1/components?repository=maven-releases"
```

### 总结：应该使用哪种方法？

| 方法                            | 推荐？ | 何时使用                                         |
|---------------------------------|--------|--------------------------------------------------|
| `curl -u name_code:pass_code`   | 是     | 日常使用、脚本、Maven settings.xml 等              |
| `-H "Authorization: Basic …"`   | 是     | 当您已经有 Base64 字符串或需要完全控制时（例如，某些 CI 工具） |

两种方法对于 Nexus 用户令牌来说是 100% 等效的。
切勿将 `Authorization: Bearer` 与 Nexus 用户令牌一起使用——这 reserved for future OAuth/OIDC integrations and will always return 401。

* [Nexus User Token Documentation](https://help.sonatype.com/repomanager3/nexus-repository-administration/user-management/user-tokens)
* [Nexus REST API Authentication](https://help.sonatype.com/repomanager3/rest-and-integration-api)
