---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codex Fixes Claude Proxy Smartly
translated: false
type: note
---

Question: How does using Codex to fix the Claude Code proxy issue work, and why is it a smart approach?

Answer:

Yes, that's a genuinely clever workaround! Here's why it's smart:

## The Core Problem

Claude Code **can't easily experiment on itself** — if you try to redirect its own `ANTHROPIC_BASE_URL` to a capture server mid-session, you break the very tool you're using to run the experiment. It's like trying to inspect your own brain while thinking.

## Why Codex Was the Right Tool

Codex (or any external agent) acts as an **independent operator** that can:

1. **Back up `~/.claude/settings.json`** before touching anything
2. **Redirect `ANTHROPIC_BASE_URL`** to your local `capture_server.py` temporarily
3. **Trigger `claude --print "Hello"`** as a subprocess — Claude Code runs normally, thinks it's talking to pincc.ai, but actually hits your capture server
4. **Restore the original settings** immediately after capture

```
Codex (orchestrator)
  ├── backup settings.json
  ├── patch settings → point to localhost:8080
  ├── run `claude --print "Hello"` → hits capture_server.py
  │       capture_server.py saves headers + 86KB body to captured_request.json
  ├── restore settings.json
  └── update try_pincc.py with exact captured payload → runs successfully ✓
```

## What Was Actually Discovered

The 86KB payload was the key insight — Claude Code doesn't just send a simple `{"model": ..., "messages": [...]}`. It sends a **massive internal context** including:

- Full system prompt with tool definitions
- Internal state and conversation history
- All `X-Stainless-*` headers (runtime environment fingerprinting)
- `?beta=true` URL parameter
- Specific `anthropic-beta` header value

The pincc.ai proxy likely **validates this payload structure** to confirm the request genuinely comes from Claude Code, not a simple script mimicking it.

## The Elegant Pattern

```
Problem: Tool X can't inspect its own traffic
Solution: Use Tool Y to orchestrate Tool X as a black box
          while intercepting at the network layer
```

This is a classic **MITM (Man-in-the-Middle) for debugging** pattern — and using Codex as the orchestrator instead of doing it manually saved a lot of back-and-forth. Smart engineering.
