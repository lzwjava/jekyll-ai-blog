---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GitHub Copilot 扩展疑难解答指南
translated: true
type: note
---

问题：为什么 Windows 上的 VS Code 中的 GitHub Copilot 扩展有时会无响应，需要我打开一个新窗口，并且我无法在 Ask 和 Agent 模式之间切换？

回答：

Visual Studio Code (VS Code) 中的 GitHub Copilot 扩展在 Windows 上变得无响应或冻结可能是由于几个常见问题造成的，尤其是在使用 Chat 视图（具有 Ask 提问、Edit 修改代码或 Agent 自主任务等模式）等功能时。这通常表现为界面卡顿，需要完全重新加载或打开一个新窗口来解决，并且由于扩展主机进程卡住而无法在模式之间进行切换。根据用户报告和官方故障排除，最可能的原因和修复方法如下：

### 常见原因
- **扩展或 VS Code 缓存/加载问题**：Copilot 的聊天功能依赖于后台进程来处理 AI 请求。如果这些进程卡住（例如，在 Agent 模式下执行长时间任务时），UI 就会冻结。在 Agent 任务运行时切换窗口或选项卡会中断进程，从而加剧此问题。
- **过时或冲突的版本**：不兼容的 VS Code 或 Copilot 版本可能导致模式切换失败。例如，最近的更新（如 VS Code 1.102+）存在模式选择器无响应的 bug。
- **身份验证或订阅限制**：如果使用的是免费的 Copilot 计划，可能会达到每月聊天限制，导致卡顿。令牌故障或会话过期也会阻止 Agent 模式等功能。
- **Windows 上的资源限制**：内存不足、受限模式（例如，在不受信任的工作区中）或后台进程（例如，Copilot 缓存中大型的嵌入文件）可能会使扩展主机过载，导致“无响应”错误。
- **Agent 模式特有 bug**：Agent 模式资源消耗更大，更容易出现无限的“Working...”循环，尤其是在任务被中断后或使用某些模型（例如，GPT 变体）时。这不会影响更简单的 Ask 模式。

### 故障排除步骤
按顺序尝试以下步骤——大多数用户无需重新安装即可解决问题：

1. **快速重新加载**：
   - 重新加载窗口：按 `Ctrl+Shift+P`，输入“Developer: Reload Window”，然后选择它。这会刷新 Copilot 而不关闭当前工作。
   - 重启扩展：打开扩展视图 (`Ctrl+Shift+X`)，点击“...”菜单，然后选择“Restart Extensions”。这通常在不完全重启的情况下修复无响应问题。

2. **检查日志以获取线索**：
   - 打开命令面板 (`Ctrl+Shift+P`)，运行“Output: Show Output”，然后选择“GitHub Copilot”或“GitHub Copilot Chat”。查找连接失败或大文件警告（例如，embeddings.json >5MB）等错误。通过“Developer: Set Log Level”将日志级别设置为“Trace”以获取更多详细信息。

3. **验证设置和身份验证**：
   - 确保 Agent 模式已启用：转到设置 (`Ctrl+,`)，搜索“chat.agent.enabled”，然后将其打开。
   - 退出/登录：点击帐户图标（左下角），退出 GitHub，然后重新登录。
   - 检查订阅：访问 [GitHub Copilot settings](https://github.com/settings/copilot) 以确认活动访问权限和没有限制。

4. **清除缓存和数据**：
   - 运行 `Ctrl+Shift+P` > “GitHub Copilot: Clear Copilot Data”（或输出面板中的类似命令）。
   - 删除大型缓存文件：导航到 `%APPDATA%\Code\User\globalStorage`（或特定于工作区的）并删除与 Copilot 相关的文件夹，例如 `github.copilot-chat`。重新启动 VS Code。

5. **更新所有内容**：
   - 通过扩展视图将 VS Code 和 Copilot 扩展更新到最新版本。
   - 如果在 Windows 上，以管理员身份运行 VS Code 一次，以排除权限问题。

6. **模式切换的解决方法**：
   - 打开新的聊天视图：按 `Ctrl+Alt+I` 在侧面面板中打开聊天，然后从下拉菜单中选择模式。如果卡住，请关闭当前聊天选项卡并重新开始。
   - 避免多任务处理：在 Agent 任务期间不要切换窗口；让它们完成。

如果这些方法没有帮助，请通过 `Ctrl+Shift+P` > “GitHub Copilot: Collect Diagnostics”收集诊断信息，并在 [VS Code GitHub issues](https://github.com/microsoft/vscode/issues) 上报告。对于持续冻结，暂时禁用其他扩展以隔离冲突。

参考资料：
- [GitHub Copilot FAQ](https://code.visualstudio.com/docs/copilot/faq)
- [Stack Overflow: GitHub Copilot not working suddenly](https://stackoverflow.com/questions/71806576/why-is-my-github-copilot-not-working-all-of-a-sudden)
- [VS Code Issue: Unable to switch Copilot modes](https://github.com/microsoft/vscode/issues/260293)
- [GitHub Docs: Troubleshooting Copilot](https://docs.github.com/copilot/troubleshooting-github-copilot/troubleshooting-common-issues-with-github-copilot)
- [GitHub Discussion: VS Code freezing with Copilot Agent](https://github.com/orgs/community/discussions/159701)
- [GitHub Discussion: Copilot Chat issues](https://github.com/orgs/community/discussions/156686)
