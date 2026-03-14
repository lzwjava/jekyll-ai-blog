---
audio: false
generated: true
image: false
lang: en
layout: post
title: PinCC Blocks Non-Claude Code Clients Fix
translated: false
type: note
---

Question: After configuring OpenClaw to use the PinCC relay (`https://v2-as.pincc.ai/`), why does it return `HTTP 503 api_error: No available accounts: this group only allows Claude Code clients`? How do I fix it?

Answer:

## Root Cause: This Is a PinCC Server-Side Restriction, Not an OpenClaw Config Error

This error does **not** come from OpenClaw's configuration being wrong. It comes from the **PinCC relay server itself**, which is actively checking whether the incoming request looks like it came from the official Claude Code CLI.

In January 2026, Anthropic deployed strict new technical safeguards blocking subscription OAuth tokens from working outside their official Claude Code CLI. The error message `"This credential is only authorized for use with Claude Code"` (or variants like `"this group only allows Claude Code clients"`) is the gate Anthropic and relay operators put up to enforce this.

Tools like OpenCode and third-party harnesses had been working by presenting themselves to Anthropic's servers as the legitimate Claude Code client — mimicking headers or client identifiers associated with Anthropic's own CLI. Anthropic's new checks severed that connection.

In the PinCC relay's case: the relay itself is built on **Claude Code Max subscription accounts** (carpool/shared seats). PinCC's carpool service works by sharing Claude Code Max subscription costs across multiple users. Because those accounts use subscription OAuth tokens (not the paid API), the relay enforces that requests must **look like they come from Claude Code**, and rejects anything that doesn't pass its client check.

---

## What the Error Actually Means

| Term | Meaning |
|---|---|
| `No available accounts` | No relay backend account accepted this request |
| `this group only allows Claude Code clients` | The PinCC group you're using specifically requires the `User-Agent` (or equivalent headers) to identify as the official Claude Code CLI |

---

## Your Options to Fix This

### Option A — Add Claude Code Client Headers in OpenClaw (May Work)

The relay checks headers to decide if a request is from Claude Code. You need OpenClaw to send the correct `User-Agent` that matches what the official `claude-code` CLI sends. Look for a `headers` or `extraHeaders` field in your OpenClaw provider config:

```json
"pincc-claude": {
  "baseUrl": "https://v2-as.pincc.ai",
  "apiKey": "YOUR_PINCC_TOKEN_HERE",
  "api": "anthropic-messages",
  "authHeader": true,
  "extraHeaders": {
    "User-Agent": "claude-code/1.0",
    "anthropic-version": "2023-06-01"
  },
  ...
}
```

> **Note:** The exact `User-Agent` string that PinCC requires may differ. Check PinCC's documentation or their Telegram/Discord support group for the current accepted value.

---

### Option B — Use the Official Claude Code CLI as a Proxy (Recommended)

Since the PinCC relay is designed exclusively for Claude Code, the correct workflow is:

1. Install the official Claude Code CLI
2. Point it at the PinCC relay via environment variables:

```bash
export ANTHROPIC_BASE_URL="https://v2-as.pincc.ai"
export ANTHROPIC_AUTH_TOKEN="YOUR_PINCC_TOKEN_HERE"
```

3. Then run Claude Code normally — it will use the relay transparently.

This bypasses the client-check entirely because you're using the actual official client.

---

### Option C — Switch to an API-Key-Based Relay (Best Long-Term Fix)

By blocking third-party harnesses, Anthropic is forcing high-volume automation toward two sanctioned paths: the Commercial API (metered, per-token pricing) and the official Claude Code environment.

The PinCC relay's "Claude Code clients only" groups are built on **subscription OAuth** accounts, which inherently carry this restriction. If you want to use OpenClaw freely, you should use a relay group or provider backed by **Anthropic API keys** (not subscription accounts):

- **OpenRouter** — Already works with OpenClaw, uses real API keys, no client-check issues
- **A different PinCC group** — PinCC may offer API-key-backed groups; contact their support to ask
- **Direct Anthropic API** — Configure OpenClaw with `api.anthropic.com` directly using a paid API key

---

## Summary

| Fix | Effort | Reliability |
|---|---|---|
| Add correct `User-Agent` headers in OpenClaw | Low | Uncertain — may break again if PinCC updates checks |
| Use official Claude Code CLI with PinCC relay | Medium | High — that's what PinCC is designed for |
| Switch to OpenRouter or API-key-backed provider | Low | High — no client-check restrictions at all |

**Bottom line:** The PinCC relay groups marked "Claude Code clients only" are not designed for use with third-party clients like OpenClaw. Either configure OpenClaw to send the correct Claude Code headers, use the official CLI, or switch to an API-key-based provider like OpenRouter which has no such restrictions.

References:

- [Anthropic's Walled Garden: The Claude Code Crackdown (paddo.dev)](https://paddo.dev/blog/anthropic-walled-garden-crackdown/)
- [Anthropic cracks down on unauthorized Claude usage (VentureBeat)](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses)
- [Anthropic Tightens Control Over Claude Code Access (techbuddies.io)](https://www.techbuddies.io/2026/01/12/anthropic-tightens-control-over-claude-code-access-disrupting-third-party-harnesses-and-rival-labs/)
- [PinCC Carpool Service](https://pincc.ai/en/join-carpool)
- [PinCC Claude Code Installation Guide](https://pincc.ai/en/claude-code-install)