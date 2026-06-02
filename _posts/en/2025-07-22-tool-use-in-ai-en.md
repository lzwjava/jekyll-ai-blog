---
audio: false
generated: true
lang: en
layout: post
title: AI Tool Use in APIs Explained
translated: false
type: note
---

### What is Tool Use in AI APIs?

Tool use, often referred to as "tool calling" or "function calling," is a feature in AI APIs that allows large language models (LLMs) to interact with external tools, functions, or APIs. Instead of generating responses solely based on their internal knowledge, the model can decide to call predefined functions to fetch real-time data, perform calculations, or execute actions. This makes the AI more dynamic and useful for tasks like querying weather, searching databases, or integrating with other services.

The process typically works like this:
- You define tools (functions) with descriptions and parameters in JSON format.
- The model analyzes the user's query and, if needed, outputs a "tool call" with the function name and arguments.
- Your application executes the function and feeds the result back to the model.
- The model then generates a final response incorporating the tool's output.

This is commonly inspired by OpenAI's function calling API, and many providers like Mistral and DeepSeek support compatible implementations.

### Mistral or DeepSeek for Tool Use?

Both Mistral AI and DeepSeek AI support tool calling in their APIs, making them suitable for building agents or applications that require external integrations. Here's a quick comparison based on available information:

- **Support for Tool Use**:
  - Both follow a similar structure to OpenAI's API, allowing easy integration with tools via JSON schemas.
  - Mistral supports it across models like Mistral Large and Medium, with options for agent-based workflows.
  - DeepSeek supports it primarily through its "deepseek-chat" model and is fully compatible with OpenAI's SDK.

- **Pros and Cons**:
  - **Mistral**: More versatile for general tasks, faster inference in some benchmarks, and better suited for European data privacy needs. It excels in quick responses and has strong multilingual capabilities. However, it can be more expensive (e.g., input/output costs are higher compared to DeepSeek).
  - **DeepSeek**: Significantly cheaper (up to 28x less costly in some comparisons), strong in math, coding, and reasoning tasks. It's ideal for budget-conscious users or high-volume usage. Drawbacks include potentially slower performance in non-technical tasks and less emphasis on multimodal features.
  - **Which to Choose?** If cost is a priority and your use case involves coding/math with tools, go with DeepSeek. For broader applications, faster responses, or enterprise features like agents, Mistral is better. Both are open-source friendly and performant, but test with your specific needs.

Ultimately, neither is strictly "better" for tool use—they both work well. DeepSeek might edge out for cost savings, while Mistral offers more polished agent integrations.

### How to Use Tool Use

To use tool calling, you'll need an API key from the respective provider (sign up at mistral.ai for Mistral or platform.deepseek.com for DeepSeek). Both use Python SDKs similar to OpenAI's. Below are step-by-step examples for a simple weather query tool.

#### Using Tool Use with Mistral AI
Mistral's API supports tool calling via their `MistralClient` in chat completions. Install the SDK with `pip install mistralai`.

**Example Python Code** (adapted from official and community sources):
```python
from mistralai import Mistral

# Initialize client with your API key
api_key = "YOUR_MISTRAL_API_KEY"
model = "mistral-large-latest"  # Supports tool calling
client = Mistral(api_key=api_key)

# Define tools (functions)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city, e.g., San Francisco"}
                },
                "required": ["location"]
            }
        }
    }
]

# User message
messages = [{"role": "user", "content": "What's the weather in Hangzhou?"}]

# First API call: Model decides if tool is needed
response = client.chat.complete(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto"  # Auto-decides tool use
)

# Check for tool calls
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    # Append the model's response to messages
    messages.append(response.choices[0].message)

    # Simulate executing the tool (in real code, call an actual API)
    tool_call = tool_calls[0]
    if tool_call.function.name == "get_weather":
        location = eval(tool_call.function.arguments)["location"]
        weather_result = "24°C and sunny"  # Replace with real function call

        # Append tool result
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": weather_result
        })

    # Second API call: Model generates final response
    final_response = client.chat.complete(model=model, messages=messages)
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
```

This code sends a query, checks for a tool call, executes it (simulated here), and gets the final answer. For agent-based setups, use Mistral's beta agents API for more complex workflows.

#### Using Tool Use with DeepSeek AI
DeepSeek's API is OpenAI-compatible, so you can use the OpenAI Python SDK. Install with `pip install openai`.

**Example Python Code** (from official docs):
```python
from openai import OpenAI

# Initialize client with DeepSeek base URL and API key
client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

# Function to send messages
def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",  # Supports tool calling
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

# User message
messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

# Handle tool call
tool = message.tool_calls[0]
messages.append(message)

# Simulate tool execution (replace with real function)
messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})

# Get final response
message = send_messages(messages)
print(f"Model>\t {message.content}")
```

This follows the same flow: query → tool call → execute → final response. DeepSeek limits context length, so keep messages concise.

For advanced usage, check rate limits, costs, and model-specific docs. Test in a sandbox to handle errors like invalid parameters.

### References
- [Mistral AI Function Calling Documentation](https://docs.mistral.ai/agents/function_calling/)
- [DeepSeek API Function Calling Guide](https://api-docs.deepseek.com/guides/function_calling)
- [Mistral AI Function Calling Example with Code](https://medium.com/@jcrsch/mistral-ai-function-calling-a-simple-example-with-code-72f3a762550f)
- [DeepSeek vs. Mistral: A Comprehensive AI Models Comparison](https://medium.com/ai-tools-tips-and-news/deepseek-vs-mistral-a-comprehensive-ai-models-comparison-f7d7b86f4b28)
- [Mistral Large vs DeepSeek-V3 Comparison](https://docsbot.ai/models/compare/mistral-large-2/deepseek-v3)
