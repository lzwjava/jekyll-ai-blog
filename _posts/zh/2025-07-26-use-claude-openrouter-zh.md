---
audio: false
generated: true
lang: zh
layout: post
title: 通过OpenRouter访问Claude
translated: true
type: note
---

### 如何通过 OpenRouter 使用 Claude 模型（中国用户无需 Anthropic API 访问权限）

作为中国用户，由于区域限制可能无法直接访问 Anthropic 的 Claude API。不过，OpenRouter 是一个可靠的替代方案，它作为统一 API 网关连接多个 AI 提供商，包括 Anthropic 的 Claude 模型。OpenRouter 在中国可以访问（其网站和 API 端点均未被屏蔽），让您无需直接拥有 Anthropic 账户或 API 密钥即可向 Claude 发送请求。这是按使用量付费的服务（需要添加支付方式），但注册免费，且支持有限用量的免费层级。

OpenRouter 的 API 与 OpenAI 的格式兼容，因此您可以使用熟悉的库，比如 OpenAI Python SDK。下面我将概述入门步骤，并提供在 Python 中使用 Claude 的代码示例。

#### 第一步：注册 OpenRouter
1. 访问 OpenRouter 网站：https://openrouter.ai。
2. 点击“Sign Up”或“Get Started”（通常在右上角）。
3. 使用您的电子邮箱（或 GitHub/Google 登录，如果可用）创建账户。无需 VPN，因为该网站在中国可以访问。
4. 注册后，如果需要，请验证您的电子邮箱。
5. 进入仪表板并添加支付方式（例如信用卡）为账户充值。OpenRouter 基于令牌使用量收费，但您可以从小额存款开始。有关 Claude 模型的详细定价，请查看其定价页面。

#### 第二步：生成 API 密钥
1. 在您的 OpenRouter 仪表板中，导航至“API Keys”或“Keys”部分。
2. 创建一个新的 API 密钥（它将是一个长字符串，例如 `sk-or-v1-...`）。
3. 复制并安全保存——请像对待密码一样对待它。您将在代码中使用此密钥，而不是 Anthropic 的密钥。

#### 第三步：选择 Claude 模型
OpenRouter 列出了 Anthropic 的 Claude 模型，其 ID 类似：
- `anthropic/claude-3.5-sonnet`（推荐用于大多数任务；均衡且能力强）。
- `anthropic/claude-3-opus`（更强大但更昂贵）。
- 更新的版本（例如，如果 2025 年有 Claude 3.7）将在 https://openrouter.ai/models?providers=anthropic 列出。

您可以浏览模型页面以查看成本、上下文限制和可用性。

#### 第四步：设置您的环境
- 如果尚未安装 Python，请安装（推荐版本 3.8+）。
- 安装 OpenAI 库：在终端中运行 `pip install openai`。

#### 第五步：在代码中使用 Claude
使用 OpenAI SDK 并指定 OpenRouter 的基础 URL（`https://openrouter.ai/api/v1`）。在您的请求中指定 Claude 模型 ID。

以下是一个简单的 Python 示例，用于与 Claude 3.5 Sonnet 聊天：

```python
from openai import OpenAI

# 使用 OpenRouter 的端点和您的 API 密钥初始化客户端
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY_HERE",  # 替换为您的实际密钥
)

# 向 Claude 发送请求
completion = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # 使用 Claude 模型 ID
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, what is the capital of China?"}
    ],
    temperature=0.7,  # 可选：调整创造性（0-1）
    max_tokens=150    # 可选：限制响应长度
)

# 打印响应
print(completion.choices[0].message.content)
```

- **解释**：这将向 Claude 发送系统提示和用户消息，获取响应并打印。根据需要替换 API 密钥并调整参数。
- **如果您偏好原始 HTTP 请求**（不使用 OpenAI 库）：

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

# 解析并打印响应
data = response.json()
print(data['choices'][0]['message']['content'])
```

- **提示**：
  - 添加可选头部，如 `"HTTP-Referer": "your-site-url"` 和 `"X-Title": "Your App Name"`，以归属使用情况（有助于排行榜和潜在的免费积分）。
  - 在您的 OpenRouter 仪表板中监控使用情况，以避免意外成本。
  - 对于流式响应或高级功能（例如工具），请参考 OpenRouter 的完整文档。
  - 如果遇到速率限制或错误，请检查您的余额或尝试不同的模型。

#### 故障排除
- **API 错误**：确保您的密钥正确且已充值。首先使用一个便宜的模型进行测试。
- **区域问题**：如果出现任何屏蔽（不太可能），请使用 VPN，但 OpenRouter 旨在为支持的模型绕过此类限制。
- **免费替代方案**：对于有限的免费访问，可以探索像 Puter.js 这样的代理（但它们可能有限制）。

此设置让您无需直接访问 Anthropic 即可编程使用 Claude。如果您需要与特定工具（例如 Cursor IDE 或 Make.com）集成，请搜索相关教程。

参考文献：
[OpenRouter 文档](https://openrouter.ai/docs)
[OpenRouter 上的 Anthropic Claude](https://openrouter.ai/anthropic/claude-3.5-sonnet)
[在中国使用 OpenRouter](https://medium.com/ai-simplified-in-plain-english/not-re-inventing-the-wheel-in-ai-2ec3e76ae2bd)
[如何在中国使用 Claude](https://www.comparitech.com/blog/vpn-privacy/how-to-use-claude-in-china/)
