---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenCode GitHub Copilot Integration Details
translated: false
type: note
---

Yes — OpenCode has first-class GitHub Copilot support with web login (device-code OAuth flow).

Here's what I found from the source code:

**Provider ID**: `github-copilot` (registered in `packages/core/src/provider.ts`)

**Auth flow**: OAuth device-code flow (RFC 8628), implemented in `packages/opencode/src/plugin/github-copilot/copilot.ts`:

1. You select "Login with GitHub Copilot" in OpenCode
2. Choose deployment type: GitHub.com or GitHub Enterprise
3. OpenCode hits `https://github.com/login/device/code` with client_id `Ov23li8tweQw6odWQebz`
4. You get a user code + verification URL (https://github.com/login/device)
5. You enter the code in your browser, authorize
6. OpenCode polls `https://github.com/login/oauth/access_token` until it gets an access token
7. Token is used as Bearer auth for all Copilot API calls

**API endpoint**: `https://api.githubcopilot.com` (or `https://copilot-api.<your-ghe-domain>` for Enterprise)

**What it supports**:
- Chat completions API and OpenAI Responses API
- Vision requests (images)
- Agent mode (auto-detected via `x-initiator` header)
- Reasoning/thinking (via `reasoning_opaque` field)
- Model list fetched dynamically from Copilot API
- GitHub Enterprise with custom URL

**How to use it**:
```
# In OpenCode TUI, go to provider settings
# Select "github-copilot" -> "Login with GitHub Copilot"
# Choose GitHub.com or Enterprise
# Enter the device code at github.com/login/device
```

No API key needed — it's your existing GitHub Copilot subscription (individual, business, or enterprise). The auth token gets stored locally by OpenCode's account system.