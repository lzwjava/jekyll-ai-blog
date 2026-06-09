---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VS Code Copilot 代理架构
translated: true
type: note
---

以下是发现的内容。VS Code 代码库拥有一个非常庞大的 Copilot agent 系统。具体分解如下：

== COPILOT AGENT 架构 ==

1. 三种核心 Agent 模式（在 promptFileContrib.ts 中注册）

   - Plan Agent（planAgentProvider.ts）
     - 只读规划 agent，从不执行实现
     - 工作流程：发现 → 对齐 → 设计 → 细化
     - 使用 Explore/SearchSubagent 进行代码库研究
     - 通过 vscode/memory 工具将计划保存到 /memories/session/plan.md
     - 可通过切换按钮将任务移交给实现 agent
     - 工具：DEFAULT_READ_TOOLS（搜索、读取、网络、记忆、github/issue_read、终端输出、测试失败信息）
     - 配置：chat.planAgent.model、chat.planAgent.additionalTools

   - Ask Agent（askAgentProvider.ts）
     - 只读问答 agent，严格不修改工作区
     - 工作流程：理解 → 研究 → 澄清 → 回答
     - 工具：DEFAULT_READ_TOOLS + mermaid 图表渲染 + askQuestions
     - 配置：chat.askAgent.model、chat.askAgent.additionalTools

   - Agent Mode（agentIntent.ts）—— 主编码 agent
     - 完全读写访问，工具调用循环
     - 配置：chat.agent.maxRequests（默认 200）

2. Agent 交接系统（agentTypes.ts）

   AgentHandoff 接口支持 Plan → Agent 的转换：
   - label、agent 名称、提示、发送标志、模型覆盖
   - buildAgentMarkdown() 动态生成 .agent.md YAML 前置元数据
   - 在聊天 UI 中渲染交接按钮供用户批准

3. 切换 Agent 工具（switchAgentTool.ts）

   - ToolName.SwitchAgent —— 允许主 agent 切换到 Plan agent
   - 仅支持切换到 Plan（不支持 Ask 或其他）
   - 执行 `workbench.action.chat.toggleAgentMode` 命令
   - 切换后返回 Plan agent 主体作为上下文

4. 工具调用循环（toolCallingLoop.ts —— 2073 行）

   agent 核心执行引擎：
   - 迭代循环：构建提示 → 调用 LLM → 执行工具调用 → 重复
   - 工具调用限制，可配置行为（确认或停止）
   - 用于会话生命周期的启动/停止钩子
   - 用于嵌套 agent 追踪的子 agent 启动/停止钩子
   - 长构建期间的保活探测（4 分钟间隔）
   - 上下文溢出处理，以 0.5 倍安全系数重试
   - 支持从 VS Code 编辑器发出的 yield 请求

5. 子 Agent 系统

   - SearchSubagentTool（searchSubagentTool.ts）
     - 为代码库研究运行嵌套的 ToolCallingLoop
     - 详尽程度：正常（1x）或深度（2x 轮次限制）
     - 向父 agent 返回综合搜索结果的摘要

   - ExecutionSubagentTool（executionSubagentTool.ts）
     - 在嵌套循环中运行终端命令
     - 捕获输出，将轨迹链接回父会话
     - 使用 CapturingToken 实现 OTel 追踪层级

   - Explore Agent（ExploreAgentProvider）
     - 功能标志控制（ConfigKey.ExploreAgentEnabled）
     - Plan Agent 的专用研究子 agent

6. 模型特定提示系统（promptRegistry.ts）

   每个模型族有自己的提示模板：
   - GPT-5 族：gpt5Prompt.tsx（305 行）
     - 用于计划的 CoreManageTodoList 工具
     - 详细的规划指导及示例
     - 进度更新、前导消息、最终答案格式化
   - GPT-5.1 Codex：gpt51CodexPrompt.tsx（受 Codex CLI 启发）
   - GPT-5.5：gpt55BasePrompt.tsx（生动个性，认知好奇）
   - Anthropic/Claude：anthropicPrompts.tsx（706 行）
     - 带延迟工具的工具搜索
     - 代码搜索模式指令
   - xAI/Grok：xAIPrompts.tsx
   - ZAI：zaiPrompts.tsx

