---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 禁用Claude代码编辑确认弹窗
translated: true
type: note
---

要禁用 Claude Code 中的编辑确认弹窗（使其能直接对 `sync_githook.py` 等文件应用编辑而无需询问），您需要在 `settings.json` 文件中配置权限。这就是您提到的 "Claude Code JSON"——它是 Claude Code 用于用户级配置的主设置文件。

### 设置步骤

1. **定位或创建文件**：
   - 文件位于 `~/.claude/settings.json`（macOS/Linux）或 `%USERPROFILE%\.claude\settings.json`（Windows）。`.claude` 文件夹是隐藏的，请使用终端/文件资源管理器导航到该位置。
   - 如果文件或文件夹不存在，请创建它们。您可以在 Claude Code 的交互式 REPL 中运行 `/config` 命令来完成此操作（它会引导您打开设置界面）。

2. **编辑 JSON**：
   - 在任何文本编辑器（如 VS Code）中打开 `settings.json`。
   - 添加或更新 `permissions` 部分以自动批准编辑。以下是一个简单的配置，用于禁用所有编辑操作的提示：

     ```json:disable-run
     {
       "permissions": {
         "defaultMode": "acceptEdits",
         "allow": [
           "Edit(*)",
           "Write(*)",
           "MultiEdit(*)"
         ],
         "ask": []
       }
     }
     ```

     - **此配置的作用**：
       - `"defaultMode": "acceptEdits"`：将全局默认设置为无需提示即接受编辑。
       - `"allow"`：预先批准特定工具，如 `Edit`（用于单文件编辑）、`Write`（用于写入内容）和 `MultiEdit`（用于批量更改）对任何文件（`*` 通配符）的操作。
       - `"ask": []`：确保除非在其他地方明确拒绝，否则不会触发任何操作的提示。
     - 保存文件。更改将在您的下一个 Claude Code 会话中立即生效。

3. **测试**：
   - 重启 Claude Code 或重新加载会话。
   - 要求它编辑一个文件（例如，"编辑 sync_githook.py 以添加注释"）。它应该在没有弹窗的情况下应用更改。
   - 如果您需要项目特定设置（例如，仅针对此仓库），请在项目根目录中创建 `.claude/settings.json`。

4. **可选调整**：
   - 如需更精细的控制（例如，仅允许在特定目录中编辑）：将 `"Edit(*)"` 更改为 `"Edit(./src/**)"`。
   - 如果提示仍然存在，请在 REPL 中运行 `/allowed-tools` 以检查当前规则，或使用 `/config` 通过 UI 进行调整。
   - 出于安全考虑，避免过于宽泛的 `allow` 规则——从简单开始逐步扩展。

这应该能让您的工作流程更快且无中断。如果您处于企业设置中，请与管理员核实，因为托管策略可能会覆盖用户设置。

[Claude Code 设置文档](https://docs.claude.com/en/docs/claude-code/settings)
[禁用 Claude Code 权限提示指南](https://www.arsturn.com/blog/how-to-disable-claude-code-permission-prompts)
