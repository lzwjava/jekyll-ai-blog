---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 配置GitHub Copilot LLM路由器
translated: true
type: note
---

要在企业环境中配置您的LLM路由器，使其专门使用GitHub Copilot的LLM API，您需要为其添加专用提供商，并调整路由器设置以将所有流量路由至该提供商。

- **添加GitHub Copilot提供商**：在"Providers"数组中新增一个条目，包含适当的API基础URL、您的GitHub个人访问令牌作为API密钥，以及支持的模型。
- **更新路由器默认设置**：将所有路由器字段更改为仅指向新提供商名称，确保不调用其他任何提供商。
- **处理企业限制**：使用您企业GitHub账户具有必要作用域的个人访问令牌，如果您的环境出于合规性要求需要代理路由，请利用现有的"PROXY_URL"。
- **测试与验证**：更新后，验证所有API调用是否仅定向到Copilot端点，以符合仅允许Copilot API交互的策略。

### 分步配置指南

1. **生成GitHub个人访问令牌**：登录您的企业GitHub账户，创建一个具有`copilot`作用域的个人访问令牌，以确保安全认证而不暴露更广泛的权限。
2. **修改提供商数组**：在您的配置JSON中的"Providers"列表末尾追加一个新对象。将"name"设置为描述性名称，将"api_base_url"设置为Copilot代理端点或GitHub Models推理端点，将"api_key"设置为您的个人访问令牌，并列出兼容的模型。
3. **调整路由器部分**：将"Router"对象中的所有值替换为您的新提供商名称，以强制排他性使用。这可以防止回退到其他提供商。
4. **企业注意事项**：在受限环境中，确认您的网络策略允许对GitHub域进行出站调用。如果需要，更新"PROXY_URL"以通过经批准的企业代理进行路由。启用日志记录以审计调用并确保合规性。

### 更新后的配置示例

以下为修改后配置的可能样貌：

```json
{
  "PROXY_URL": "http://127.0.0.1:7890",
  "LOG": true,
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "",
      "models": [
        "moonshotai/kimi-k2",
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking",
        "anthropic/claude-opus-4",
        "google/gemini-2.5-flash",
        "google/gemini-2.5-pro",
        "deepseek/deepseek-chat-v3.1",
        "deepseek/deepseek-r1",
        "mistralai/mistral-medium-3.1",
        "qwen/qwen3-coder",
        "openai/gpt-oss-120b",
        "openai/gpt-5",
        "z-ai/glm-4.6",
        "x-ai/grok-code-fast-1",
        "x-ai/grok-4-fast",
        "minimax/minimax-m2",
        "moonshotai/kimi-k2-thinking"
      ],
      "transformer": {
        "use": [
          "openrouter"
        ]
      }
    },
    {
      "name": "github_copilot",
      "api_base_url": "https://api.githubcopilot.com/chat/completions",
      "api_key": "ghp_YourPersonalAccessTokenHere",
      "models": [
        "gpt-4o",
        "gpt-4o-mini",
        "claude-3-5-sonnet-20240620"
      ],
      "transformer": {
        "use": [
          "github_copilot"
        ]
      }
    }
  ],
  "Router": {
    "default": "github_copilot",
    "background": "github_copilot",
    "think": "github_copilot",
    "longContext": "github_copilot",
    "longContextThreshold": 30000,
    "webSearch": "github_copilot"
  }
}
```

此设置确保路由器仅与Copilot API交互，符合限制调用至经批准端点的企业策略。

---

在企业环境中，集成像GitHub Copilot这样的LLM API需要仔细配置以遵守安全策略，通常限制出站调用至特定的经批准服务。所提供的路由器配置似乎是一个用于跨提供商路由LLM请求的自定义设置。要使其专门使用GitHub Copilot的LLM API——确保不调用其他外部服务——您需要将Copilot添加为提供商，并在所有路由器路径中强制执行。这种方法支持企业防火墙或合规规则仅允许GitHub托管API的场景，利用Copilot的OpenAI兼容接口进行聊天补全。

