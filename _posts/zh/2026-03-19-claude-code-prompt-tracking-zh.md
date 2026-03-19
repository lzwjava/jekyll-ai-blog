---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude 代码提示跟踪工具概述
translated: true
type: note
---

**问题：** 有没有现有的工具或项目，用于记录 Claude Code（以及 VS Code 中的 GitHub Copilot）的所有请求和响应，以跟踪和改进提示？是否有可能构建一个自定义的全栈系统来实现这个？

**答案：**

## 概述

是的——这个领域已经相当成熟。每个层面都有工具：开源 CLI 日志记录器、官方遥测管道、托管 SaaS 可观测性平台，以及专为提示管理构建的系统。下面是结构化的分解。

---

## 第一部分：Claude Code —— 现有工具与方法

### A. 原生 JSONL 记录（内置）

Claude Code 会自动将所有对话记录写入磁盘上的 JSONL 文件，路径为 `~/.claude/projects/`。每个提示、响应和工具调用都存储在那里。这是构建自己系统的最低摩擦起点——无需代理。

### B. 开源 CLI 日志记录器

**`claude-code-logger`** (GitHub: dreampulse/claude-code-logger)  
一个 CLI 代理工具，拦截所有 Claude Code 流量。它运行本地代理服务器，您只需将 `ANTHROPIC_BASE_URL` 指向它。功能包括聊天模式可视化、AI 响应的 markdown 渲染、工具使用跟踪、请求/响应体日志记录，以及 SSE（流式传输）合并。这是您想要构建的最接近的东西——一个中间人日志记录器。

**`claude-code-log`** (GitHub: daaain/claude-code-log)  
一个 Python CLI 工具，将 Claude Code 的 JSONL 记录转换为可读的 HTML 文件。它支持项目层次处理、会话导航、token 使用跟踪、日期过滤，以及交互式 TUI 界面。

**`claude-trace`** (by Mario Zechner)  
一个工具，通过 monkeypatch Claude Code 内部的 `fetch` 来拦截客户端与 Anthropic 服务器之间的所有请求-响应对，并将它们写入磁盘上的 JSONL 文件。这会捕获系统提示、工具定义和完整对话——提供完全内省，包括通常不可见的内容。

### C. 官方 OpenTelemetry (OTEL) 管道

Claude Code 在配置 `OTEL_LOGS_EXPORTER` 时通过 OpenTelemetry 导出事件。关键事件包括 `claude_code.user_prompt`（用户提交提示时）、`claude_code.api_request`（每个 API 调用）和 `claude_code.tool_result`（工具执行完成）。您可以设置 `OTEL_LOG_TOOL_DETAILS=1` 来包含 MCP 服务器/工具名称。

推荐的开源栈将数据路由通过：Claude Code → OpenTelemetry Collector → Prometheus (metrics) + Loki (events/logs) → Grafana (visualization)。您可以通过 `CLAUDE_CODE_ENABLE_TELEMETRY=1` 启用它。

### D. Claude Code 的托管 SaaS 选项

**LangSmith (LangChain)**  
LangSmith 通过 Stop hook 支持跟踪 Claude Code，它读取生成的对话记录，将消息转换为 LangSmith runs，并发送到项目。跟踪包括用户消息、工具调用和助手响应，通过 `.claude/settings.local.json` 中的 `TRACE_TO_LANGSMITH=true` 按项目启用。

**Datadog AI Agents Console**  
Datadog 的 AI Agents Console 聚合 Claude Code 性能指标，包括延迟百分位数、错误率、失败的 bash 命令，以及按仓库的请求，提供项目级洞察。

**Dev-Agent-Lens (Arize)**  
一个基于开源代理的层，将 Claude Code 请求路由通过 LiteLLM，发出 OpenTelemetry 和 OpenInference spans，并发送到 Arize AX 或本地 Phoenix。它捕获流式响应、嵌套工具调用和内部调用——标准日志遗漏的内容。

---

## 第二部分：VS Code 中的 GitHub Copilot —— 可能实现什么

### A. 内置日志记录（诊断模式）

VS Code 提供工具来检查发送提示时发生的情况。您可以通过命令面板（`Developer: Set Log Level`）将 GitHub Copilot 和 GitHub Copilot Chat 扩展的日志级别设置为 `Trace`，然后在 Output 面板查看输出。还有一个 “Agent Debug” 面板，显示代理交互的时序事件日志，包括工具调用序列、LLM 请求、token 使用、提示文件发现和错误。

### B. 主要限制

与 Claude Code 不同，**Copilot 不提供开放 API 来捕获完整的请求/响应对**。Copilot 将所有请求路由通过专有的 Copilot 代理服务器，该服务器处理限流、认证和安全检查，然后转发到 LLM 后端。流量端到端加密。这意味着您无法轻松拦截原始提示+响应，而无需企业 MITM 代理（例如 Zscaler）。

