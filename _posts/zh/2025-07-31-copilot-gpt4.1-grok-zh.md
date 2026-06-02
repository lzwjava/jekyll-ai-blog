---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置Copilot以支持自定义模型
translated: true
type: note
---

当你在 GitHub Copilot 中选择“托管模型”后，仍然看到 GPT-4.1 作为默认模型，或者无法按预期使用 OpenRouter 提供的 Grok 或 Kimi 模型时，可能存在以下几个原因及解决步骤。以下是问题分析及如何通过 OpenRouter 配置 Copilot 使用 Grok 或 Kimi 模型的详细说明：

### 为何仍在使用 GPT-4.1

1. **默认模型设置**：GitHub Copilot 默认将 GPT-4.1 用于 Copilot Chat、编辑和代理模式，除非明确更改。即使选择了“托管模型”，如果未完全配置 OpenRouter 集成或选择特定模型，默认模型可能仍然生效。[](https://github.blog/changelog/2025-05-08-openai-gpt-4-1-is-now-generally-available-in-github-copilot-as-the-new-default-model/)
2. **上下文特定的模型使用**：Copilot 中的“修复框”（内联聊天或代码补全）在某些上下文中可能不支持切换到自定义模型（如 Grok 或 Kimi）。例如，除非在沉浸式视图或代理模式中明确切换到自定义模型，否则 Copilot Chat 面板或内联建议可能仍使用默认模型（GPT-4.1）。[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
3. **OpenRouter 集成限制**：OpenRouter 允许访问诸如 Grok（由 xAI 创建）和 Kimi（来自 Moonshot AI）等模型，但 Copilot 与 OpenRouter 的集成需要特定设置，且由于 API 限制或配置问题，并非所有模型都能立即可用。例如，OpenRouter 的 API 可能未宣布对所有模型的工具支持，这可能会阻止代理模式或某些功能与 Grok 或 Kimi 协同工作。[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
4. **订阅或配置限制**：如果你使用的是免费层或非 Pro/企业版 Copilot 订阅，可能会被限制使用默认模型（如 GPT-4.1）。此外，某些模型（例如 Grok 或 Kimi）可能需要通过 OpenRouter 进行特定配置或高级访问权限。[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)[](https://github.com/microsoft/vscode-copilot-release/issues/10193)

### 如何通过 OpenRouter 在 Copilot 中使用 Grok 或 Kimi 模型

要通过 OpenRouter 在 Copilot 中使用 Grok 或 Kimi 模型，特别是针对“修复框”（内联聊天或代码补全），请按照以下步骤操作：

1. **设置 Copilot 与 OpenRouter 的集成**：
   - **获取 OpenRouter API 密钥**：在 [openrouter.ai](https://openrouter.ai) 注册并获取 API 密钥。确保你拥有支持访问 Grok (xAI) 和 Kimi (Moonshot AI K2) 模型的积分或套餐。[](https://openrouter.ai/models)[](https://openrouter.ai)
   - **在 VS Code 中配置 OpenRouter**：
     - 打开 Visual Studio Code (VS Code) 并确保已安装最新版本的 GitHub Copilot 扩展（v1.100.2 或更高版本）。[](https://github.com/microsoft/vscode-copilot-release/issues/10193)
     - 转到状态栏中的 Copilot 仪表板，或打开命令面板（`Ctrl+Shift+P` 或 Mac 上的 `Command+Shift+P`）并输入 `GitHub Copilot: Manage Models`。
     - 添加你的 OpenRouter API 密钥，并将端点配置为包含 OpenRouter 模型。你可能需要遵循 OpenRouter 关于与 VS Code 的 Copilot 扩展集成的文档。[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)
   - **验证模型可用性**：添加 OpenRouter 端点后，在 Copilot 的“Manage Models”部分检查。诸如 `openrouter/xai/grok` 或 `openrouter/moonshotai/kimi-k2` 之类的模型应出现在模型选择器中。如果未出现，请确保你的 OpenRouter 帐户有权访问这些模型，并且没有限制（例如，免费层限制）。[](https://github.com/microsoft/vscode-copilot-release/issues/10193)

2. **为修复框切换模型**：
   - **对于内联聊天（修复框）**：“修复框”很可能指的是 Copilot 的内联聊天或代码补全功能。要更改内联聊天的模型：
     - 在 VS Code 中打开 Copilot Chat 界面（通过标题栏或侧边栏中的图标）。
     - 在聊天视图中，选择 `CURRENT-MODEL` 下拉菜单（通常在右下角），如果可用，请选择 `openrouter/xai/grok` 或 `openrouter/moonshotai/kimi-k2`。[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
     - 如果下拉菜单未显示 Grok 或 Kimi，可能是因为 OpenRouter 的 API 未宣布对这些模型的工具支持，这会限制它们在 Copilot 的某些功能（如代理模式或内联修复）中的使用。[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
   - **对于代码补全**：要更改代码补全（不仅仅是聊天）的模型：
     - 打开命令面板（`Ctrl+Shift+P` 或 Mac 上的 `Command+Shift+P`）并输入 `GitHub Copilot: Change Completions Model`。
     - 从列表中选择所需的 OpenRouter 模型（例如，Grok 或 Kimi）。请注意，由于 VS Code 当前仅支持 Ollama 端点用于自定义模型，并非所有 OpenRouter 模型都支持代码补全，尽管 OpenRouter 可以通过代理变通方法工作。[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-completion-model)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)

3. **OpenRouter 模型的变通方案**：
   - **代理解决方案**：由于 OpenRouter 的 API 并不总是宣布工具支持（代理模式或高级功能所需），你可以使用像 `litellm` 这样的代理来在 Copilot 中启用 Grok 或 Kimi。编辑 `config.yaml` 文件以包含：

     ```yaml
     model_list:
       - model_name: grok
         litellm_params:
           model: openrouter/xai/grok
       - model_name: kimi-k2
         litellm_params:
           model: openrouter/moonshotai/kimi-k2
     ```

     - 遵循来自 [Bas codes](https://bas.codes) 或 [DEV Community](https://dev.to) 等来源的设置说明，了解配置代理的详细步骤。[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
   - **重启 VS Code**：配置代理后，重启 VS Code 以确保新模型在模型选择器中可用。

4. **检查订阅和权限**：
   - **Copilot 订阅**：确保你拥有 Copilot Pro 或企业版订阅，因为免费层用户可能无法添加自定义模型。[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)
   - **企业限制**：如果你使用的是 Copilot 企业版订阅，你的组织必须启用模型切换功能。请向管理员核实或参考 GitHub 关于管理 Copilot 策略的文档。[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
   - **OpenRouter 积分**：确认你的 OpenRouter 帐户有足够的积分来访问高级模型（如 Grok 或 Kimi），因为这些模型可能比其他模型消耗更多积分。[](https://www.reddit.com/r/GithubCopilot/comments/1la87wr/why_are_gh_copilot_pro_models_so_much_worse_than/)

5. **修复框故障排除**：
   - 如果修复框仍在使用 GPT-4.1，可能是因为内联聊天功能在某些上下文（例如，非沉浸式视图）中被锁定为默认模型。尝试切换到 Copilot Chat 的沉浸式视图 (`https://github.com/copilot`) 以明确选择 Grok 或 Kimi。[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
   - 如果 Grok 或 Kimi 未出现在模型选择器中，请仔细检查 `Manage Models` 中的 OpenRouter 集成。你可能需要刷新模型列表或重新添加 OpenRouter API 密钥。[](https://github.com/microsoft/vscode-copilot-release/issues/10193)
   - 如果问题仍然存在，请先在 Copilot 的代理模式或聊天界面中测试模型以确认它们正常工作，然后尝试将它们应用于内联修复。

6. **替代工具**：
   - 如果 Copilot 与 OpenRouter 的集成仍然存在问题，可以考虑直接通过 [grok.com](https://grok.com) 或 Grok iOS/Android 应用使用 Grok，这些应用提供带有使用配额的免费访问。也可以通过 OpenRouter 的聊天界面测试 Kimi 模型以确保它们可访问。[](https://openrouter.ai)
   - 为了获得更无缝的体验，你可以探索其他 IDE 或工具，例如 Cursor，据称它与 OpenRouter 的 Kimi K2 模型配合良好。[](https://openrouter.ai)

### 补充说明

- **模型性能**：Grok 针对推理和求真进行了优化，使其适用于复杂的调试或架构任务，而 Kimi (K2) 可能在特定的编码场景中表现更佳。测试两者以确定哪个更适合你的用例。[](https://github.blog/ai-and-ml/github-copilot/which-ai-model-should-i-use-with-github-copilot/)
- **社区反馈**：一些用户报告称 OpenRouter 模型未出现在 Copilot 的模型选择器中，尤其是免费层帐户。这可能需要付费的 OpenRouter 计划或 Copilot Pro 订阅来解决。[](https://github.com/microsoft/vscode-copilot-release/issues/10193)[](https://www.reddit.com/r/GithubCopilot/comments/1la87wr/why_are_gh_copilot_pro_models_so_much_worse_than/)
- **持续限制**：关于在 Copilot 中直接启用自定义 API 端点的讨论仍在进行中（参见 [microsoft/vscode-copilot-release#7518](https://github.com/microsoft/vscode-copilot-release/issues/7518)）。在此功能实现之前，代理变通方案是使用 Grok 或 Kimi 最可靠的方法。[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)

### 引用来源

- [更改 Copilot Chat 的 AI 模型 - GitHub 文档](https://docs.github.com/en/copilot/managing-copilot/changing-the-ai-model-for-copilot-chat)[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
- [如何在 GitHub Copilot 代理模式中使用第三方模型 - Bas codes](https://bas.codes)[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)
- [Openrouter - openrouter.ai](https://openrouter.ai)[](https://openrouter.ai/models)
- [在 Copilot 代理模式中使用第三方模型 - DEV Community](https://dev.to)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
- [Openrouter - openrouter.ai](https://openrouter.ai)[](https://openrouter.ai)
- [Reddit 上的 r/LocalLLaMA：Github Copilot 现在支持 Ollama 和 OpenRouter 模型](https://www.reddit.com)[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)
- [我应该在 GitHub Copilot 中使用哪个 AI 模型？- GitHub 博客](https://github.blog)[](https://github.blog/ai-and-ml/github-copilot/which-ai-model-should-i-use-with-github-copilot/)
- [OpenAI GPT-4.1 现已在 GitHub Copilot 中正式可用 - GitHub 更新日志](https://github.blog)[](https://github.blog/changelog/2025-05-08-openai-gpt-4-1-is-now-generally-available-in-github-copilot-as-the-new-default-model/)
- [OpenRouter（免费）模型在 Manage Models 中缺失 - GitHub Issues](https://github.com/microsoft/vscode-copilot-release/issues/10193)[](https://github.com/microsoft/vscode-copilot-release/issues/10193)

如果你遇到特定错误或需要有关设置的进一步帮助，请提供更多详细信息（例如，错误消息、VS Code 版本或订阅类型），我可以进一步定制解决方案！