GitHub Copilot主要通过两种途径提供LLM访问：用于构建代理和扩展的专用Copilot LLM端点，以及用于通用推理的更广泛的GitHub Models API。Copilot专用端点专为企业级代理开发量身定制，支持OpenAI聊天补全格式的POST请求。认证使用源自GitHub个人访问令牌的Bearer令牌。或者，GitHub Models API提供了一个更通用的推理服务，允许仅使用GitHub凭证访问模型目录。这对于原型设计和集成到工作流中非常理想。可用模型包括行业标准，所有这些都可通过相同的OpenAI兼容API格式调用。这种兼容性使其易于融入您的路由器配置，而无需对下游代码进行重大更改。

对于企业特定配置，GitHub Copilot Enterprise增强了标准Copilot的功能，但API访问遵循相同的模式。网络管理至关重要：您可以配置基于订阅的路由以确保Copilot流量使用经批准的路径。如果您的环境强制使用代理，请更新配置中的"PROXY_URL"指向您的企业代理服务器。像LiteLLM这样的工具可以作为中间代理进行进一步控制。但在您的情况下，由于目标是排他性，请避免在路由器中使用回退以符合策略。

要在您的配置中实现这一点，首先追加一个新的提供商对象。根据您的用例选择端点：如果构建扩展，请使用Copilot代理端点；如果用于通用LLM路由，请使用GitHub Models。列出与您现有模型重叠的模型以保持兼容性。然后，覆盖所有"Router"字段以仅引用此新提供商，消除回退。启用日志记录以监控合规性，并通过模拟请求进行测试以验证未命中未经授权的端点。如果与VS Code或其他IDE集成，请调整设置以在需要时通过您配置的代理进行路由。

以下是两个主要GitHub LLM API选项的比较表，以帮助决定在您的提供商配置中使用哪个端点：

| 方面                     | GitHub Copilot LLM API                     | GitHub Models API                                   |
|--------------------------|--------------------------------------------|-----------------------------------------------------|
| 端点                     | <https://api.githubcopilot.com/chat/completions> | <https://models.github.ai/inference/chat/completions> |
| 主要用途                 | 构建Copilot扩展和代理                      | 通用原型设计、推理和工作流                          |
| 认证                     | Bearer PAT                                 | 具有models:read作用域的PAT                          |
| 支持的模型               | 隐式                                       | 显式目录                                            |
| 企业功能                 | 第三方速率限制；与Copilot Enterprise集成   | 可在GitHub Actions中使用；自带密钥支持              |
| 速率限制/配额            | 对非GitHub代理严格                         | 原型设计免费层级；企业可扩展                        |
| 兼容性                   | OpenAI聊天格式                             | OpenAI兼容；易于路由器集成                          |

此表突显了为什么GitHub Models可能更适用于广泛的路由器使用，因为它提供了更明确的模型选择和企业工作流集成。

潜在挑战包括令牌过期，因此在企业脚本中自动化续订。如果您的环境使用GitHub Enterprise Cloud，请在组织级别启用Copilot以实现无缝访问。对于高级设置，探索在GitHub Models中自带API密钥，以通过首选提供商进行路由，同时保持在GitHub的生态系统内。始终优先参考主要的GitHub文档以获取最新的作用域和端点，因为功能发展迅速。如果直接API调用由于网络限制而失败，请考虑使用GitHub的代理配置选项或与Azure集成以进行混合企业部署。

总之，此配置将您的路由器转变为Copilot专用系统，在保持代码相关或通用LLM任务功能的同时，与企业策略保持一致。

**主要引用文献：**

- [使用GitHub Copilot的LLM为您的代理服务](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/use-copilot-extensions/build-a-copilot-agent/use-copilots-llm)
- [GitHub Models快速入门](https://docs.github.com/en/github-models/quickstart)
- [GitHub Copilot | liteLLM](https://docs.litellm.ai/docs/tutorials/github_copilot_integration)
- [管理GitHub Copilot对您企业网络的访问](https://docs.github.com/enterprise-cloud%40latest/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-access/manage-network-access)
- [配置GitHub Copilot的网络设置](https://docs.github.com/copilot/configuring-github-copilot/configuring-network-settings-for-github-copilot)
- [使用AI模型进行原型设计](https://docs.github.com/github-models/prototyping-with-ai-models)
- [在GitHub Models中使用您自己的API密钥](https://docs.github.com/en/github-models/github-models-at-scale/using-your-own-api-keys-in-github-models)
