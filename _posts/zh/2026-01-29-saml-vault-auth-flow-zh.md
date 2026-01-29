---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: HashiCorp Vault 中的 SAML 身份验证流程
translated: true
type: note
---

HashiCorp Vault 的 SAML login 通过将 Vault 与外部 SAML Identity Provider (IdP)（如 Okta、Azure AD 等）集成来工作。以下是 authentication flow 的工作原理：

**Initial Setup：**
- Vault 配置了 SAML auth method，其中包括 IdP 的 metadata（SSO URL、entity ID、certificate）
- IdP 将 Vault 配置为 Service Provider (SP)，包括 Vault 的 callback URL 和 entity ID
- Vault 中的 Policies 被映射到 SAML assertions（如 groups 或 attributes）

**Authentication Flow：**

1. **User initiates login** - 用户导航到 Vault 的 SAML login endpoint，或使用 CLI/API 配合 SAML method

2. **SAML request generation** - Vault 生成一个 SAML authentication request，并将用户的浏览器重定向到 IdP 的 SSO URL

3. **IdP authentication** - 用户在 IdP 端进行身份验证（username/password、MFA 等）

4. **SAML response** - 身份验证成功后，IdP 生成一个包含用户 attributes（username、email、group memberships）的已签名 SAML assertion，并将其发回 Vault 的 callback URL

5. **Assertion validation** - Vault 通过以下方式验证 SAML response：
   - 使用 IdP 的 certificate 验证 digital signature
   - 检查 assertion 是否已过期
   - 验证 audience 和 recipient 是否匹配 Vault 的配置

6. **Token generation** - 如果验证成功，Vault 将：
   - 从 assertion 中提取 user identity 和 attributes
   - 将 SAML groups/attributes 映射到 Vault policies
   - 签发一个附带相应 policies 的 Vault token

7. **Access granted** - 用户现在可以使用此 token 根据其分配的 policies 访问 Vault 资源

核心优势在于 Vault 不直接存储或管理用户 credentials——它信任 IdP 的 assertions，并专注于通过 policy mappings 进行 authorization。