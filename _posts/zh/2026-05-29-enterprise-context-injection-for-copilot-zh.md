---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向Copilot的企业上下文注入
translated: true
type: note
---

**问题：** 在企业环境中，我们能否向 Copilot 提供数据库 Python 示例代码，并从前端复制缓存/授权 HTTP 标头，以帮助它修复后端代码？

**回答：**

是的，这是在企业代码库中获得良好 Copilot 输出的标准“上下文注入”模式。以下是完整的思维模型以及如何有效执行：

## 核心思想：上下文 = 输出质量

Copilot（以及任何 LLM 编码助手）的好坏取决于你提供的上下文窗口。在模型未针对内部代码库进行微调的企业环境中，你必须**手动注入相关上下文**。

## 注入什么以及如何注入

### 1. 数据库代码示例

将实际的 ORM/查询模式粘贴为行内注释或在同一文件中：

```python
# === 上下文：我们的数据库模式（SQLAlchemy + 连接池） ===
# from app.db import get_session
# async with get_session() as session:
#     result = await session.execute(
#         select(User).where(User.id == user_id)
#     )
#     return result.scalar_one_or_none()

# === 修复此代码： ===
def get_user_trades(user_id: str):
    # TODO: 查询有 bug，未正确使用异步会话
    conn = db.connect()
    return conn.execute(f"SELECT * FROM trades WHERE user_id = {user_id}")
```

Copilot 将根据上述示例进行模式匹配，并使用你的内部约定（异步会话、参数化查询等）修复有问题的代码。

### 2. 来自前端的授权标头

这是一个关键技巧。从浏览器 DevTools 网络选项卡复制实际的 `Authorization` / 缓存标头，并将其粘贴为注释块：

```python
# === 上下文：前端发送这些标头（来自 DevTools） ===
# Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
# X-Cache-Control: no-store
# X-Request-ID: 8f3a1b2c-...
# X-User-Context: {"role": "trader", "region": "APAC", "desk": "FX"}
#
# JWT 负载解码为：
# { "sub": "u_12345", "roles": ["TRADER"], "exp": 1234567890 }

# === 修复此代码：中间件未正确提取角色 ===
def extract_user_roles(request: Request) -> list[str]:
    token = request.headers.get("Authorization", "").split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get("role")  # BUG：应该是 "roles"（列表）
```

现在 Copilot 知道了确切的 JWT 结构、标头名称和字段类型——它可以精确地修复 bug。

### 3. 完整上下文块模式

对于复杂修复，在文件顶部创建一个结构化的上下文注释：

```python
# === 企业上下文块 ===
# 技术栈：FastAPI + SQLAlchemy async + Redis cache + Azure AD JWT
#
# 认证流程：
#   1. 前端从 Azure AD 获取令牌（RS256）
#   2. 发送：Authorization: Bearer <token>
#   3. 后端通过 JWKS 端点验证
#   4. 从声明中提取：sub、roles、desk、region
#
# 数据库会话模式：（参见 app/db/session.py）
#   async with AsyncSessionLocal() as session:
#       async with session.begin():
#           ...
#
# 缓存模式：
#   cache_key = f"user:{user_id}:positions"
#   ttl = 300  # 5 分钟
#
# 工作示例端点：GET /api/v1/positions（positions.py:L45）
# ================================
```

## 后端修复的实际工作流程

```
1. 在 VS Code / Copilot Chat 中打开有问题的后端文件
2. 粘贴：来自类似端点的正常数据库示例
3. 粘贴：来自 DevTools 的实际标头（对敏感值进行脱敏处理）
4. 粘贴：解码后的 JWT 负载结构
5. 提问：“修复此函数，使其符合上述模式”
```

在 **Copilot Chat**（侧边栏）中，你还可以使用 `#file:positions.py` 引用自动从其他文件中拉取工作示例——比手动复制粘贴更好。

## 安全注意事项（企业环境）

- **切勿将带有有效签名的真实 JWT 粘贴到 Copilot 中**——它们是实时凭据。先解码负载，对签名进行脱敏，或使用过期令牌。
- 检查你的企业是否启用了 `github.copilot.chat.codeGeneration.useInstructionFiles`——你可以创建一个包含数据库/认证模式的 `.github/copilot-instructions.md` 文件，这样就不必每次会话都重复操作。
- 某些银行完全阻止 Copilot 遥测——请确认你的实例是企业隔离版，而非消费者端点。

## `.github/copilot-instructions.md`——永久上下文

```markdown
## 数据库模式
始终通过 `get_async_session()` 使用异步 SQLAlchemy 会话。
绝不使用原始 SQL 字符串——使用 ORM 或带绑定参数的 `text()`。

## 认证模式
JWT 来自 Azure AD，使用 RS256 算法。声明：sub、roles（列表）、desk、region。
通过 `request.state.user` 提取（由 AuthMiddleware 设置）。

## 缓存模式
通过 `app.cache.get_client()` 使用 Redis。键格式：`{entity}:{id}:{field}`。默认 TTL：300 秒。
```

该文件会自动注入到每个 Copilot 会话中。

---

你所描述的模式基本上是**通过代码上下文进行少量样本提示**——这与让 GPT-4 擅长上下文学习的机制相同，只是应用于编码助手。你的上下文越精确地匹配内部约定，产生的幻觉就越少。
