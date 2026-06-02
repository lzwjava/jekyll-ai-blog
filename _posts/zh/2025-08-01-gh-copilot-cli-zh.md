---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Copilot CLI 集成
translated: true
type: note
---

你无法通过类似 `code --plugin copilot "hi"` 的语法直接在命令行中调用 GitHub Copilot 作为插件来获取响应。不过，GitHub Copilot 确实通过 GitHub CLI 的 `gh copilot` 扩展提供了命令行集成，该扩展为命令建议和解释提供了类似聊天的界面。这与通过 `code` 命令调用的通用插件并不完全相同，但在命令行交互方面具有相似用途。

### GitHub Copilot CLI 功能详情
- **要求**：你需要拥有 GitHub Copilot 订阅、已安装 GitHub CLI (`gh`) 并安装 `gh-copilot` 扩展。设置说明可在 GitHub CLI 仓库或文档中获取：[GitHub CLI 安装指南](https://cli.github.com/) 和 [在 CLI 中使用 GitHub Copilot](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)。
- **使用方法**：设置完成后，你可以使用如下命令：
  - `gh copilot suggest -t shell "hi"` 获取 shell 命令建议
  - `gh copilot explain "hi"` 获取命令解释
  - 示例：运行 `gh copilot suggest -t shell "say hello"` 可能会根据上下文建议 `echo "hello"` 或在 macOS 上建议文本转语音命令 `say "hello"`
- **限制**：CLI 界面专为命令行相关任务（如 shell、Git 或 GitHub CLI 命令）设计，不支持像聊天机器人那样的通用对话响应，且仅支持英文提示[负责任地使用 GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/responsible-use-of-github-copilot-in-the-cli)。
- **交互模式**：运行 `suggest` 命令后，Copilot 会启动交互式会话，你可以优化建议、执行命令（复制到剪贴板）或进行评分。如需自动执行，需要设置 `ghcs` 别名[在命令行中使用 GitHub Copilot](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)。

### 为何 `code --plugin copilot "hi"` 不可行
- **Visual Studio Code CLI**：`code` 命令（用于 VS Code）支持如 `--install-extension` 等选项来安装扩展，但没有 `--plugin` 标志来直接通过输入 `"hi"` 调用扩展。GitHub Copilot 等扩展通常在 VS Code 编辑器内运行，提供内联建议或聊天界面，而非作为独立 CLI 工具[VS Code 中的 GitHub Copilot](https://code.visualstudio.com/docs/copilot/overview)。
- **Copilot 架构**：GitHub Copilot 的 VS Code 插件通过与语言服务器和 GitHub 后端通信来实现代码补全和聊天功能。没有公开 API 或 CLI 机制可从命令行直接向插件传递任意字符串（如 `"hi"`）并获取响应[如何以编程方式调用 Github Copilot？](https://stackoverflow.com/questions/76761429/how-to-invoke-github-copilot-programmatically)。
- **通用输入替代方案**：如需向 Copilot 发送如 `"hi"` 的提示并获取响应，需使用 VS Code 或其他受支持 IDE 中的 Copilot Chat，或探索支持对话式提示的其他 AI CLI 工具（如微软用于 Azure CLI 的 AI Shell）[在 Azure 中使用 Microsoft Copilot 与 AI Shell](https://learn.microsoft.com/en-us/azure/copilot/use-copilot-cli)。

### 实现目标的变通方案
若需通过命令行调用类似 Copilot 的 AI 助手并获取对 `"hi"` 等提示的响应，可以：
1. **使用 `gh copilot` 处理命令行任务**：
   - 安装 GitHub CLI 和 Copilot 扩展
   - 运行 `gh copilot suggest -t shell "greet with hi"` 获取类似 `echo "hi"` 的命令
   - 此方法限于命令行场景，单独的 `"hi"` 可能无法获得有意义的响应，除非以命令请求的形式提出
2. **使用 VS Code 的 Copilot Chat**：
   - 打开 VS Code，通过 `⌃⌘I` 或聊天图标访问 Copilot Chat 界面，输入 `"hi"` 获取对话响应
   - 此方法需在编辑器内手动交互，非 CLI 调用方式[GitHub Copilot in VS Code 速查表](https://code.visualstudio.com/docs/copilot/copilot-cheat-sheet)
3. **探索其他 AI CLI 工具**：
   - **AI Shell**：微软的 AI Shell 支持在 CLI 中使用自然语言提示处理 Azure 相关任务。安装后可尝试 `"hi"` 等提示，但该工具主要针对 Azure CLI 和 PowerShell 命令优化[在 Azure 中使用 Microsoft Copilot 与 AI Shell](https://learn.microsoft.com/en-us/azure/copilot/use-copilot-cli)
   - **自定义脚本**：可通过编写脚本与 AI 模型 API（如可访问的 OpenAI API）交互来处理 `"hi"` 等提示。但 GitHub Copilot 的 API 未公开提供此类使用[如何以编程方式调用 Github Copilot？](https://stackoverflow.com/questions/76761429/how-to-invoke-github-copilot-programmatically)
4. **模拟插件行为**：
   - 创建将输入传递给 `gh copilot suggest` 或其他 AI CLI 工具的 shell 脚本或别名
   - 示例：
     ```bash
     alias ai='gh copilot suggest -t shell'
     ai "greet with hi"
     ```
     这将建议类似 `echo "hi"` 的命令

### 编程式调用
如需编程式调用类 Copilot 功能（如示例所示），请注意：
- GitHub Copilot 未提供用于直接编程式访问的公共 API。虽有社区通过反向工程语言服务器或使用代理捕获建议的尝试，但这些方案复杂且存在风险（如可能导致封号）[如何以编程方式调用 Github Copilot？](https://stackoverflow.com/questions/76761429/how-to-invoke-github-copilot-programmatically)
- 可探索开源替代方案或其他具有 CLI 集成的 AI 模型（如 Hugging Face 的 CLI 工具或使用自定义封装的本地 LLM）

### 总结
虽然不支持 `code --plugin copilot "hi"` 的调用方式，但你可以通过 `gh copilot` 处理命令行任务，或使用 VS Code 的 Copilot Chat 处理对话式提示来实现类似功能。如需通用 CLI AI 体验，可考虑 AI Shell 等工具或使用其他 AI API 的自定义脚本。请务必验证建议内容，因为 Copilot 的 CLI 响应可能包含训练数据中的错误或偏见[负责任地使用 GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/responsible-use-of-github-copilot-in-the-cli)。

如果你有特定使用场景（如对话式 AI 与命令生成），请告知，我可以进一步定制解决方案！
