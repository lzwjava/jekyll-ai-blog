---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enterprise Context Injection for Copilot
translated: false
type: note
---

**Question:** In enterprise environments, can we provide Copilot with example database Python code and copy cache/authorization HTTP headers from the frontend to help it fix backend code?

**Answer:**

Yes, this is a standard "context injection" pattern for getting good Copilot output in enterprise codebases. Here's the full mental model and how to do it effectively:

## The Core Idea: Context = Output Quality

Copilot (and any LLM coding assistant) is only as good as the context window you feed it. In enterprise environments where models aren't fine-tuned on your internal codebase, you have to **manually inject relevant context**.

## What to Inject and How

### 1. Database Code Examples

Paste your actual ORM/query patterns as inline comments or in the same file:

```python
# === CONTEXT: Our DB pattern (SQLAlchemy + connection pool) ===
# from app.db import get_session
# async with get_session() as session:
#     result = await session.execute(
#         select(User).where(User.id == user_id)
#     )
#     return result.scalar_one_or_none()

# === FIX THIS: ===
def get_user_trades(user_id: str):
    # TODO: broken query, not using async session correctly
    conn = db.connect()
    return conn.execute(f"SELECT * FROM trades WHERE user_id = {user_id}")
```

Copilot will pattern-match from the example above and fix the broken code using your internal conventions — async session, parameterized queries, etc.

### 2. Authorization Headers from Frontend

This is the key trick. Copy the actual `Authorization` / cache headers from browser DevTools Network tab and paste them as a comment block:

```python
# === CONTEXT: Frontend sends these headers (from DevTools) ===
# Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
# X-Cache-Control: no-store
# X-Request-ID: 8f3a1b2c-...
# X-User-Context: {"role": "trader", "region": "APAC", "desk": "FX"}
#
# JWT payload decodes to:
# { "sub": "u_12345", "roles": ["TRADER"], "exp": 1234567890 }

# === FIX THIS: middleware isn't extracting roles correctly ===
def extract_user_roles(request: Request) -> list[str]:
    token = request.headers.get("Authorization", "").split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get("role")  # BUG: should be "roles" (list)
```

Now Copilot knows the exact JWT structure, header names, and field types — it can fix the bug precisely.

### 3. Full Context Block Pattern

For complex fixes, create a structured context comment at the top of the file:

```python
# === ENTERPRISE CONTEXT BLOCK ===
# Stack: FastAPI + SQLAlchemy async + Redis cache + Azure AD JWT
#
# Auth flow:
#   1. Frontend gets token from Azure AD (RS256)
#   2. Sends: Authorization: Bearer <token>
#   3. Backend validates via JWKS endpoint
#   4. Extracts: sub, roles, desk, region from claims
#
# DB session pattern: (see app/db/session.py)
#   async with AsyncSessionLocal() as session:
#       async with session.begin():
#           ...
#
# Cache pattern:
#   cache_key = f"user:{user_id}:positions"
#   ttl = 300  # 5 min
#
# Example working endpoint: GET /api/v1/positions (positions.py:L45)
# ================================
```

## Practical Workflow for Backend Fixes

```
1. Open broken backend file in VS Code / Copilot Chat
2. Paste: working DB example from similar endpoint
3. Paste: actual headers from DevTools (redact sensitive values)
4. Paste: decoded JWT payload structure
5. Ask: "Fix this function to match the patterns above"
```

In **Copilot Chat** (the sidebar), you can also use `#file:positions.py` references to pull in working examples from other files automatically — better than manual copy-paste.

## Security Caveat (Enterprise)

- **Never paste real JWTs** with valid signatures into Copilot — they're live credentials. Decode the payload, redact the signature, or use an expired token.
- Check if your enterprise has `github.copilot.chat.codeGeneration.useInstructionFiles` enabled — you can put a `.github/copilot-instructions.md` with your DB/auth patterns permanently so you don't have to repeat this every session.
- Some banks block Copilot telemetry entirely — verify your instance is the enterprise-isolated one, not the consumer endpoint.

## `.github/copilot-instructions.md` — Permanent Context

```markdown
## Database Pattern
Always use async SQLAlchemy sessions via `get_async_session()`.
Never use raw SQL strings — use ORM or `text()` with bound params.

## Auth Pattern
JWT from Azure AD, RS256. Claims: sub, roles (list), desk, region.
Extract via `request.state.user` (set by AuthMiddleware).

## Cache Pattern
Redis via `app.cache.get_client()`. Keys: `{entity}:{id}:{field}`. TTL: 300s default.
```

This gets injected into every Copilot session automatically.

---

The pattern you're describing is basically **few-shot prompting via code context** — the same mechanism that makes GPT-4 good at in-context learning, just applied to a coding assistant. The more precisely your context matches your internal conventions, the less hallucination you get.
