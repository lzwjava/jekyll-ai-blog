---
audio: false
generated: true
lang: en
layout: post
title: Accessing Claude via OpenRouter
translated: false
type: note
---

### How to Use Claude Models with OpenRouter (As a Chinese User Without Anthropic API Access)

As a Chinese user, you may face restrictions accessing Anthropic's Claude API directly due to regional blocks. However, OpenRouter is a reliable alternative that acts as a unified API gateway to multiple AI providers, including Anthropic's Claude models. OpenRouter is accessible in China (both the website and API endpoints are not blocked), allowing you to route requests to Claude without needing a direct Anthropic account or API key. It's pay-per-use (you'll need to add a payment method), but signing up is free, and it supports a free tier for limited usage.

OpenRouter's API is compatible with OpenAI's format, so you can use familiar libraries like the OpenAI Python SDK. Below, I'll outline the steps to get started and provide code examples for using Claude in Python.

#### Step 1: Sign Up for OpenRouter
1. Visit the OpenRouter website: https://openrouter.ai.
2. Click on "Sign Up" or "Get Started" (usually in the top right).
3. Create an account using your email (or GitHub/Google login if available). No VPN is needed, as the site works in China.
4. After signing up, verify your email if required.
5. Go to the dashboard and add a payment method (e.g., credit card) to fund your account. OpenRouter charges based on token usage, but you can start with a small deposit. Check their pricing page for details on Claude models.

#### Step 2: Generate an API Key
1. In your OpenRouter dashboard, navigate to the "API Keys" or "Keys" section.
2. Create a new API key (it will look like a long string, e.g., `sk-or-v1-...`).
3. Copy and save it securely—treat it like a password. You'll use this in your code instead of an Anthropic key.

#### Step 3: Choose a Claude Model
OpenRouter lists Anthropic's Claude models with IDs like:
- `anthropic/claude-3.5-sonnet` (recommended for most tasks; balanced and capable).
- `anthropic/claude-3-opus` (more powerful but expensive).
- Newer versions (e.g., Claude 3.7 if available in 2025) will be listed on https://openrouter.ai/models?providers=anthropic.

You can browse the models page to see costs, context limits, and availability.

#### Step 4: Set Up Your Environment
- Install Python if you don't have it (version 3.8+ recommended).
- Install the OpenAI library: Run `pip install openai` in your terminal.

#### Step 5: Use Claude in Code
Use the OpenAI SDK with OpenRouter's base URL (`https://openrouter.ai/api/v1`). Specify the Claude model ID in your requests.

Here's a simple Python example to chat with Claude 3.5 Sonnet:

```python
from openai import OpenAI

# Initialize the client with OpenRouter's endpoint and your API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY_HERE",  # Replace with your actual key
)

# Make a request to Claude
completion = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # Use the Claude model ID
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, what is the capital of China?"}
    ],
    temperature=0.7,  # Optional: Adjust for creativity (0-1)
    max_tokens=150    # Optional: Limit response length
)

# Print the response
print(completion.choices[0].message.content)
```

- **Explanation**: This sends a system prompt and user message to Claude, gets a response, and prints it. Replace the API key and adjust parameters as needed.
- **If you prefer raw HTTP requests** (without the OpenAI library):

```python
import requests
import json

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_OPENROUTER_API_KEY_HERE",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, what is the capital of China?"}
        ]
    })
)

# Parse and print the response
data = response.json()
print(data['choices'][0]['message']['content'])
```

- **Tips**:
  - Add optional headers like `"HTTP-Referer": "your-site-url"` and `"X-Title": "Your App Name"` to attribute usage (helps with leaderboards and potential free credits).
  - Monitor usage in your OpenRouter dashboard to avoid unexpected costs.
  - For streaming responses or advanced features (e.g., tools), refer to OpenRouter's full docs.
  - If you encounter rate limits or errors, check your balance or try a different model.

#### Troubleshooting
- **API Errors**: Ensure your key is correct and funded. Test with a cheap model first.
- **Regional Issues**: If any blocks occur (unlikely), use a VPN, but OpenRouter is designed to bypass such restrictions for supported models.
- **Free Alternatives**: For limited free access, explore proxies like Puter.js (but they may have limitations).

This setup lets you use Claude programmatically without direct Anthropic access. If you need integration with specific tools (e.g., Cursor IDE or Make.com), search for tutorials on those.

References:
[OpenRouter Documentation](https://openrouter.ai/docs)
[Anthropic Claude on OpenRouter](https://openrouter.ai/anthropic/claude-3.5-sonnet)
[Using OpenRouter in China](https://medium.com/ai-simplified-in-plain-english/not-re-inventing-the-wheel-in-ai-2ec3e76ae2bd)
[How to Use Claude in China](https://www.comparitech.com/blog/vpn-privacy/how-to-use-claude-in-china/)
