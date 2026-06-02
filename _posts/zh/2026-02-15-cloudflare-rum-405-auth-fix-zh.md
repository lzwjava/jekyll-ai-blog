---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Cloudflare RUM 405 身份验证错误
translated: true
type: note
---

**Question:** 当尝试获取 RUM sites 时遇到以下错误是什么意思，以及如何修复：Exit code 1, Error fetching RUM sites: 405 {"success":false,"errors":[{"code":10405,"message":"Method not allowed for this authentication scheme"}],"messages":[],"result":null}, No Web Analytics sites found?

**Answer:**

当调用 Cloudflare API 端点（在本例中，可能是 RUM/Web Analytics 管理端点，如 `/accounts/{account_id}/rum/site_info`）时，如果使用的 **API Token** 以及身份验证 Header 与所使用的 HTTP method 不兼容，就会出现此错误。

核心部分在于：
**"Method not allowed for this authentication scheme" (code 10405)**
这是一个 Cloudflare 特有的错误，表明身份验证方式（发送凭据的方式）不支持你请求的 HTTP method（例如 GET, POST, DELETE, PATCH）。

### 常见原因

1. 使用了 **API Token** 身份验证（通过 `Authorization: Bearer <token>`），但该端点或方法在某些操作上并不完全支持它。
   一些较旧或特定的端点（包括部分 RUM/Web Analytics 端点）历史上对 **Global API Key**（通过 `X-Auth-Email` + `X-Auth-Key` Header）的支持比 Scoped API Tokens 更好、更一致。

2. 端点使用了错误的 HTTP method。
   - List sites: 必须是 **GET**
   - Create site: **POST**
   - Delete/Update: **DELETE** / **PATCH** / **PUT**
   如果你在查询列表时误用了 POST，或者在创建时误用了 GET，就会收到 405 错误。

3. Token 缺少必要的 **Edit** 权限（尽管这通常会导致 403 Forbidden 或 10000 身份验证错误，而不是特定的 10405）。

4. 罕见情况：端点本身对非 GET 方法的 Token auth 有限制（在社区报告中，在各种 API 的 PATCH/PUT/DELETE 操作中见过此类情况）。

### 如何修复（分步指南）

1. **核实你使用的是正确的 HTTP method**
   获取 Web Analytics 站点列表（最常见的起点）：
   - Endpoint: `GET https://api.cloudflare.com/client/v4/accounts/{account_id}/rum/site_info`
   - **不要**在获取列表时使用 POST/PATCH 等。

2. **切换到 Global API Key 身份验证**（这是解决 RUM 相关端点此错误的最高效方案）
   - 前往 Cloudflare Dashboard → **My Profile** → **API Tokens** 选项卡 → 滚动到 **Global API Key** 部分 → 查看/生成。
   - 在请求中使用以下 Header（而不是 Bearer token）：

     ```
     X-Auth-Email: your@email.com
     X-Auth-Key: YOUR_GLOBAL_API_KEY_HERE
     ```

   - 获取站点列表的 curl 示例：

     ```bash
     curl -X GET "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/rum/site_info" \
     -H "X-Auth-Email: your@email.com" \
     -H "X-Auth-Key: YOUR_GLOBAL_API_KEY_HERE" \
     -H "Content-Type: application/json"
     ```

   - 这通常能解决较旧或 Legacy 风格端点的 “authentication scheme” 不匹配问题。

3. **如果必须使用 API Token (Bearer auth)**
   - 确保 Token 拥有 **Account → Web Analytics: Edit** 权限。
   - 再次检查获取列表时是否使用的是 **GET**。
   - 先测试简单的 GET 请求。一些用户报告称，在使用 Bearer 时，即便权限正确，RUM 端点上的非 GET 方法（POST/DELETE/PATCH）仍会抛出 10405 错误 —— 在这种情况下，请退而使用 Global Key。
   - 重新生成 Token 并重试。

4. **其他检查**
   - 确认 **Account ID** 正确（在 Dashboard 的 Overview 侧边栏可以找到）。
   - 如果尚未存在任何站点 → 结果将是空数组，但 success 会是 true（不会报这个错）。
   - 使用 Postman 或带有 `-v` 参数的 curl 查看完整的 Response Headers（留意列出允许方法的 `Allow:` Header）。

总结：最快的修复方法通常是**切换到 Global API Key + X-Auth-* Header** 来替代 Bearer token，特别是对于 RUM/Web Analytics 管理类的 API 调用。这可以绕过在某些方法/端点上出现的身份验证方案限制。

**References:**

- [Cloudflare Community - PATCH method not allowed for the api_token authentication scheme](https://community.cloudflare.com/t/patch-method-not-allowed-for-the-api-token-authentication-scheme/505411)
- [Cloudflare Community - PUT method not allowed for the api_token authentication scheme](https://community.cloudflare.com/t/put-method-not-allowed-for-the-api-token-authentication-scheme/381292)
- [Cloudflare API Authentication - Headers reference](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [Cloudflare Community - 405 response in RUM Rules API (similar auth scheme issue)](https://community.cloudflare.com/t/405-response-in-rum-rules-api/876646)
