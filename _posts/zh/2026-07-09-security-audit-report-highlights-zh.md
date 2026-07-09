---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安全审计报告亮点
translated: true
type: note
---

现在我有了全面的了解。以下是我的分析：

## 对 first-tree 的安全审查

我审计了认证、加密、作用域守卫、WebSocket 认证、Webhook 验证、配置以及 OAuth 流程。对于如此规模的单体仓库来说，代码库**非常干净**——类型级别的作用域强制和路由分类文档是新颖的模式，在编译时就能消除整类错误。不过，确实有一些需要关注的问题。

### 🔴 中高：WebSocket 令牌在查询字符串中——暴露在服务器日志和 Referer 头中（`orgs/ws.ts:207`）

```
const token = (request.query as Record<string, string>).token;
```

组织管理员 WebSocket（`/api/v1/orgs/:orgId/ws?token=...`）将 JWT 作为**查询参数**接受。查询字符串会：
- 被 Fastify 的 `req` 序列化器完整记录（以及 `logger.ts` 中的 `redactUrl` 函数）
- 如果页面链接或重定向，会通过 `Referer` 头发送
- 在浏览器历史记录和书签中可见

有一个 `redactUrl` 工具旨在隐藏 URL 中的 JWT，但 JWT 在查询字符串中的模式本质上是容易泄露的。需要检查 `redactUrl` 是否实际捕获了 `token=` 参数。

**修复**：使用 `Sec-WebSocket-Protocol` 子协议协商或 `Cookie` 头代替——WebSocket 的 `on upgrade` 路径会携带 HTTP 头。

### 🟡 中：XFF 伪造绕过基于 IP 的速率限制（`app.ts:182-197`）

```ts
trustProxy: config.trustProxy,
```

当 `trustProxy=true` 时，**任何**上游的 `x-forwarded-for` 都会被信任——而不仅仅是 Cloudflare 的。启动日志明确警告了这一点，但速率限制键生成器对未认证请求回退到 `req.ip`（`app.ts:381`）。如果 `trustProxy=true` 并且容器直接暴露（绕过 Cloudflare），攻击者可以伪造其 IP 来耗尽基于 IP 的速率限制桶，从而对 `POST /auth/login` 进行暴力破解（该端点本身有单独的 5 次/分钟限制，但这表明已经考虑过该问题）。

`.env.example` 文档中记录了此警告。这种“日志即执行”的模式并不常见——大多数应用会验证 XFF 来源。

### 🟡 低中：首次启动时自动生成密钥（`server-config.ts:26-37`）

```ts
jwtSecret: field(z.string().min(1),
  { env: "FIRST_TREE_JWT_SECRET", auto: "random:base64url:32", ... }),
```

如果环境变量未设置，配置系统会在首次启动时自动生成 `jwtSecret` 和 `encryptionKey`，并将其写入本地文件。这对自托管用户来说很友好，但意味着：
- 如果两个副本同时启动且未设置环境变量，每个副本会生成**不同**的密钥——一个副本签发的令牌会被另一个副本拒绝，且加密的凭据无法解密。
- 如果文件丢失，所有活跃会话失效，所有加密的凭据（GitHub 令牌）无法恢复。
- `auto` 字段写入磁盘的路径是 `~/.first-tree/server.yaml`，而不是密钥存储服务。

这是文档记录的行为，但值得注意。

### 🟢 低：HMAC 空密钥路径已防护，但值得提及（`server-config.ts:228-235`）

注释明确指出了空密钥伪造漏洞：

> HMAC 空密钥伪造路径 [...] 恰好在 `webhookSecret` 作为 `""` 传入时触发——`createHmac("sha256", "")` 是一个任何攻击者都能复现的有效哈希。

GitHub 应用块中的每个字段都有 `.min(1)`，因此 Zod 会拒绝 `""`。编写这段代码的人做得很好——大多数应用都会忽略这一点。

### 🟢 做得好的地方

1. **JWT 仅携带 `sub`**——JWT 中不包含组织/成员/角色信息。类型系统使得 `request.user.organizationId` 在编译时不可能出现（`scope/types.ts`）。每个组织检查都是实时数据库探测。这消除了文档中提到的 JWT 环境作用域漏洞类（#220/#222/#238/#239）——撤销成员资格会立即生效，无需令牌失效。

2. **OAuth CSRF**——双重提交 cookie + 签名状态 JWT，并带有 nonce 匹配。`oauth-state.ts` 第 12-15 行的注释正确指出了登录 CSRF 攻击。`/dev-callback` 明确绕过此检查（仅限本地开发）。

3. **Webhook HMAC**——时序安全比较（`timingSafeEqual`），`sha256` HMAC，原始请求体缓冲区（不解析 JSON，避免重新序列化不匹配）。

4. **AES-256-GCM** 加密凭据——正确的 12 字节 IV，16 字节认证标签，每次加密随机 IV。没有 ECB，没有静态 IV，认证加密。

5. **速率限制**——认证后按用户（`req.user.userId`），绑定后按代理，未认证时回退到 IP。登录端点有单独的更严格限制（5 次/分钟）。在认证钩子填充身份后正确使用 `hook: "preHandler"`。

6. **WebSocket 收件箱背压**——每个代理 + 每个聊天在途上限（8192/8），FIFO ACK 队列，积压批量限制（50），修复间隔（30 秒）。防止因慢速 ACK 客户端导致内存耗尽。

7. **无 SQL 注入**——所有数据库查询使用 Drizzle ORM 的参数化查询（`eq`、`and`、`inArray`）。未发现任何原始 `sql` 模板字面量。

8. **Web 中无 XSS**——无 `dangerouslySetInnerHTML`，无 `innerHTML` 赋值。

9. **仅在错误时捕获请求体**——`otelRecordBody` 标志仅在 `statusCode >= 400` 时触发请求体日志记录，因此成功请求中的明文密码不会泄露到追踪导出器。

### 总结

| 严重程度 | 问题 | 文件 |
|---|---|---|
| 🔴 中高 | WebSocket 查询字符串中的 JWT，日志/Referer 暴露 | `orgs/ws.ts:207` |
| 🟡 中 | XFF 伪造绕过 IP 速率限制 | `app.ts:182-197` |
| 🟡 低中 | 多副本时自动生成的密钥丢失 | `server-config.ts:28-37` |
| 🟢 低 | 空 HMAC 密钥（已防护） | `server-config.ts:228-235` |
| ✅ 强项 | JWT 作用域、OAuth CSRF、AES-GCM、无 SQL 注入、无 XSS | — |

我真正会修复的是 WebSocket 查询字符串中的 JWT——这是一个真正的暴露路径，代码库的其他部分已经避免了（HTTP 认证使用 `Authorization: Bearer`）。将其迁移到 cookie 或 `Sec-WebSocket-Protocol` 头中。