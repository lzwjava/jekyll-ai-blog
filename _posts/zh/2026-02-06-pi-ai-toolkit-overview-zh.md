---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Pi AI 智能体工具包概览
translated: true
type: note
---

我将为您获取并分析该 GitHub 仓库。让我获取详细的 README 和 AGENTS 文档，为您提供更全面的概览。

# Pi Monorepo - 综合介绍

**Pi-mono** 是由 Mario Zechner (badlogic) 创建的 AI agent 工具包，它提供了一个完整的生态系统，用于构建和部署 AI coding agents 以及管理 LLM 交互。它以 monorepo 结构组织，包含多个相互关联的 package。

## 核心理念

Pi 采用极简且可扩展的方法。它不捆绑所有可能的功能，而是提供强大的默认设置，并允许您通过 skills、extensions、prompt 模板或第三方 package 构建所需的功能。重点在于灵活性和实际可用性。

## 主要 Packages

### 1. **@mariozechner/pi-coding-agent** (旗舰项目)

一个在终端运行的交互式 coding agent CLI。这是大多数用户交互的主要产品。

**核心特性：**

- 四种运行模式：交互式 chat、print/JSON 输出、用于进程集成的 RPC 以及用于嵌入的 SDK
- 内置 tools：用于文件和系统操作的 `read`、`write`、`edit` 和 `bash`
- 支持多个 LLM provider，并具有自动 model 轮换功能
- 具有 branching、forking 和树状导航功能的 session 管理
- 通过 skills（prompt 增强）、extensions（自定义代码）和 packages 进行扩展

**基本用法：**

```bash
# 安装
npm install -g @mariozechner/pi-coding-agent

# 交互模式
pi "List all .ts files in src/"

# 非交互模式
pi -p "Summarize this codebase"

# 指定 model
pi --provider openai --model gpt-4o "Help me refactor"

# 只读模式
pi --tools read,grep,find,ls -p "Review the code"
```

### 2. **@mariozechner/pi-ai**

基础 LLM 工具包，为多个 provider 提供统一的 API。

**支持的 Providers：**

- OpenAI (GPT-4, GPT-4o, o1, o3-mini)
- Anthropic (Claude Opus, Sonnet, Haiku)
- Google (Gemini)
- xAI (Grok)
- Mistral
- OpenRouter
- Azure OpenAI
- 任何兼容 OpenAI API 的接口 (Ollama, vLLM, LM Studio)

**核心特性：**

- 使用 TypeBox schema 的类型安全 tool 定义
- Streaming 和 completion API
- 具有自动 tool 执行功能的内置 agent loop
- Tool 参数验证
- 可序列化的会话上下文

### 3. **@mariozechner/pi-agent**

核心 agent runtime，提供状态管理和 tool 执行统筹。

**功能：**

- 带有验证的 tool 调用
- 跨轮次的状态管理
- 事件驱动架构
- 与 pi-ai 层集成

### 4. **@mariozechner/pi-tui**

一个具有差异渲染功能的终端 UI 库，用于构建响应式 CLI 界面。

**特性：**

- 高效的屏幕更新（仅渲染更改部分）
- 自定义组件系统
- 输入处理
- 被 coding agent 用于其交互界面

### 5. **@mariozechner/pi-web-ui**

用于在浏览器中构建 AI chat 界面的 Web components。

### 6. **@mariozechner/pi-mom**

一个将消息委派给 pi coding agent 的 Slack bot，实现通过 Slack 进行团队协作。

### 7. **@mariozechner/pi-proxy**

用于在不暴露 key 的情况下进行基于浏览器的 LLM API 调用的 CORS 代理（尽管生产级应用应使用正式的后端）。

### 8. **@mariozechner/pi** (pi-pods)

用于在 GPU pods 上管理 vLLM 部署的 CLI 工具，适用于自托管 models。

## 扩展系统

### Skills

增强 agent 能力的 prompt 模板或指令。它们被加载并注入到 system prompt 中。

### Extensions

通过事件钩入 agent 生命周期的 TypeScript/JavaScript 代码：

