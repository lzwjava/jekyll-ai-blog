---
audio: false
generated: true
lang: zh
layout: post
title: API中的人工智能工具应用解析
translated: true
type: note
---

### 什么是 AI API 中的工具使用？

工具使用，通常被称为“工具调用”或“函数调用”，是 AI API 中的一项功能，允许大型语言模型（LLMs）与外部工具、函数或 API 进行交互。模型不再仅仅依赖其内部知识生成响应，而是可以决定调用预定义的函数来获取实时数据、执行计算或执行操作。这使得 AI 对于诸如查询天气、搜索数据库或与其他服务集成等任务更加动态和实用。

该过程通常如下工作：

- 您以 JSON 格式定义具有描述和参数的**工具**（函数）。
- 模型分析用户的查询，并在需要时输出一个包含函数名称和参数的 **"工具调用"**。
- 您的应用程序执行该函数并将结果反馈给模型。
- 模型随后生成一个**最终响应**，其中包含了工具的输出。

这通常受到 OpenAI 的函数调用 API 的启发，许多提供商如 Mistral 和 DeepSeek 都支持兼容的实现。

### 工具使用选 Mistral 还是 DeepSeek？

Mistral AI 和 DeepSeek AI 都在其 API 中支持工具调用，这使得它们适合构建需要外部集成的智能体或应用程序。以下是基于现有信息的简要比较：

- **对工具使用的支持**：
  - 两者都遵循与 OpenAI API 类似的结构，允许通过 JSON 模式轻松集成工具。
  - Mistral 在其 Mistral Large 和 Medium 等模型中支持此功能，并提供基于智能体工作流的选项。
  - DeepSeek 主要通过其 "deepseek-chat" 模型支持，并且与 OpenAI 的 SDK 完全兼容。

- **优缺点**：
  - **Mistral**：更适用于通用任务，在某些基准测试中推理速度更快，并且更符合欧洲的数据隐私需求。它在快速响应方面表现出色，并具有强大的多语言能力。然而，它可能更昂贵（例如，与 DeepSeek 相比，输入/输出成本更高）。
  - **DeepSeek**：显著更便宜（在某些比较中成本可低至 28 倍），在数学、编码和推理任务方面表现强劲。对于预算敏感的用户或高使用量场景来说是理想选择。缺点包括在非技术任务中可能性能较慢，并且对多模态功能的重视较少。
  - **如何选择？** 如果成本是首要考虑因素，并且您的用例涉及编码/数学相关的工具使用，请选择 DeepSeek。对于更广泛的应用、更快的响应速度或企业级功能（如智能体），Mistral 是更好的选择。两者都对开源友好且性能良好，但请根据您的具体需求进行测试。

最终，对于工具使用而言，没有哪一个是绝对“更好”的——它们都运作良好。DeepSeek 可能在成本节约方面略胜一筹，而 Mistral 则提供了更完善的智能体集成。

### 如何使用工具使用功能

要使用工具调用，您需要从相应的提供商处获取 API 密钥（在 mistral.ai 注册 Mistral 或在 platform.deepseek.com 注册 DeepSeek）。两者都使用与 OpenAI 类似的 Python SDK。以下是一个简单天气查询工具的分步示例。

#### 使用 Mistral AI 进行工具调用

Mistral 的 API 通过其 `MistralClient` 在聊天补全中支持工具调用。使用 `pip install mistralai` 安装 SDK。

**Python 代码示例**（改编自官方和社区来源）：

```python
from mistralai import Mistral

# 使用您的 API 密钥初始化客户端
api_key = "YOUR_MISTRAL_API_KEY"
model = "mistral-large-latest"  # 支持工具调用
client = Mistral(api_key=api_key)

# 定义工具（函数）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取某个地点的天气。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市，例如：San Francisco"}
                },
                "required": ["location"]
            }
        }
    }
]

# 用户消息
messages = [{"role": "user", "content": "杭州的天气怎么样？"}]

# 第一次 API 调用：模型决定是否需要工具
response = client.chat.complete(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto"  # 自动决定是否使用工具
)

# 检查工具调用
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    # 将模型的响应附加到消息列表中
    messages.append(response.choices[0].message)

    # 模拟执行工具（在实际代码中，调用真实的 API）
    tool_call = tool_calls[0]
    if tool_call.function.name == "get_weather":
        location = eval(tool_call.function.arguments)["location"]
        weather_result = "24°C，晴朗"  # 替换为真实的函数调用

        # 附加工具结果
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": weather_result
        })

    # 第二次 API 调用：模型生成最终响应
    final_response = client.chat.complete(model=model, messages=messages)
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
```

此代码发送查询，检查工具调用，执行它（此处为模拟），并获取最终答案。对于基于智能体的设置，可以使用 Mistral 的 beta 版智能体 API 来处理更复杂的工作流。

#### 使用 DeepSeek AI 进行工具调用

DeepSeek 的 API 与 OpenAI 兼容，因此您可以使用 OpenAI Python SDK。使用 `pip install openai` 安装。

**Python 代码示例**（来自官方文档）：

```python
from openai import OpenAI

# 使用 DeepSeek 基础 URL 和 API 密钥初始化客户端
client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取某个地点的天气，用户应首先提供一个地点",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市和州，例如 San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

# 发送消息的函数
def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",  # 支持工具调用
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

# 用户消息
messages = [{"role": "user", "content": "杭州的天气怎么样？"}]
message = send_messages(messages)
print(f"用户>\t {messages[0]['content']}")

# 处理工具调用
tool = message.tool_calls[0]
messages.append(message)

# 模拟工具执行（替换为真实函数）
messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})

# 获取最终响应
message = send_messages(messages)
print(f"模型>\t {message.content}")
```

这遵循相同的流程：查询 → 工具调用 → 执行 → 最终响应。DeepSeek 限制了上下文长度，因此请保持消息简洁。

对于高级用法，请查看速率限制、成本和模型特定文档。在沙盒环境中进行测试以处理诸如无效参数之类的错误。

### 参考资料

- [Mistral AI 函数调用文档](https://docs.mistral.ai/agents/function_calling/)
- [DeepSeek API 函数调用指南](https://api-docs.deepseek.com/guides/function_calling)
- [Mistral AI 函数调用代码示例](https://medium.com/@jcrsch/mistral-ai-function-calling-a-simple-example-with-code-72f3a762550f)
- [DeepSeek vs. Mistral：全面的 AI 模型比较](https://medium.com/ai-tools-tips-and-news/deepseek-vs-mistral-a-comprehensive-ai-models-comparison-f7d7b86f4b28)
- [Mistral Large vs DeepSeek-V3 比较](https://docsbot.ai/models/compare/mistral-large-2/deepseek-v3)