### C. Copilot 可以跟踪的内容

- **使用配额**（已用请求、token 配额）：通过 VS Code 状态栏仪表板和 GitHub API 端点 `https://api.github.com/copilot_internal/user`。有一个开源 VS Code 扩展 `copilot-usage-tracker`，使用 VS Code 的 GitHub 认证提供商实时跟踪高级请求使用。
- **代理会话日志**：对于 Copilot 编码代理，您可以直接在 VS Code 中点击 Agent sessions 面板查看会话日志，并实时查看 Copilot 提交背后的理由。
- **诊断日志文件**，存储在 VS Code 的标准扩展日志位置——适用于调试，但未结构化为提示改进。

**Copilot 底线**：您无法从 VS Code 捕获单个建议级别的原始提示/响应对。您只能跟踪使用指标和代理模式会话日志。

---

## 第三部分：专属提示管理平台（SaaS）

如果您的目标是专门**提示改进和迭代跟踪**（而非仅原始日志记录），这些平台是为此专为构建的：

| Platform | Key Strength | Open Source? |
|---|---|---|
| **PromptLayer** | 中间件层，记录所有 LLM 请求，支持非技术提示迭代、A/B 测试和版本控制，通过视觉仪表板 | No |
| **Langfuse** | 开源 LLM 可观测性，详细跟踪、成本跟踪、延迟监控和提示版本控制 | Yes |
| **LangSmith** | 擅长日志记录、可追溯性、对提示性能的深度洞察、系统调试和优化 | No |
| **Datadog LLM Observability** | 将提示版本与性能指标相关联——延迟、token 成本、错误率——跨生产流量 | No |
| **Lilypad** | 将 LLM 调用包装在 Python 函数中，自动版本化所有更改，捕获完整执行上下文，以便每个输出可跟踪和重现 | Yes |

---

## 第四部分：是否应该构建自定义全栈系统？

**是的，如果：**
- 您想跟踪特定于**团队工作流程**的 Claude Code 提示（例如，按项目、开发者、结果质量标记）
- 您想要**超出原始日志的提示改进工作流程**——评分、注释、建议重写
- 您想将 Claude Code 日志与 Copilot 使用数据结合在一个仪表板中

**构建自己的推荐架构：**

```
Claude Code (OTEL or JSONL) 
    ↓
后端 API (Node.js / FastAPI)
    ↓
数据库 (PostgreSQL 用于结构化数据 + 全文搜索)
    ↓
前端仪表板 (Next.js)
  - 查看所有会话 + 提示
  - 评分响应 (好/坏)
  - 注释和版本化提示
  - 并排比较提示版本
  - Token/成本分析
```

对于 Claude Code，具体来说，最简单的数据源是 **`~/.claude/projects/` JSONL 文件**——无需代理设置。您可以构建一个文件监视后端，以近实时摄入新会话。

对于 Copilot，您限于：代理会话日志（编码代理模式）+ 通过 GitHub API 的使用配额。没有企业网络代理，完整提示/响应捕获不可行。

---

**参考资料：**

- [Claude Code Official Monitoring Docs](https://code.claude.com/docs/en/monitoring-usage)
- [claude-code-logger (GitHub)](https://github.com/dreampulse/claude-code-logger)
- [claude-code-log (GitHub)](https://github.com/daaain/claude-code-log)
- [claude-trace / cchistory writeup](https://mariozechner.at/posts/2025-08-03-cchistory/)
- [Claude Code + OpenTelemetry + Grafana guide](https://quesma.com/blog/track-claude-code-usage-and-limits-with-grafana-cloud/)
- [LangSmith Claude Code Tracing](https://docs.langchain.com/langsmith/trace-claude-code)
- [Dev-Agent-Lens (Arize)](https://arize.com/blog/claude-code-observability-and-tracing-introducing-dev-agent-lens/)
- [Datadog Claude Code Monitoring](https://www.datadoghq.com/blog/claude-code-monitoring/)
- [PromptLayer](https://www.promptlayer.com/)
- [Langfuse](https://langfuse.com/)
- [Top 5 Prompt Management Platforms 2025](https://www.getmaxim.ai/articles/top-5-prompt-management-platforms-in-2025/)
- [VS Code Copilot Troubleshooting / Agent Debug](https://code.visualstudio.com/docs/copilot/troubleshooting)
- [copilot-usage-tracker (GitHub)](https://github.com/ethanhubin/copilot-usage-tracker)
- [GitHub Copilot Chat: Life of a Prompt](https://devblogs.microsoft.com/all-things-azure/github-copilot-chat-explained-the-life-of-a-prompt/)