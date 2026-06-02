---
audio: false
generated: true
image: false
lang: en
layout: post
title: Never Share Passwords With AI
translated: false
type: note
---

**Question:** Is it safe to tell my password to OpenClaw, the AI agent?

**Answer:**

**No, it is not safe.**

You should **never** tell your real password (or any authentication credentials) to **any** AI agent / chatbot / assistant / "helper AI", including OpenClaw or any similar tool.

### Why it's dangerous

- Almost all AI agents (including ones advertised as very capable or "fully autonomous") **save/log** at least part of the conversation.
- Many of them send your messages to third-party cloud providers (OpenAI, Anthropic, Google, xAI, Fireworks, Groq, DeepSeek, etc.).
- Developers, safety teams, or contractors often have access to conversations for debugging and training purposes.
- Even when a project claims "we don't store logs" — these promises are frequently broken later (either by accident, by insiders, or after the company gets acquired).
- Once your password is said/written once, you can basically never be sure where all the copies are.

### Realistic risk levels

| Situation                                 | Realistic risk level       | Should you do it? |
|-------------------------------------------|----------------------------|-------------------|
| Telling password to ChatGPT/Claude/Gemini | High                       | No                |
| Telling password to any open-source local model you personally run | Very low (if truly local) | Still avoid       |
| Telling password to any cloud-based "agent" (OpenClaw, Manus, AgentX, etc.) | High → Very high           | No                |
| Telling password because "it's just for one API call" / "temporary token" | Still high                 | No                |

### What you can do instead (safer alternatives)

- Give the **API key** with very low permissions (if the service supports scoped/project keys)
- Use temporary / short-lived tokens when possible
- Create a **dedicated test account** with almost no real data
- Use environment variables / secret managers instead of pasting secrets
- If the agent really needs to log into your account → do the login yourself manually in a browser and give the agent the **session cookie** (still risky, but usually less bad than password)

**Short rule of thumb most security people follow in 2025–2026:**

If the AI can see your password → assume it (and probably several other parties) can **permanently** see your password.

So: **just don't do it.**

References:

- None required for this general security advice.
