---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enterprise VSCode Copilot Chat Settings Guide
translated: false
type: note
---

**Question:** What are the important VSCode Copilot Chat settings, especially auto-approve and `settings.json` configurations, that help make Copilot more useful in enterprise environments?

---

**Answer:**

## VSCode Copilot Chat Settings for Enterprise Use

Understanding the key settings in `settings.json` gives teams consistent, safe, and productive Copilot behavior. Here is a comprehensive breakdown grouped by category.

---

### 1. Agent Mode Core Settings

Agent mode is available starting from VS Code 1.99. To enable it, use the `chat.agent.enabled` setting. Organizations can centrally enable or disable agent mode via device management.

Key settings:

```json
"chat.agent.enabled": true,
"chat.agent.maxRequests": 25
```

The default `maxRequests` is 15. Increasing it to around 50 allows for longer continuous work sessions — the larger the value, the longer Copilot will continue coding, but also the easier it is to hit Copilot's request limits.

---

### 2. Auto-Approve Settings (The Most Important for Enterprise)

There are **three layers** of auto-approval to understand:

#### A. Global Auto-Approve (Nuclear Option — Use with Caution)

Enable `chat.tools.global.autoApprove` to auto-approve all tools across all workspaces. You can also toggle this directly from chat by using `/yolo` or `/autoApprove` slash commands to enable it, or `/disableYolo` or `/disableAutoApprove` to disable it. Both approaches disable manual approval prompts, including for potentially destructive actions — only use these if you understand the implications.

```json
"chat.tools.global.autoApprove": false   // Recommended: keep false for enterprise
```

#### B. Terminal Command Auto-Approve (Granular & Recommended)

You can configure which terminal commands are automatically approved using `chat.tools.terminal.autoApprove`. Set commands to `true` to automatically approve them, and `false` to block them. By default, patterns match against individual subcommands. For advanced scenarios, use object syntax with the `matchCommandLine` property to match against the full command line.

Enterprise-safe example:

```json
"chat.tools.terminal.autoApprove": {
  // Safe read-only git commands
  "/^git\\s+(status|diff|log|show)\\b/": true,
  // Safe build/test commands
  "/^npm\\s+(test|run\\s+lint)\\b/": true,
  "/^pnpm\\s+(test|lint)\\b/": true,
  "/^mvn\\s+test\\b/": true,
  "mkdir": true,
  // BLOCK destructive commands
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

Regex keys are wrapped in `/…/`. Anything not matched falls back to the normal confirmation dialog.

#### C. Terminal Enable/Disable Auto-Approve (Org-level Policy)

Organizations and individuals can enable or disable terminal auto-approve via `chat.tools.terminal.enableAutoApprove`, with improved UI for rules and security warnings.

```json
"chat.tools.terminal.enableAutoApprove": true
```

#### D. URL-Based Auto-Approve

The `chat.tools.urls.autoApprove` setting stores auto-approve URL patterns. The value can be a boolean or an object with `approveRequest` and `approveResponse` properties for granular control. Exact URLs, glob patterns, or wildcards are supported.

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

#### E. Sensitive File Edit Confirmation

With the `chat.tools.edits.autoApprove` setting, you can configure file patterns that indicate which files require explicit confirmation before agent mode makes changes to them.

---

### 3. MCP (Model Context Protocol) Settings

```json
"chat.mcp.access": true,
"chat.mcp.discovery.enabled": false,     // Disable auto-discovery for security
"chat.mcp.gallery.enabled": false,        // Disable public gallery for enterprise
"chat.mcp.autoStart": "newAndOutdated"
```

---

### 4. Agent Behavior & Workflow Settings

```json
"github.copilot.chat.agent.autoFix": true,          // Auto-fix errors after edits
"github.copilot.chat.agent.thinkingTool": false,     // Disable extended thinking (cost control)
"github.copilot.chat.virtualTools.threshold": 128,   // Max tools per request (limit: 128)
"chat.agent.thinkingStyle": "fixedScrolling",
"chat.agent.todoList.position": "default"
```

---

### 5. Custom Instructions & Organization Agents

To enable discovery of organization-level custom agents, set `github.copilot.chat.organizationCustomAgents.enabled` to `true`. Custom agent files use `.agent.md` format and can be placed in workspace or user profile locations configured by `chat.agentFilesLocations`.

```json
"github.copilot.chat.organizationCustomAgents.enabled": true
```

---

### 6. Inline Chat & Editor Completions

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

### 7. Enterprise Workspace Strategy

Keep a shared `settings.json` in `.vscode/` for regulated projects, then let developers extend personal preferences in their user profile. This lets you lock down agent tooling (such as disallowing destructive shell commands) while still letting individuals experiment with chat or inline suggestion preferences. Revisit the configuration quarterly — many Copilot features are still in preview and can change behavior.

Place the policy file at `.vscode/settings.json` in your repo and commit it so all teammates inherit the same defaults.

---

### 8. Resetting Tool Approvals

To clear all saved tool approvals, use the **Chat: Reset Tool Confirmations** command in the Command Palette (`Ctrl+Shift+P` on Windows/Linux, `Cmd+Shift+P` on macOS).

---

### Summary: Recommended Enterprise `settings.json` Baseline

```json
{
  // Agent Mode
  "chat.agent.enabled": true,
  "chat.agent.maxRequests": 25,
  "github.copilot.chat.agent.autoFix": true,

  // Auto-Approve: Conservative for enterprise
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

  // MCP: Controlled access
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

**References:**

- [VSCode Official: Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [VSCode Official: Tools in Chat (Auto-Approve)](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [VSCode Copilot Settings Reference](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
- [VSCode: Use Tools in Chat](https://code.visualstudio.com/docs/copilot/chat/chat-tools)
- [Tune GitHub Copilot Settings in VS Code — DEV Community](https://dev.to/pwd9000/tune-github-copilot-settings-in-vs-code-32kp)
- [YOLO/Auto-Approve Gist by intellectronica](https://gist.github.com/ichim-david/8c2ad537068137a658d938b229d3adef)
- [GitHub Copilot v1.104 Changelog](https://github.blog/changelog/2025-09-12-github-copilot-in-vs-code-august-release-v1-104/)
