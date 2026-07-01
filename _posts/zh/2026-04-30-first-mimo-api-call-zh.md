---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小米首次米墨API调用
translated: true
type: note
---

问题：什么是小米MiMo API开放平台，如何通过它进行首次API调用？

回答：

## 小米MiMo API开放平台简介

**platform.xiaomimimo.com** 是小米官方的API控制台，用于访问**MiMo**系列大语言模型。该平台设计为**与OpenAI兼容**，这意味着您可以使用与OpenAI SDK或任何OpenAI兼容客户端相同的调用模式——只需替换基础URL和API密钥。

---

### 什么是MiMo？

MiMo是小米的AI模型系列，由AI负责人罗福立（原DeepSeek成员）领导开发。平台目前支持MiMo-V2.5和MiMo-V2系列的全部8个模型，采用基于令牌的计费方式，并提供透明可控的配额。

主要可用模型：

| 模型 | 特点 |
| --- | --- |
| **mimo-v2.5-pro** | 1.02T参数的MoE模型，420亿活跃参数，混合注意力架构，100万令牌上下文窗口，在智能体/编码任务中表现最强 |
| **mimo-v2.5** | 310B参数的稀疏MoE模型（150亿活跃参数），基于48T令牌训练，原生多模态（图像、视频、音频、文本），100万上下文 |
| **mimo-v2-pro** | 旧版旗舰模型，100万令牌上下文，推理能力强 |
| **mimo-v2-flash** | 快速、高性价比；262,144令牌上下文窗口，8192最大输出令牌 |
| **mimo-v2-omni** | 多模态（文本+图像），262,144令牌上下文 |
| **mimo-v2-tts / mimo-v2.5-tts** | 通过聊天补全端点实现文本转语音 |

---

### 基础URL与认证

API的基础URL为 `https://api.xiaomimimo.com/v1`，使用OpenAI兼容的补全接口（`openai-completions`）。

认证通过API密钥在`Authorization`请求头中完成：`Authorization: Bearer <从平台获取的API密钥>`

您可以在**小米MiMo控制台**（platform.xiaomimimo.com）中创建API密钥。

---

### 进行首次API调用

#### 选项一：cURL

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

#### 选项二：Python（OpenAI SDK）

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

#### 选项三：JavaScript（fetch）

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

### 关键API参数

| 参数 | 描述 |
| --- | --- |
| `model` | 模型ID（例如 `mimo-v2-flash`、`mimo-v2.5-pro`） |
| `messages` | `{role, content}`对象数组（system、user、assistant） |
| `max_completion_tokens` | 生成的最大令牌数 |
| `temperature` | 随机性（0–1）；推荐0.8 |
| `top_p` | 核采样；推荐0.95 |
| `stream` | `true`表示通过服务器发送事件进行流式传输 |
| `thinking` | 启用/禁用思维链推理（pro/v2.5模型支持） |

---

### 思维链模式

对于`mimo-v2.5-pro`、`mimo-v2.5`、`mimo-v2-pro`和`mimo-v2-omni`等模型，思维链（thinking）默认启用。您可以通过`"enabled"`或`"disabled"`选项进行控制。

当使用`enable_thinking: true`配合多轮工具调用时，模型会同时返回`reasoning_content`和`tool_calls`字段。您必须将之前所有轮次的`reasoning_content`持久化到消息数组中，以便在后续请求中保持推理连续性。

---

### 定价/令牌方案

令牌方案支持月付/年付订阅，覆盖MiMo-V2.5和MiMo-V2系列的全部8个模型，提供从个人到企业的四种套餐。该方案兼容主流开发工具链，如OpenCode、OpenClaw和Claude Code。

参考链接：

- [小米MiMo API平台](https://platform.xiaomimimo.com/docs/en-US/quick-start/first-api-call)
- [MiMo OpenAI兼容API参考](https://platform.xiaomimimo.com/docs/api/chat/openai-api)
- [MiMo-V2.5-Pro模型页](https://mimo.xiaomi.com/mimo-v2-5-pro/)
- [MiMo-V2.5模型页](https://mimo.xiaomi.com/mimo-v2-5)
- [LiteLLM上的小米MiMo](https://docs.litellm.ai/docs/providers/xiaomi_mimo)
- [OpenClaw小米供应商文档](https://docs.openclaw.ai/providers/xiaomi)
- [DeepWiki – MiMo-V2-Flash访问方法](https://deepwiki.com/XiaomiMiMo/MiMo-V2-Flash/4.1-access-methods)
- [令牌方案全球发布](https://mimo.mi.com/)
