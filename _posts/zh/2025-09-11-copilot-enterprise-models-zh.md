---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Copilot企业版模型选项概览
translated: true
type: note
---

你在询问**Copilot Enterprise**使用哪种模型，特别是关于它究竟是GPT-4.1、GPT-4o还是其他模型。以下是截至**2025年9月**的最新相关信息：

---

### Copilot Enterprise 可使用哪些模型？

#### GitHub Copilot Enterprise 和 Copilot Chat

* **默认情况下**，GitHub Copilot Enterprise（包括 Copilot Chat）**运行在 GPT-4o 上**，提供更快的响应速度和更高的质量。([Reddit][1])
* 近期，**GPT-4.1** 也已推出——但管理员必须在 Copilot 设置中通过策略**显式启用它**。启用后，用户可以在 VS Code 和 github.com 的模型选择器中选择 GPT-4.1。([The GitHub Blog][2])

#### Visual Studio Copilot

* 截至**2025年6月**，Visual Studio 的 Copilot **现已默认使用 GPT-4.1 作为其模型**，取代了 GPT-4o。微软的测试表明，GPT-4.1 能提供**更快的响应、更高质量的建议和更高的效率**。([Visual Studio Magazine][3], [Microsoft Learn][4])

#### Microsoft 365 Copilot（Office 生产力工具）

* 微软已开始通过新的“**智能模式**”将 **GPT-5** 集成到更广泛的 Copilot 生态系统中——包括 Microsoft 365 Copilot、GitHub Copilot、Copilot Studio 等——该模式会根据需求自动将任务路由到最合适的模型，从而提升推理能力、上下文保留能力和交互质量。([The Verge][5])
* 此外，微软宣布集成 Anthropic 的 **Claude Sonnet 4**，用于演示文稿设计和电子表格自动化等高级任务，同时其他功能仍使用 **GPT-5**（以及剩余的基于 GPT 的路径）。([New York Post][6])

---

### 总结 — **Copilot Enterprise** 应使用哪种模型？

* **GitHub Copilot Enterprise / Copilot Chat**：

  * 默认模型：**GPT-4o**
  * 可选模型：**GPT-4.1**（如果管理员已启用）
* **Visual Studio Copilot**：默认模型现在是 **GPT-4.1**
* **Microsoft 365 Copilot**：利用 **GPT-5 智能模式**，具备更高性能的路由和能力——并且还集成了 **Claude Sonnet 4**，用于特定的企业任务。

---

### 快速概览（根据你的偏好，不使用宽表）

* **GPT-4o**：GitHub Copilot Enterprise 的默认模型；以企业聊天中的速度和质量著称。
* **GPT-4.1**：功能更强大的继任者——在代码、指令遵循和长上下文方面表现更佳。如果在 GitHub Copilot 中启用则可用，并且现在是 Visual Studio Copilot 的默认模型。([OpenAI][7])
* **GPT-5**：最新模型，通过智能模式集成到 M365 Copilot 中，并在所有 Copilot 平台中实现更智能的模型选择。([The Verge][5])
* **Claude Sonnet 4**：主要针对 PowerPoint 和 Excel 自动化等 Office 任务添加，与 GPT-5 并存。([New York Post][6])

---

### 接下来该做什么？

* 如果你是管理 GitHub Copilot Enterprise 的**管理员**，请检查你的设置，**启用 GPT-4.1**，以便用户利用其性能改进。
* 如果你使用 **Visual Studio Copilot**，那么你默认已经在使用 **GPT-4.1**。
* 对于 **Microsoft 365 Copilot**，你将受益于 **GPT-5 智能模式**的推出和 **Claude Sonnet 4** 的集成。无需任何操作——它已经是服务层的一部分。

如果你需要帮助配置这些设置或在你组织的特定环境中导航模型选项，请告诉我！

[1]: https://www.reddit.com/r/GithubCopilot/comments/1dx2iq1/github_copilot_enterprise_on_gpt4o/?utm_source=chatgpt.com "GitHub Copilot Enterprise on GPT-4o : r/GithubCopilot"
[2]: https://github.blog/changelog/2025-04-14-openai-gpt-4-1-now-available-in-public-preview-for-github-copilot-and-github-models/?utm_source=chatgpt.com "OpenAI GPT-4.1 now available in public preview for GitHub ..."
[3]: https://visualstudiomagazine.com/articles/2025/06/26/new-default-model-for-visual-studio-copilot-so-how-do-you-choose.aspx?utm_source=chatgpt.com "New Default Model for Visual Studio Copilot, So How Do ..."
[4]: https://learn.microsoft.com/en-us/visualstudio/ide/copilot-select-add-models?view=vs-2022&utm_source=chatgpt.com "Using AI models in Copilot Chat - Visual Studio (Windows)"
[5]: https://www.theverge.com/news/753984/microsoft-copilot-gpt-5-model-update?utm_source=chatgpt.com "Microsoft brings GPT-5 to Copilot with new smart mode"
[6]: https://nypost.com/2025/09/10/business/microsoft-to-add-anthropic-ai-models-as-rift-with-openai-grows-report/?utm_source=chatgpt.com "Microsoft to add Anthropic AI models - as rift with OpenAI grows: report"
[7]: https://openai.com/index/gpt-4-1/?utm_source=chatgpt.com "Introducing GPT-4.1 in the API"
