---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Claude Code Billing Header
translated: false
type: note
---

Question: What does `"CLAUDE_CODE_ATTRIBUTION_HEADER": "0"` mean in Claude Code's `settings.json`?

Answer:Question: What does `"CLAUDE_CODE_ATTRIBUTION_HEADER": "0"` mean in Claude Code's `settings.json`?

Answer:

## What `CLAUDE_CODE_ATTRIBUTION_HEADER` Actually Is

This is an **undocumented but real environment variable** that controls whether Claude Code sends a special billing/tracking header called `x-anthropic-billing-header` with every API request.

### What the Header Looks Like

Starting with Claude Code version 2.1.36, Claude Code sends a special header that changes with every request. It looks like:

```
x-anthropic-billing-header: cc_version=xxxx; cc_entrypoint=cli; cch=xxxx;...
```

### What the Header Is For

By default, Claude Code sends this billing attribution header — `x-anthropic-billing-header` — with every single request. When you're hitting Anthropic's actual API, this makes sense: they need to track usage. But when you're pointing Claude Code at a local model or a relay proxy, that header still goes out, and your server has to process it — overhead on every request, for zero benefit.

### What Setting It to `"0"` Does

When `CLAUDE_CODE_ATTRIBUTION_HEADER` is set to `0` in the env, Claude Code stops sending this header.

### Why This Matters for Your PinCC Setup

This is **directly relevant to your situation**. The `x-anthropic-billing-header` sent by Claude Code contains values that change with every request (like a session hash `cch=xxxx`). This causes two problems when using a relay:

1. **Breaks prompt caching** — because the header changes every request, the relay/Anthropic backend sees each request as unique and cannot reuse the cache, making responses slower and more expensive.
2. **May trigger client verification checks** — the relay may inspect this header as part of its "is this really Claude Code?" check. A malformed or unexpected value could contribute to the `503 only allows Claude Code clients` error.

### How to Set It in `settings.json`

Place it inside the `env` block:

```json
{
  "env": {
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0"
  }
}
```

This is the correct way to set environment variables persistently in Claude Code's `settings.json`, rather than using shell exports.

### Summary Table

| Value | Behaviour |
|---|---|
| Not set (default) | Claude Code sends `x-anthropic-billing-header` with every request (changes per-request) |
| `"0"` | Claude Code suppresses the header entirely — no billing attribution sent |

### Recommendation for Your PinCC Setup

Add this to your `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0",
    "ANTHROPIC_BASE_URL": "https://v2-as.pincc.ai",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_PINCC_TOKEN_HERE"
  }
}
```

This suppresses the dynamic billing header, which helps with both prompt cache stability and avoids sending unexpected header content to the relay. It will not affect Claude Code's core functionality when used with the official Claude Code CLI pointed at PinCC.

References:

- [Fix: use CLAUDE_CODE_ATTRIBUTION_HEADER to avoid breaking cache — claude-code-router PR #1220](https://github.com/musistudio/claude-code-router/pull/1220)
- [I Made Claude Code 3× Faster With Local Models — Medium/Coding Nexus](https://medium.com/coding-nexus/i-made-claude-code-3-faster-with-local-models-heres-the-one-env-variable-nobody-talks-about-7fd515eabe21)
- [Claude Code Settings Reference — claudefa.st](https://claudefa.st/blog/guide/settings-reference)
