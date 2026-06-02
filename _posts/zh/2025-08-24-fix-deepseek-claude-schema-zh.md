---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复DeepSeek Claude代码模式不匹配问题
translated: true
type: note
---

简短回答：模式不匹配。

Claude Code “说Anthropic语言”（它期望Anthropic-Messages风格的工具使用，如`tool_use`/`tool_result`块）。而OpenRouter上的DeepSeek V3.1 “说OpenAI语言”（它输出OpenAI风格的`tool_calls`/函数调用）。如果您的Claude Code路由器在未转换请求/响应的情况下将任务转发给DeepSeek V3.1，助手的工具调用消息将无法解析——您会在代理尝试计划/运行工具或流式输出时立即看到错误。（[Anthropic][1], [OpenRouter][2], [DeepSeek API文档][3]）

解决方案（快速修复）：

1. 使用路由器的转换器
   在您的Claude Code路由器中启用OpenRouter↔︎Anthropic请求/响应转换器，以便双向映射`tool_calls` ⇄ `tool_use`。热门的社区路由器明确支持此功能；请查看其“请求/响应转换”部分和示例配置。（[GitHub][4], [ClaudeLog][5]）

2. 选择正确的模型标识
   DeepSeek V3.1有特定的OpenRouter标识（例如V3.1/V3系列条目）。错误或过时的标识也会在流式传输或工具阶段引发错误。请验证OpenRouter的DeepSeek页面上显示的确切模型ID，并在您的路由器映射中使用它。（[OpenRouter][6]）

3. 保持在“聊天”模式（而非“推理器”），除非您已映射其字段
   如果您尝试使用流式传输特殊推理字段的推理变体，您的路由器必须转换这些字段——否则Claude Code将无法处理。在您的转换器能够处理之前，建议使用标准聊天模型或禁用额外的“思考”输出。（DeepSeek的文档强调OpenAI风格的函数调用；这正是您应该映射的。）（[DeepSeek API文档][3]）

4. 更新到最新的路由器版本
   近期的社区版本增加了对非Anthropic提供商的兼容性调整；请在测试前升级。（[GitHub][4]）

为何仅V3.1出现此问题
V3.1默认增强了代理/工具调用功能。这增加了您的Claude Code流程遇到未转换工具消息的可能性，而这正是模式不匹配问题发生的关键点。（[DeepSeek API文档][7]）

如果您分享确切的错误文本，我可以为您提供应放入配置的具体转换器代码片段。

[1]: https://www.anthropic.com/engineering/claude-code-best-practices?utm_source=chatgpt.com "Claude Code：面向智能编码的最佳实践"
[2]: https://openrouter.ai/docs/features/tool-calling?utm_source=chatgpt.com "工具与函数调用"
[3]: https://api-docs.deepseek.com/guides/function_calling?utm_source=chatgpt.com "函数调用"
[4]: https://github.com/musistudio/claude-code-router?utm_source=chatgpt.com "musistudio/claude-code-router"
[5]: https://claudelog.com/claude-code-mcps/claude-code-router/?utm_source=chatgpt.com "Claude Code路由器"
[6]: https://openrouter.ai/models?q=deepseek&utm_source=chatgpt.com "模型：'deepseek'"
[7]: https://api-docs.deepseek.com/news/news250821?utm_source=chatgpt.com "DeepSeek-V3.1发布"
