---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 企业级 VSCode Copilot Chat 设置指南
translated: true
type: note
---

**Question:** 哪些重要的 VSCode Copilot Chat 设置（特别是 auto-approve 和 `settings.json` 配置）有助于在企业环境中提高 Copilot 的实用性？

---

**Answer:**

## 企业级 VSCode Copilot Chat 设置指南

了解 `settings.json` 中的关键设置可以让团队获得一致、安全且高效的 Copilot 体验。以下是按类别分组的详细配置说明。

---

### 1. Agent Mode 核心设置

Agent mode 从 VS Code 1.99 版本开始可用。要启用它，请使用 `chat.agent.enabled` 设置。企业可以通过设备管理集中启用或禁用 agent mode。

关键设置：

```json
"chat.agent.enabled": true,
"chat.agent.maxRequests": 25
```

默认的 `maxRequests` 为 15。将其增加到 50 左右可以支持更长的连续工作流 —— 数值越大，Copilot 持续编写代码的时间越长，但也越容易触发 Copilot 的 request limits。

---

### 2. Auto-Approve 设置（企业环境中最重要）

需要了解 **三个层级** 的 auto-approval：

#### A. 全局 Auto-Approve（终极选项 —— 谨慎使用）

启用 `chat.tools.global.autoApprove` 可自动批准所有 workspace 中的所有 tools。你也可以直接在 chat 中通过 `/yolo` 或 `/autoApprove` slash commands 来开启，或者使用 `/disableYolo` 或 `/disableAutoApprove` 来关闭。这些操作都会禁用手动审批提示（包括潜在的破坏性操作），请务必在了解后果的情况下使用。

```json
"chat.tools.global.autoApprove": false   // 建议：在企业环境中保持 false
```

#### B. Terminal 命令 Auto-Approve（细粒度且推荐）

通过 `chat.tools.terminal.autoApprove` 配置哪些 terminal commands 可以自动执行。将命令设为 `true` 表示自动批准，`false` 表示拦截。默认情况下，模式匹配针对单个 subcommands。对于高级场景，可以使用带有 `matchCommandLine` 属性的对象语法来匹配完整的 command line。

企业安全示例：

```json
"chat.tools.terminal.autoApprove": {
  // 安全的只读 git 命令
  "/^git\\s+(status|diff|log|show)\\b/": true,
  // 安全的 build/test 命令
  "/^npm\\s+(test|run\\s+lint)\\b/": true,
  "/^pnpm\\s+(test|lint)\\b/": true,
  "/^mvn\\s+test\\b/": true,
  "mkdir": true,
  // 拦截破坏性命令
  "rm": false,
  "rmdir": false,
  "del": false,
  "kill": false,
  "chmod": false,
  "chown": false,
  "curl": false,
  "wget": false,
  "eval": false,
  "/^Remove-Item\\b/i": false,
  "/^git\\s+(push|reset|revert|clean)\\b/": false
}
```

Regex 键需要包裹在 `/…/` 中。任何未匹配的内容都将回退到正常的确认对话框。

#### C. Terminal 启用/禁用 Auto-Approve（组织级策略）

组织和个人可以通过 `chat.tools.terminal.enableAutoApprove` 开启或关闭 terminal 自动批准功能，该功能提供了改进的规则 UI 和安全警告。

```json
"chat.tools.terminal.enableAutoApprove": true
```

#### D. 基于 URL 的 Auto-Approve

`chat.tools.urls.autoApprove` 设置存储自动批准的 URL 模式。其值可以是布尔值，也可以是包含 `approveRequest` 和 `approveResponse` 属性的对象以进行细粒度控制。支持精确 URL、glob 模式或通配符。

```json
"chat.tools.urls.autoApprove": {
  "https://www.example.com": false,
  "https://*.contoso.com/*": true,
  "https://example.com/api/*": {
    "approveRequest": true,
    "approveResponse": false
  }
}
```

#### E. 敏感文件编辑确认

通过 `chat.tools.edits.autoApprove` 设置，你可以配置特定的文件模式，指定哪些文件在 agent mode 进行更改之前必须经过显式确认。

---

### 3. MCP (Model Context Protocol) 设置

