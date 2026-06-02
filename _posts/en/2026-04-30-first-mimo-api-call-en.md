---
audio: false
generated: true
image: false
lang: en
layout: post
title: First Xiaomi MiMo API Call
translated: false
type: note
---

Question: What is the Xiaomi MiMo API Open Platform, and how do I make my first API call using it?

Answer:

## Introduction to the Xiaomi MiMo API Open Platform

**platform.xiaomimimo.com** is Xiaomi's official API console for accessing the **MiMo** family of large language models. It is designed to be **OpenAI-compatible**, meaning you can use the same patterns you already know from the OpenAI SDK or any OpenAI-compatible client — just swap the base URL and API key.

---

### What Is MiMo?

MiMo is Xiaomi's AI model series, developed under AI lead Fuli Luo (formerly of DeepSeek). The platform currently supports all 8 models in the MiMo-V2.5 and MiMo-V2 series, with token-based billing and transparent, controllable quotas.

Key models available:

| Model | Highlights |
|---|---|
| **mimo-v2.5-pro** | 1.02T-parameter MoE with 42B active parameters, hybrid-attention architecture, 1M-token context window, strongest for agentic/coding tasks |
| **mimo-v2.5** | 310B-parameter Sparse MoE (15B active), trained on 48T tokens, native multimodal (image, video, audio, text), 1M context |
| **mimo-v2-pro** | Older flagship with 1M token context, strong reasoning |
| **mimo-v2-flash** | Fast, cost-efficient; 262,144 token context window, 8192 max output tokens |
| **mimo-v2-omni** | Multimodal (text + image), 262,144 token context |
| **mimo-v2-tts / mimo-v2.5-tts** | Text-to-speech via the chat completions endpoint |

---

### Base URL & Authentication

The base URL for the API is `https://api.xiaomimimo.com/v1` and it uses OpenAI-compatible completions (`openai-completions`).

Authentication is done via an API key in the `Authorization` header: `Authorization: Bearer <your-api-key-from-platform>`

You create your API key inside the **Xiaomi MiMo console** at platform.xiaomimimo.com.

---

### Making Your First API Call

#### Option 1: cURL

```bash
curl --location --request POST 'https://api.xiaomimimo.com/v1/chat/completions' \
  --header "Authorization: Bearer $MIMO_API_KEY" \
  --header "Content-Type: application/json" \
  --data-raw '{
    "model": "mimo-v2-flash",
    "messages": [
      {
        "role": "system",
        "content": "You are MiMo, an AI assistant developed by Xiaomi."
      },
      {
        "role": "user",
        "content": "Hello, please introduce yourself."
      }
    ],
    "max_completion_tokens": 1024,
    "temperature": 0.8,
    "top_p": 0.95,
    "stream": false
  }'
```

#### Option 2: Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MIMO_API_KEY",
    base_url="https://api.xiaomimimo.com/v1"
)

response = client.chat.completions.create(
    model="mimo-v2-flash",
    messages=[
        {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi."},
        {"role": "user", "content": "Hello, please introduce yourself."}
    ],
    max_tokens=1024,
    temperature=0.8,
    top_p=0.95
)

print(response.choices[0].message.content)
```

#### Option 3: JavaScript (fetch)

```javascript
const response = await fetch('https://api.xiaomimimo.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_MIMO_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'mimo-v2-flash',
    messages: [
      { role: 'system', content: 'You are MiMo, an AI assistant developed by Xiaomi.' },
      { role: 'user', content: 'Hello!' }
    ],
    max_tokens: 1024,
    temperature: 0.8
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

---

### Key API Parameters

| Parameter | Description |
|---|---|
| `model` | Model ID (e.g., `mimo-v2-flash`, `mimo-v2.5-pro`) |
| `messages` | Array of `{role, content}` objects (system, user, assistant) |
| `max_completion_tokens` | Max tokens to generate |
| `temperature` | Randomness (0–1); 0.8 recommended |
| `top_p` | Nucleus sampling; 0.95 recommended |
| `stream` | `true` for streaming via server-sent events |
| `thinking` | Enable/disable chain-of-thought reasoning (supported on pro/v2.5 models) |

---

### Thinking / Chain-of-Thought Mode

For models like `mimo-v2.5-pro`, `mimo-v2.5`, `mimo-v2-pro`, and `mimo-v2-omni`, chain-of-thought (thinking) is enabled by default. You can control this with `"enabled"` or `"disabled"` options.

When using `enable_thinking: true` with multi-turn tool calls, the model returns both `reasoning_content` and `tool_calls` fields. You must persist all `reasoning_content` from previous turns in the messages array for subsequent requests to maintain reasoning continuity.

---

### Pricing / Token Plan

The Token Plan supports monthly/annual subscriptions and covers all 8 models in the MiMo-V2.5 and MiMo-V2 series, with four tiers available for individuals to enterprises. It is compatible with mainstream development toolchains like OpenCode, OpenClaw, and Claude Code.

References:

- [Xiaomi MiMo API Platform](https://platform.xiaomimimo.com/docs/en-US/quick-start/first-api-call)
- [MiMo OpenAI-compatible API reference](https://platform.xiaomimimo.com/docs/api/chat/openai-api)
- [MiMo-V2.5-Pro model page](https://mimo.xiaomi.com/mimo-v2-5-pro/)
- [MiMo-V2.5 model page](https://mimo.xiaomi.com/mimo-v2-5)
- [Xiaomi MiMo on LiteLLM](https://docs.litellm.ai/docs/providers/xiaomi_mimo)
- [OpenClaw Xiaomi provider docs](https://docs.openclaw.ai/providers/xiaomi)
- [DeepWiki – MiMo-V2-Flash Access Methods](https://deepwiki.com/XiaomiMiMo/MiMo-V2-Flash/4.1-access-methods)
- [Token Plan Global Launch](https://mimo.mi.com/)
