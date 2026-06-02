---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Python Claude API Proxy Script
translated: false
type: note
---

**Question:** How do I fix the Python script that calls the pincc.ai Claude API proxy, and make it work correctly?

**Answer:**

Based on the document you shared and what the actual `claude` CLI does successfully (`ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`), here is a complete analysis and fix.

---

## Root Cause Analysis

The pincc.ai proxy is a **Claude Code relay service**. From the logs, you can see the real CLI works perfectly with:

```bash
ANTHROPIC_BASE_URL="https://v2-as.pincc.ai" ANTHROPIC_AUTH_TOKEN="$PINCC_API_KEY" claude --print "Hello"
# Output: Hello! How can I help you today?
```

But the Python `requests` script keeps failing. The most likely reasons:

1. **Wrong auth header format** — the relay may expect `x-api-key` not `Authorization: Bearer`
2. **Wrong model name** — `claude-sonnet-4-6` may not be accepted; the relay may want a specific model string
3. **Missing or wrong `anthropic-beta` header** — the relay validates Claude Code client identity
4. **SSL / request library issues** — the urllib3 version warning in your logs

---

## Fixed Script

Try each approach in order:

### Approach 1 — Use `x-api-key` (standard Anthropic format)

```python
#!/usr/bin/env python3
import os
import requests

def main():
    api_key = os.environ.get("PINCC_API_KEY")
    if not api_key:
        raise ValueError("PINCC_API_KEY environment variable not set")

    response = requests.post(
        "https://v2-as.pincc.ai/v1/messages",
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": api_key,              # ← standard Anthropic header
        },
        json={
            "model": "claude-sonnet-4-20250514",  # ← use full model string
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello!"}],
        },
    )
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    main()
```

### Approach 2 — Match exactly what the CLI sends

From the document, the CLI uses `ANTHROPIC_AUTH_TOKEN` which maps to `Authorization: Bearer`. The key insight from the logs is the CLI also identifies itself with specific headers:

```python
#!/usr/bin/env python3
import os
import requests

def main():
    api_key = os.environ.get("PINCC_API_KEY")
    if not api_key:
        raise ValueError("PINCC_API_KEY environment variable not set")

    response = requests.post(
        "https://v2-as.pincc.ai/v1/messages",
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "claude-code/2.1.76 (external)",
            "anthropic-beta": "claude-code-20250219",
            "x-stainless-helper": "true",        # ← found in the CLI source
        },
        json={
            "model": "claude-sonnet-4-20250514",  # ← full model string
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello!"}],
        },
    )
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    main()
```

### Approach 3 — Use `httpx` to avoid the urllib3 warning

The `requests` version warning (`urllib3 (2.6.3) ... doesn't match a supported version`) can sometimes cause SSL issues. Switch to `httpx`:

```python
#!/usr/bin/env python3
import os
import httpx

def main():
    api_key = os.environ.get("PINCC_API_KEY")
    if not api_key:
        raise ValueError("PINCC_API_KEY environment variable not set")

    with httpx.Client() as client:
        response = client.post(
            "https://v2-as.pincc.ai/v1/messages",
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": api_key,
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello!"}],
            },
        )
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    main()
```

### Approach 4 — Use the official Anthropic SDK (most reliable)

The pincc.ai relay supports the standard `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` configuration. You can leverage this directly with the SDK:

```python
#!/usr/bin/env python3
import os
import anthropic

def main():
    client = anthropic.Anthropic(
        base_url="https://v2-as.pincc.ai",
        auth_token=os.environ.get("PINCC_API_KEY"),
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(message.content)

if __name__ == "__main__":
    main()
```

Install with: `pip install anthropic`

---

## Quick Debugging Tips

Print the full error response to see exactly what's failing:

```python
print(response.status_code)
print(response.text)  # raw response text, better than .json() when it fails
```

Common error meanings:
- **401** → wrong API key or auth header format
- **403** → client identity check failing (User-Agent / beta header)
- **404** → wrong endpoint path
- **422** → wrong model name or request body format

The **Approach 4 (SDK)** is the most recommended since it handles auth, retries, and model naming automatically and is known to work with relay proxies.

**References:**

- [pincc.ai Claude Code Install Guide](https://pincc.ai/en/claude-code-install)
- [pincc.ai Relay Service](https://pincc.ai/en/)
