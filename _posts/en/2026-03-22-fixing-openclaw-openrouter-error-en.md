---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenClaw OpenRouter API Key Error
translated: false
type: note
---

Question: What does this error mean and how do I fix it: "No API key found for provider 'openrouter'. Auth store: /root/.openclaw/agents/main/agent/auth-profiles.json"?

Answer:

This error comes from **OpenClaw**, an AI agent framework, and means it cannot find an API key configured for the **OpenRouter** provider. Here's what's happening and how to fix it:

## What's Going On

OpenClaw stores provider credentials in a JSON file at:
```
/root/.openclaw/agents/main/agent/auth-profiles.json
```

The agent tried to start but found no OpenRouter API key in that file, so it aborted before it could reply.

---

## How to Fix It

### Option 1: Use the OpenClaw CLI to add credentials (recommended)

```bash
openclaw agents add main
```

This command should prompt you to enter your OpenRouter API key interactively and save it to the auth profile.

### Option 2: Manually edit `auth-profiles.json`

1. Open the file:
   ```bash
   nano /root/.openclaw/agents/main/agent/auth-profiles.json
   ```

2. Add your OpenRouter key in the expected format (typically something like):
   ```json
   {
     "openrouter": {
       "api_key": "sk-or-..."
     }
   }
   ```
   *(The exact schema may vary — check OpenClaw's documentation for the correct structure.)*

3. Save and retry running the agent.

### Option 3: Copy auth from the main agent directory

The error message hints at this:
```bash
cp /root/.openclaw/agents/main/auth-profiles.json \
   /root/.openclaw/agents/main/agent/auth-profiles.json
```

Use this if you already configured credentials in the parent directory but they weren't propagated to the agent subdirectory.

---

## Getting an OpenRouter API Key

If you don't have one yet:

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign up or log in
3. Navigate to **Keys** in your account dashboard
4. Create a new key (starts with `sk-or-...`)

---

## Check the Logs

For more detail on the failure, run:
```bash
openclaw logs --follow
```

This may reveal additional context about what the agent was trying to do when it failed.
