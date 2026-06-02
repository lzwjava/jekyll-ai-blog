---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Fixing LibreChat OpenRouter Web Search Error
translated: false
type: note
---

The error **"404 No endpoints found that support tool use"** when using the web search function in LibreChat with OpenRouter is a known issue. Here’s what’s happening and how to fix it:

---

## **Why This Happens**
- **Not all models on OpenRouter support "tool use" (like web search, function calling, etc.)**—only a subset do. If you select a model that doesn’t support tools, you’ll get this 404 error.
- OpenRouter requires you to **explicitly choose a model that supports tool/function calling** for features like web search to work.
- LibreChat’s configuration may also override endpoints if not set up correctly, leading to routing issues.

---

## **How to Fix It**

### 1. **Select a Model That Supports Tools**
- Go to [OpenRouter’s model list](https://openrouter.ai/models) and **filter by "tools"** in the sidebar. Only models with tool support will work with LibreChat’s web search function.
- Recommended models: Look for those labeled as supporting "function calling" or "tools" (e.g., some versions of GPT-4, Claude, or other advanced models).

### 2. **Update LibreChat Configuration**
- **Do not use `OPENROUTER_API_KEY`** in your LibreChat config, as it may override the OpenAI endpoint and cause conflicts.
- In `librechat.yaml`, ensure your OpenRouter endpoint is correctly configured and not blocked by "Ignored Providers" or restricted by "Allowed Providers".

### 3. **Clear Provider Restrictions**
- In OpenRouter settings, **unblock all "Ignored Providers"** and **clear "Allowed Providers"** to ensure LibreChat can access all available endpoints.

### 4. **Restart LibreChat**
- After making these changes, restart LibreChat to apply the new settings.

---

## **Still Not Working?**
- Check the [LibreChat docs on custom endpoints](https://www.librechat.ai/docs/quick_start/custom_endpoints) for advanced setup.
- If the issue persists, try switching to the official OpenAI API (if you have access) or another provider that supports tool use
