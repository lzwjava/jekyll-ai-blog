---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Proxy Errors and Fixes
translated: false
type: note
---

Question: Why does the custom Claude API proxy return a "400 Bad Request" error saying the interface is only for Claude Code clients, and why do subsequent attempts fail with missing credentials or wrong API key?

Answer:

## Root Cause Analysis

You're hitting **three separate issues** in sequence. Let me break them down:

---

### Issue 1: Proxy Rejects Your Request (400 Bad Request)

```
默认渠道限制: 请求非法 接口仅可用于Claude Code客户端
(如误判请修改CC客户端版本 其他渠道不限)
```

**Translation:** "Default channel restriction: illegal request. This interface can only be used by Claude Code clients."

**Why it happens:**

The proxy at `https://claude2.sssaicode.com/api` is a **third-party API reseller/relay**. It inspects the HTTP request headers to verify the caller is a legitimate Claude Code client. It checks headers like:

- `User-Agent` — must look like the official Claude Code CLI
- `anthropic-version`
- `x-api-key` format or token type

Your custom `claw` tool doesn't send the right headers to pass this check.

**Fix:** The error message itself hints at the solution — *"如误判请修改CC客户端版本"* meaning "if incorrectly flagged, modify the CC client version." You need to set your client's `User-Agent` or version header to match what official Claude Code sends.

---

### Issue 2: Missing Credentials (after you unset the env var)

```
error: missing Anthropic credentials; export ANTHROPIC_AUTH_TOKEN or ANTHROPIC_API_KEY
```

This happened because your second attempt ran **after the `export ANTHROPIC_API_KEY=` command** — which set the key to an **empty string**, and then your shell session may have lost it. The tool correctly complained about missing credentials.

---

### Issue 3: Wrong API Key for OpenAI (401 Unauthorized)

```
Incorrect API key provided: 999VUv4m**...8MZq
```

When you switched to `--model openai/gpt-4.1-mini`, the tool correctly routed to OpenAI's API — but it used your `OPENAI_API_KEY` which is **invalid or expired** on OpenAI's platform directly. The key `999VUv4m...` is likely a key issued by the proxy/reseller, not a real OpenAI key.

---

## Summary Table

| Error | Cause | Fix |
|---|---|---|
| 400 from proxy | `claw` doesn't send Claude Code client headers | Add correct `User-Agent` / client version header |
| Missing credentials | `ANTHROPIC_API_KEY` was set to empty | Re-export a valid key |
| 401 from OpenAI | `OPENAI_API_KEY` is a proxy key, not a real OpenAI key | Set `OPENAI_BASE_URL` to the proxy's OpenAI-compatible endpoint |

---

## Recommended Fix

If the proxy supports an OpenAI-compatible endpoint, try:

```bash
export OPENAI_API_KEY=<your-proxy-key>
export OPENAI_BASE_URL="https://claude2.sssaicode.com/api"   # or its openai-compat path
./target/debug/claw prompt "say hello" --model openai/claude-opus-4-6
```

Or, if you want to use it as an Anthropic endpoint, you need to make `claw` send headers that mimic the official Claude Code client — specifically the correct `User-Agent` and possibly an `x-claude-code-version` header.