7. 后台 TODO Agent（backgroundTodoAgent/）

   一个后台 LLM，维护待办列表而不阻塞主 agent：
   - 在队列中运行，在主 agent 每轮处理后执行
   - 仅在列表实际会变化时更新
   - 跟踪状态：未开始、进行中、已完成
   - 规则：从不创建单项目列表，最多 5 项，标题 3-8 个单词
   - 基于证据的完成（编辑/文件，而非探索）

8. Claude Code 集成（chatSessions/claude/）

   完整的 Claude Agent SDK 集成：
   - ClaudeAgentManager 管理生命周期
   - ClaudeCodeSession 封装 @anthropic-ai/claude-agent-sdk
   - 斜杠命令向导用于创建/管理子 agent
   - 工具使用前/后钩子
   - 通过 .jsonl 文件持久化会话

9. Cloud Agent（cloudAgentBackend.ts）

   将任务委托给 GitHub 的云端编码 agent：
   - Jobs API（基于 PR）和 Task API（基于任务）两种后端
   - 创建分支、实现变更、发起 PR
   - 在 VS Code 聊天中实时流式传输进度

10. 配置键（configurationService.ts）

    关键设置：
    - chat.agent.maxRequests（默认 200）
    - chat.advanced.enableAskAgent（基于实验）
    - chat.planAgent.model / chat.planAgent.additionalTools
    - chat.askAgent.model / chat.askAgent.additionalTools
    - chat.planAgent.defaultModel
    - chat.advanced.enableSwitchAgent（基于实验）
    - ConfigKey.ExploreAgentEnabled
    - ConfigKey.Advanced.SearchSubagentToolEnabled
    - ConfigKey.Advanced.ExecutionSubagentToolCallLimit

11. 提示结构（agentPrompt.tsx —— 958 行）

    主 AgentPrompt 元素：
    - 包含 copilot 身份、安全规则的系统消息
    - 工具前导指令
    - 规划指导（何时使用计划、示例）
    - 任务执行规则
    - 测试理念
    - 进度更新节奏
    - 最终答案格式化规则
    - 用于长对话的 SummarizedConversationHistory
    - 用于 Anthropic/OpenAI 缓存的缓存断点
    - 代码搜索模式变体（agentic Ask）

12. 意图系统（constants.ts）

    Intent 枚举包含：
    - AskAgent = 'askAgent'
    - Agent（主编码 agent）
    - EditCode、InlineChat 等

13. Agent 指令定位器（agentInstructionsLocator.ts）

    从工作区中发现 .github/copilot-instructions.md 和 agent 特定指令，用于自定义 agent 行为。

== 关键文件 ==

核心 agent 逻辑：
  extensions/copilot/src/extension/intents/node/agentIntent.ts（1386 行）
  extensions/copilot/src/extension/intents/node/toolCallingLoop.ts（2073 行）
  extensions/copilot/src/extension/prompts/node/agent/agentPrompt.tsx（958 行）

Agent 提供者：
  extensions/copilot/src/extension/agents/vscode-node/planAgentProvider.ts（268 行）
  extensions/copilot/src/extension/agents/vscode-node/askAgentProvider.ts（151 行）
  extensions/copilot/src/extension/agents/vscode-node/agentTypes.ts（120 行）
  extensions/copilot/src/extension/agents/vscode-node/promptFileContrib.ts（97 行）

子 Agent：
  extensions/copilot/src/extension/tools/node/searchSubagentTool.ts（308 行）
  extensions/copilot/src/extension/tools/node/executionSubagentTool.ts（183 行）
  extensions/copilot/src/extension/tools/vscode-node/switchAgentTool.ts（65 行）

模型提示：
  extensions/copilot/src/extension/prompts/node/agent/openai/gpt5Prompt.tsx（305 行）
  extensions/copilot/src/extension/prompts/node/agent/openai/gpt55BasePrompt.tsx（286 行）
  extensions/copilot/src/extension/prompts/node/agent/anthropicPrompts.tsx（706 行）

后台 agent：
  extensions/copilot/src/extension/prompts/node/agent/backgroundTodoAgent/（4 个文件）

Claude 集成：
  extensions/copilot/src/extension/chatSessions/claude/（完整 Claude Agent SDK）
