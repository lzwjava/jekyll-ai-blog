---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Fixing LibreChat OpenRouter Model Error
translated: false
type: note
---

This error occurs when using **LibreChat** with **OpenRouter** as the backend, and the selected model (`gpt-5-chat` or similar) is not available or not properly routed. Here’s a breakdown of the issue and how to resolve it:

---

## **Why This Error Happens**
- **OpenRouter** acts as a proxy to various AI models, but not all models are available or enabled by default.
- The error `404 No endpoints found that support tool use` means the model you selected (`gpt-5-chat`) is either:
  - Not supported by OpenRouter.
  - Not configured in your LibreChat setup.
  - Requires a different provider or API key.

---

## **How to Fix It**

### 1. **Check Available Models in OpenRouter**
- Visit [OpenRouter’s model list](https://openrouter.ai/models) to see which models are available.
- As of now, `gpt-5-chat` is not an official OpenAI model (the latest is GPT-4o). If you meant GPT-4, use `openai/gpt-4` or similar.

### 2. **Update LibreChat Configuration**
- In LibreChat, go to **Settings** > **Model Selection**.
- Choose a model that is **supported by OpenRouter** (e.g., `openai/gpt-4`, `mistralai/mistral-7b`, etc.).
- If you want to use OpenAI directly, switch the **API Provider** to **OpenAI** instead of OpenRouter.

### 3. **Verify API Keys**
- Ensure you have a valid **OpenRouter API key** (if using OpenRouter) or **OpenAI API key** (if using OpenAI).
- Add the key in LibreChat’s **Settings** > **API Keys**.

### 4. **Restart LibreChat**
- After changing settings, restart LibreChat to apply the changes.

### 5. **Check LibreChat Documentation**
- Refer to [LibreChat’s OpenRouter setup guide](https://github.com/danny-avila/LibreChat#openrouter) for detailed instructions.

---

## **Alternative Solutions**
- If you want to use OpenAI’s models, set the provider to **OpenAI** and select `gpt-4`, `gpt-4o`, or `gpt-3.5-turbo`.
- If you want to use OpenRouter, pick a model from their [supported list](https://openrouter.ai/models).

---