```json
"chat.mcp.access": true,
"chat.mcp.discovery.enabled": false,     // 出于安全考虑禁用自动发现
"chat.mcp.gallery.enabled": false,        // 在企业环境中禁用公开库
"chat.mcp.autoStart": "newAndOutdated"
```

---

### 4. Agent 行为与工作流设置

```json
"github.copilot.chat.agent.autoFix": true,          // 编辑后自动修复错误
"github.copilot.chat.agent.thinkingTool": false,     // 禁用扩展思考（成本控制）
"github.copilot.chat.virtualTools.threshold": 128,   // 每次请求的最大 tools 数量（上限：128）
"chat.agent.thinkingStyle": "fixedScrolling",
"chat.agent.todoList.position": "default"
```

---

### 5. Custom Instructions 与组织 Agents

要启用组织级自定义 agents 的发现功能，请将 `github.copilot.chat.organizationCustomAgents.enabled` 设置为 `true`。Custom agent 文件使用 `.agent.md` 格式，并可放置在由 `chat.agentFilesLocations` 配置的 workspace 或用户配置文件路径中。

```json
"github.copilot.chat.organizationCustomAgents.enabled": true
```

---

### 6. Inline Chat 与编辑器补全

```json
"inlineChat.finishOnType": false,
"inlineChat.holdToSpeech": true,
"editor.inlineSuggest.syntaxHighlightingEnabled": true,
"github.copilot.enable": {
  "*": true,
  "plaintext": false,
  "markdown": true,
  "yaml": true
}
```

---

### 7. 企业级 Workspace 策略

对于受监管的项目，在 `.vscode/` 目录下保留一份共享的 `settings.json`，然后允许开发者在个人配置文件中扩展个人偏好。这样你可以锁定 agent tooling（例如禁止破坏性的 shell 命令），同时仍允许个人试验 chat 或 inline suggestion 偏好。建议每季度回顾一次配置 —— 许多 Copilot 功能仍处于 preview 阶段，行为可能会发生变化。

将策略文件放置在仓库的 `.vscode/settings.json` 并提交，以便所有团队成员继承相同的默认值。

---

### 8. 重置 Tool 审批

要清除所有已保存的 tool 审批记录，请使用 Command Palette 中的 **Chat: Reset Tool Confirmations** 命令（Windows/Linux 为 `Ctrl+Shift+P`，macOS 为 `Cmd+Shift+P`）。

---

### 总结：推荐的企业级 `settings.json` 基准配置

```json
{
  // Agent Mode
  "chat.agent.enabled": true,
  "chat.agent.maxRequests": 25,
  "github.copilot.chat.agent.autoFix": true,

  // Auto-Approve: 企业保守配置
  "chat.tools.global.autoApprove": false,
  "chat.tools.terminal.enableAutoApprove": true,
  "chat.tools.terminal.autoApprove": {
    "/^git\\s+(status|diff|log|show)\\b/": true,
    "/^npm\\s+(test|run\\s+lint)\\b/": true,
    "rm": false,
    "del": false,
    "kill": false,
    "chmod": false,
    "curl": false,
    "eval": false,
    "/^git\\s+(push|reset|clean)\\b/": false
  },

  // MCP: 受控访问
  "chat.mcp.access": true,
  "chat.mcp.discovery.enabled": false,
  "chat.mcp.gallery.enabled": false,

  // Org Agents
  "github.copilot.chat.organizationCustomAgents.enabled": true,

  // Inline
  "inlineChat.finishOnType": false,
  "editor.inlineSuggest.syntaxHighlightingEnabled": true
}
```

---

**参考资料：**

- [VSCode Official: Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [VSCode Official: Tools in Chat (Auto-Approve)](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [VSCode Copilot Settings Reference](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
- [VSCode: Use Tools in Chat](https://code.visualstudio.com/docs/copilot/chat/chat-tools)
- [Tune GitHub Copilot Settings in VS Code — DEV Community](https://dev.to/pwd9000/tune-github-copilot-settings-in-vs-code-32kp)
- [YOLO/Auto-Approve Gist by intellectronica](https://gist.github.com/ichim-david/8c2ad537068137a658d938b229d3adef)
- [GitHub Copilot v1.104 Changelog](https://github.blog/changelog/2025-09-12-github-copilot-in-vs-code-august-release-v1-104/)
