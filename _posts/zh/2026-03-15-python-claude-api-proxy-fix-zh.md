---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Python Claude API 代理脚本
translated: true
type: note
---

**问题：** 如何修复调用 pincc.ai Claude API 代理的 Python 脚本，使其正确工作？

**答案：**

根据您分享的文档以及实际 `claude` CLI 的成功工作方式（`ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`），以下是完整的分析和修复。

---

## 根本原因分析

pincc.ai 代理是一个 **Claude Code 中继服务**。从日志中可以看到，真实的 CLI 完美工作：

```bash
ANTHROPIC_BASE_URL="https://v2-as.pincc.ai" ANTHROPIC_AUTH_TOKEN="$PINCC_API_KEY" claude --print "Hello"
# 输出：Hello! How can I help you today?
```

但是 Python `requests` 脚本持续失败。最可能的原因：

1. **错误的认证头格式** — 该中继可能期望 `x-api-key` 而非 `Authorization: Bearer`
2. **错误的模型名称** — `claude-sonnet-4-6` 可能不被接受；该中继可能需要特定的模型字符串
3. **缺少或错误的 `anthropic-beta` 头** — 该中继验证 Claude Code 客户端身份
4. **SSL / 请求库问题** — 日志中的 urllib3 版本警告

---

## 修复后的脚本

按顺序尝试每种方法：

### 方法 1 — 使用 `x-api-key`（标准 Anthropic 格式）

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

### 方法 2 — 完全匹配 CLI 发送的内容

根据文档，CLI 使用 `ANTHROPIC_AUTH_TOKEN`，它映射到 `Authorization: Bearer`。日志中的关键洞察是 CLI 还使用特定的头来标识自己：

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

### 方法 3 — 使用 `httpx` 避免 urllib3 警告

`requests` 版本警告（`urllib3 (2.6.3) ... doesn't match a supported version`）有时会导致 SSL 问题。切换到 `httpx`：

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

### 方法 4 — 使用官方 Anthropic SDK（最可靠）

pincc.ai 中继支持标准的 `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` 配置。您可以直接使用 SDK：

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

安装命令：`pip install anthropic`

---

## 快速调试提示

打印完整的错误响应以查看确切失败原因：

```python
print(response.status_code)
print(response.text)  # raw response text, better than .json() when it fails
```

常见错误含义：
- **401** → API 密钥错误或认证头格式错误
- **403** → 客户端身份检查失败（User-Agent / beta 头）
- **404** → 端点路径错误
- **422** → 模型名称或请求体格式错误

**方法 4 (SDK)** 是最推荐的，因为它自动处理认证、重试和模型命名，并且已知与中继代理兼容。

**参考资料：**

- [pincc.ai Claude Code Install Guide](https://pincc.ai/en/claude-code-install)
- [pincc.ai Relay Service](https://pincc.ai/en/)