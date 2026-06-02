---
audio: false
generated: true
image: false
lang: en
layout: post
title: CORS Blocks Custom Copilot API Calls
translated: false
type: note
---

Question: When calling `https://api.githubcopilot.com/chat/completions` via `fetch()` from a custom-built Copilot web portal (not the official `github.com/copilot` portal), will CORS issues occur?

Answer:

## Yes — You Will Hit CORS Issues

If you try to call `https://api.githubcopilot.com/chat/completions` directly from a **custom web portal** (i.e., a browser-based frontend on a different origin), you will almost certainly encounter a **CORS (Cross-Origin Resource Sharing) error**.

---

## Why CORS Happens Here

### 1. What CORS Is

CORS is a browser-enforced security mechanism that blocks requests from different origins unless explicitly allowed by the server. If the domain of the requester is different from the domain of the receiver, the browser will by default reject the request — even if it technically reaches the server. The browser will refuse to deliver the response to the client.

### 2. Why `api.githubcopilot.com` Blocks Custom Origins

The official GitHub Copilot web chat is hosted at `github.com/copilot/...`. GitHub's API servers are configured to only allow specific, trusted origins (like `github.com` itself) in the `Access-Control-Allow-Origin` response header.

When your custom web portal (e.g., `http://localhost:3000` or `https://mycustomapp.com`) sends a `fetch()` request to `https://api.githubcopilot.com/chat/completions`, the browser performs a **preflight OPTIONS request** first. If GitHub's server does not respond with an `Access-Control-Allow-Origin` that matches your custom origin, the browser will block the response entirely.

### 3. The Underlying Token Restriction

GitHub Copilot's API internals are only exposed to OAuth tokens from VSCode. The Copilot token endpoint requires a device-flow authentication tied to VSCode's own client ID. This means even if CORS were bypassed, getting a valid Copilot API token for a custom web portal is itself a significant barrier.

---

## The Official vs. Custom Portal Comparison

| Scenario | CORS Issue? |
|---|---|
| Official `github.com/copilot` portal | ❌ No — same origin as GitHub servers |
| Your own web frontend on any other domain | ✅ Yes — blocked by browser CORS policy |
| Server-side backend calling the API (Node.js, Python, etc.) | ❌ No — CORS only applies to browsers |

---

## How to Work Around It

Server-to-server requests (e.g., via Node.js) don't face CORS restrictions. The correct architectural solution is:

### ✅ Use a Backend Proxy (Recommended)

Build a **backend server** (Node.js, Python Flask, etc.) that:
1. Receives requests from your frontend
2. Forwards them to `api.githubcopilot.com`
3. Returns the response to your frontend

Your frontend calls **your own backend** (same origin or CORS-controlled by you), and your backend calls GitHub. Since CORS is browser-enforced only, the server-to-server call works freely.

```
Browser (Custom Portal)
    ↓  fetch("https://your-backend.com/api/chat")
Your Backend Server
    ↓  fetch("https://api.githubcopilot.com/chat/completions")
GitHub Copilot API
```

### ✅ Example: Open Source Proxy Projects

Projects like `copilot-api` (a reverse-engineered proxy) expose GitHub Copilot as an OpenAI-compatible API server, allowing tools to communicate with Copilot via a local proxy. However, note that excessive automated use may trigger GitHub's abuse detection systems.

---

## Summary

- Direct browser `fetch()` to `api.githubcopilot.com` from a custom domain **will fail with CORS**.
- This is **by design** — GitHub only allows its own origins.
- The only proper solution is to route requests **through a backend proxy** you control, which then calls GitHub's API server-to-server.

References:

- [CORS Error Explained — FreeCodeCamp](https://www.freecodecamp.org/news/how-to-fix-cross-origin-errors/)
- [copilot-api proxy project (GitHub)](https://github.com/ericc-ch/copilot-api)
- [GitHub Copilot Inside GitHub Actions — den.dev](https://den.dev/blog/github-copilot-inside-github-actions/)
- [I Turned GitHub Copilot into OpenAI API Compatible Provider — DEV](https://dev.to/ericc/i-turned-github-copilot-into-openai-api-compatible-provider-1fb8)
