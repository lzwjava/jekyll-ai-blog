---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wrangler 10000 Error Requires Read Scopes
translated: false
type: note
---

Question: Does Wrangler's `code: 10000` auth error on `/workers/services/...` require read scopes, not just edit?

Answer: Yes. Code 10000 is a generic catch-all — Cloudflare doesn't tell you *which* permission is missing, so it usually isn't the Workers Edit permission itself, it's a missing read-level scope that Wrangler needs just to bootstrap the session before it even gets to the deploy call.

Minimum working scope set for a custom API token used by Wrangler:

```
Account Settings: Read     ← wrangler calls /accounts to resolve account_id
User Details: Read         ← wrangler calls /user to fetch email on login
Workers Scripts: Edit      ← actual deploy permission
Workers Routes: Edit       (if you use routes)
Workers KV Storage: Edit   (if you bind KV)
```

`User Details: Read` is the most commonly missed one — there's a known Wrangler bug/behavior where it silently fails auth with `10000` instead of surfacing the actual "Are you missing the User->User Details->Read permission?" warning when that scope is absent, especially in CI/non-interactive environments where the warning gets swallowed.

Quick way to check what your token actually has vs what it needs:

```bash
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer <CLOUDFLARE_API_TOKEN>" | jq
```

If that 200s but Wrangler still 10000s specifically on `/workers/services/...`, it's almost always missing `Account Settings:Read` or `User Details:Read` — not the Workers edit scope, which you clearly already have since you're hitting the specific service endpoint at all.

Fastest fix — don't hand-pick scopes, use Cloudflare's own template which bundles the read+write set correctly:

```
Dashboard → My Profile → API Tokens → Create Token
→ "Edit Cloudflare Workers" template
```

This template includes Account:Read, User:Read, Workers Scripts:Edit, Workers Routes:Edit, Workers KV:Edit, Zone:Read — confirmed by other users who hit the same 10000 error and fixed it by switching from a manually-scoped token to the "Edit Cloudflare Workers" template.

References:

- [GitHub issue #2611 - custom token 10000](https://github.com/cloudflare/wrangler2/issues/2611)
- [Cloudflare Community - Wrangler Deploy 10000, fixed via template](https://community.cloudflare.com/t/wrangler-deploy-workflows-10000-error/827149)
- [Cloudflare Community - Authentication 10000](https://community.cloudflare.com/t/authentication-10000/821086)
