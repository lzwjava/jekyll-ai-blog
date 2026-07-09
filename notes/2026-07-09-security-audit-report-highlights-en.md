---
audio: false
generated: true
image: false
lang: en
layout: post
title: Security Audit Report Highlights
translated: false
type: note
---

Now I have a thorough picture. Here's my analysis:

## Security Review of first-tree

I audited auth, crypto, scope guards, WS auth, webhook verification, config, and the OAuth flow. The codebase is **remarkably clean** for a monorepo of this size — the type-level scope enforcement and the route classification doc are novel patterns that kill entire bug classes at compile time. That said, there are real things to think about.

### 🔴 Medium-High: WebSocket token in query string — exposure in server logs & referer headers (`orgs/ws.ts:207`)

```
const token = (request.query as Record<string, string>).token;
```

The org admin WS (`/api/v1/orgs/:orgId/ws?token=...`) accepts the JWT as a **query parameter**. Query strings are:

- logged in full by Fastify's `req` serializer (and the `redactUrl` function in `logger.ts`)
- sent in the `Referer` header if the page links or redirects
- visible in browser history, bookmarks

There's a `redactUrl` utility that's supposed to redact JWTs in URLs, but the pattern of JWT-in-query-string is inherently leaky. Check whether `redactUrl` actually catches the `token=` param.

**Fix**: use `Sec-WebSocket-Protocol` subprotocol negotiation or a `Cookie` header instead — the WS `on upgrade` path carries HTTP headers.

### 🟡 Medium: XFF spoofing bypasses IP-based rate limiting (`app.ts:182-197`)

```ts
trustProxy: config.trustProxy,
```

When `trustProxy=true`, **any** upstream's `x-forwarded-for` is trusted — not just Cloudflare's. The boot log warns about it explicitly, but the rate limit key generator falls back to `req.ip` for unauthenticated requests (`app.ts:381`). If `trustProxy=true` and the container is directly exposed (bypassing Cloudflare), an attacker can spoof their IP and exhaust the per-IP rate limit bucket to mount a brute-force on `POST /auth/login` (which has its own separate limit of 5/min, but that's a sign it was considered).

The `.env.example` docs the warning. The logging-is-the-enforcement pattern is unusual — most apps would validate XFF sources.

### 🟡 Low-Medium: Auto-generated secrets on first boot (`server-config.ts:26-37`)

```ts
jwtSecret: field(z.string().min(1),
  { env: "FIRST_TREE_JWT_SECRET", auto: "random:base64url:32", ... }),
```

The config system auto-generates `jwtSecret` and `encryptionKey` on first boot if the env vars are unset and writes them to a local file. This is a nice UX for self-hosters, but it means:

- If two replicas boot simultaneously without the env var set, each generates a *different* secret — tokens signed by one are rejected by the other, and encrypted credentials can't be decrypted.
- If the file is lost, all active sessions are invalidated and all encrypted credentials (GitHub tokens) are unrecoverable.
- The `auto` field writes to disk behind `~/.first-tree/server.yaml`, not a secret store.

This is documented behaviour, but worth knowing.

### 🟢 Low: HMAC empty-key path guarded but worth noting (`server-config.ts:228-235`)

The comment explicitly calls out the empty-key forgery bug:

> The HMAC-empty-key forgery path [...] trips exactly when `webhookSecret` sneaks through as `""` — `createHmac("sha256", "")` is a valid hash any attacker can reproduce.

Every field in the GitHub app block has `.min(1)` so Zod rejects `""`. Good catch by whoever wrote this — most apps would miss this.

### 🟢 The good stuff — what's done right

1. **JWT carries ONLY `sub`** — no org/member/role in the JWT. The type system makes `request.user.organizationId` impossible at compile time (`scope/types.ts`). Every org check is a real-time DB probe. This kills the JWT-ambient-scope bug class (#220/#222/#238/#239) the doc references — a revoked membership takes effect immediately, no token invalidation needed.

2. **OAuth CSRF** — double-submit cookie + signed state JWT, with a nonce match. The comment on line 12-15 of `oauth-state.ts` correctly identifies the login-CSRF attack. The `/dev-callback` explicitly bypasses it (local dev only).

3. **Webhook HMAC** — timing-safe comparison (`timingSafeEqual`), `sha256` HMAC, raw body buffer (not parsed JSON, avoids re-serialization mismatch).

4. **AES-256-GCM** for credentials — proper 12-byte IV, 16-byte auth tag, random IV per encryption. No ECB, no static IV, authenticated encryption.

5. **Rate limiting** — per-user when authenticated (`req.user.userId`), per-agent when bound, per-IP fallback. Separate tighter limit (5/min) on login endpoint. Correct `hook: "preHandler"` after auth hooks populate identity.

6. **WS inbox backpressure** — per-agent + per-chat in-flight caps (8192/8), FIFO ACK queue, backlog batch limit (50), repair interval (30s). Prevents OOM from a slow-acking client.

7. **No SQL injection** — all DB queries use Drizzle ORM with parameterized queries (`eq`, `and`, `inArray`). No raw `sql` template literals found anywhere.

8. **No XSS in web** — no `dangerouslySetInnerHTML`, no `innerHTML` assignments.

9. **Body-capture only on error** — the `otelRecordBody` flag triggers body logging only on `statusCode >= 400`, so successful requests with plaintext passwords don't leak to the trace exporter.

### Summary

| Severity | Issue | File |
| --- | --- | --- |
| 🔴 Medium-High | JWT in WS query string, log/referer exposure | `orgs/ws.ts:207` |
| 🟡 Medium | XFF spoofing bypasses IP rate limits | `app.ts:182-197` |
| 🟡 Low-Medium | Auto-generated secrets lost on multi-replica | `server-config.ts:28-37` |
| 🟢 Low | Empty HMAC key (guarded) | `server-config.ts:228-235` |
| ✅ Strong | JWT scope, OAuth CSRF, AES-GCM, no SQL injection, no XSS | — |

The one I'd actually fix is the WS query-string JWT — that's a real exposure path that the rest of the codebase already avoids (HTTP auth uses `Authorization: Bearer`). Move it to a cookie or the `Sec-WebSocket-Protocol` header.