- `session_start`, `session_switch`, `session_fork`
- `input`, `before_agent_start`, `agent_start`
- `turn_start`, `context`, `tool_call`, `tool_result`, `turn_end`
- `agent_end`, `session_compact`

Extensions 可以：

- 注册自定义命令（例如 `/mycommand`）
- 添加自定义 tools
- 拦截并修改消息
- 创建 UI widgets
- 响应用户输入

### Pi Packages

通过 npm 或 git 分发的共享包，包含 extensions、skills、prompts 和 themes。

```bash
# 从 npm 安装
pi install npm:@foo/pi-tools

# 从 git 安装
pi install git:github.com/user/repo

# 本地开发
pi install /path/to/local/package
```

**安全提示：** Extensions 以全系统权限运行，可以执行任意代码。请仅从受信任的来源安装。

## 配置与自定义

### Model 配置

通过 `~/.pi/agent/models.json` 添加自定义 models：

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        { "id": "llama3.1:8b" },
        { "id": "qwen2.5-coder:7b" }
      ]
    }
  }
}
```

### 身份验证

Model 需要通过以下方式进行身份验证：

- 订阅登录（`/login` 命令）
- API keys（环境变量或显式配置）

### 设置

通过命令配置行为：

- `/settings` - 打开设置 UI
- `/model` 或 `Ctrl+L` - 选择 model
- `/tools` - 配置可用 tools
- `/theme` - 更改外观

### 环境变量

- `PI_CODING_AGENT_DIR` - 配置目录 (默认为 `~/.pi/agent`)
- `PI_CACHE_RETENTION` - 缓存策略 (`long` 为延长, `short` 为最小化)
- `PI_SKIP_VERSION_CHECK` - 跳过启动版本检查
- `VISUAL` / `EDITOR` - 用于 `Ctrl+G` 的外部编辑器

## 开发工作流

该 monorepo 使用同步版本系统，所有 package 保持相同的版本号。

```bash
# 设置
npm install
npm run build

# 开发
npm run dev              # 所有 package 的监听模式
./pi-test.sh            # 从源码运行

# 测试
./test.sh               # 非 LLM 测试（无需 API keys）
npm test                # 所有测试

# 版本管理
npm run version:patch   # 0.7.5 → 0.7.6
npm run version:minor   # 0.7.5 → 0.8.0
npm run version:major   # 0.7.5 → 1.0.0

# 发布
npm run publish         # 发布所有 package 到 npm
```

## SDK 用法

将 pi 嵌入到您自己的应用程序中：

```typescript
import { createPiSession } from '@mariozechner/pi-coding-agent';

const session = await createPiSession({
  cwd: process.cwd(),
  model: { provider: 'anthropic', id: 'claude-opus-4-5' }
});

// 发送消息并处理 streaming
await session.sendMessage('Help me refactor this function', {
  onText: (text) => console.log(text),
  onToolCall: (tool) => console.log(`Using tool: ${tool.name}`)
});

// 干预或后续跟进
await session.steer('New instruction');
await session.followUp('After you\'re done, also do this');
```

## 平台支持

- **Windows**: 完全支持
- **Linux/macOS**: 原生支持
- **Termux (Android)**: 兼容
- 提供各种终端模拟器的设置指南

## 实际应用

Pi 已积极应用于生产环境。请参阅 [openclaw/openclaw](https://github.com/openclaw/openclaw) 了解实际的 SDK 集成案例。

## 社区与资源

- **License**: MIT
- **Stars**: GitHub 上 397+
- **活跃开发**: 定期发布（当前版本 v0.12.14）
- **文档**: `/packages/coding-agent/docs/` 中的全面文档
- **Discord**: 社区讨论和 package 发现

## 为什么选择 Pi？

Pi 的出色之处在于：

- 跨多个 LLM provider 的**统一 API**
- 通过设计良好的插件系统实现的**可扩展性**
- 具有出色 TUI 的**终端优先**方法
- 具有完善 tool 执行功能的**真实 agent 能力**
- 带有嵌入式 SDK 的**生产就绪**特性
- **积极的维护**和不断增长的生态系统

无论您是需要一个强大的编码助手，还是想要构建自定义 AI 工具，或是管理 LLM 部署，pi-mono 都能提供所需的基础模块。
