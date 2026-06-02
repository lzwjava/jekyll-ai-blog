---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建 Claude 代码插件指南
translated: true
type: note
---

**问题：** 如何为 Claude Code 制作插件，以及我们可以使用哪些 API 来与 Claude Code 集成？

**回答：**

**Claude Code** 是 Anthropic 的 agentic coding tool（基于终端，支持 VS Code / JetBrains 扩展），它允许 Claude 阅读/编辑文件、运行命令并处理开发工作流。

插件通过自定义 **slash commands** (`/something`)、**skills**、**agents**、**hooks**，有时还有 MCP (multi-step process) 服务器或 LSP 集成来扩展它。

### 如何创建 Claude Code 插件（2026 当前方法）

插件主要是 **file-based**（Markdown + JSON）——大多数情况下无需进行繁重的编译。

#### 创建简单插件的基本步骤

1. **创建目录结构**
   ```
   mkdir my-awesome-plugin
   cd my-awesome-plugin
   mkdir -p .claude-plugin
   ```

2. **创建 manifest 文件**
   这是必需的——将其放置在 `.claude-plugin/plugin.json`

   最小示例：
   ```json
   {
     "name": "my-awesome-plugin",
     "version": "1.0.0",
     "description": "Adds /greet and a session summary skill",
     "author": "Your Name",
     "repository": "https://github.com/yourname/my-awesome-plugin"
   }
   ```

3. **添加功能**（根据需要选择）

   - **Slash commands** — 将 Markdown 文件放入 `commands/`
     示例：`commands/greet/COMMAND.md`
     ```markdown
     ---
     description: Prints a friendly greeting
     ---

     Greet the user warmly and ask how their coding is going today.
     ```

   - **Skills** — 放入 `skills/skill-name/SKILL.md`
     Skills 是可重用的 prompt templates/behaviors。

   - **Hooks**（在事件如 session-start 时运行）— 放入 `hooks/`

   - 更高级：agents、MCP 服务器、LSP 服务器（详见文档）

4. **本地测试**
   使用插件文件夹启动 Claude Code：
   ```
   claude --plugin-dir ./my-awesome-plugin
   ```
   或者将其添加为本地 marketplace 以便更容易测试。

5. **分享 / 分发**
   - 推送到 GitHub
   - 其他人通过以下方式安装：
     ```
     /plugin marketplace add https://github.com/yourname/my-awesome-plugin
     /plugin install my-awesome-plugin
     ```
   - 或者创建 **marketplace**（包含多个插件的 repo），使用 `marketplace.json`

许多人从 `~/.claude/` 中的 **standalone skills/commands** 开始，后来转换为插件。

### 可以用哪些 API 与 / 扩展 Claude Code？

Claude Code 本身 **不** 暴露传统的公共 REST API 用于插件（大多数扩展是声明式的 Markdown + JSON）。

然而，存在几个集成点：

- **Anthropic API (Messages / Tool Use API)**
  构建自定义 agents/tools 与 Claude 模型交互的核心方式。
  您可以构建外部 tools/servers，Claude Code 通过 **tool use** 调用它们。

- **Code Execution Tool** (in API: `code_execution_20250825`)
  允许 Claude 在 sandbox 中运行 Python/Node/Bash——许多插件间接利用由此驱动的模型能力。

- **Computer Use Tool** (beta)
  允许 Claude 控制桌面（截图、鼠标、键盘）。
  对于非常高级的自动化插件很有用。

- **MCP Servers** (Multi-step Custom Processes)
  您可以编写轻量级 HTTP 服务器，Claude Code 在复杂工作流中调用它们。

- **Agent SDK** (for programmatic control)
  允许以编程方式加载插件并从代码构建自定义 Claude Code 会话。

- **External APIs via Tool Use**
  您以标准的 Anthropic tool-use 格式定义 tools → Claude 决定何时调用它们 → 您的代码执行 API 调用（GitHub、天气、数据库、Slack 等）。

对于 2026 年的大多数插件作者，您 **无需** 编写 API 服务器——只需编写优秀的 Markdown prompts/commands/skills。
如果需要深度编程集成（调用外部 API、持久状态等），请结合 **tool use + 您自己的 backend**。

**官方起点**
→ https://code.claude.com/docs/en/plugins

**示例与灵感**
在 GitHub 上搜索 "claude-code-plugin" 或访问社区 marketplace 如 buildwithclaude.com

参考资料：

- [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [How to Build Claude Code Plugins: A Step-by-Step Guide | DataCamp](https://www.datacamp.com/tutorial/how-to-build-claude-code-plugins)
- [How to Build Your Own Claude Code Plugin (Complete Guide) | Agnost AI Blog](https://agnost.ai/blog/claude-code-plugins-guide)
- [Code execution tool - Anthropic Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Computer use tool - Anthropic Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
