---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过个人订阅掌握 GitHub Copilot
translated: true
type: note
---

问题：在不受限的环境中使用个人 GitHub Copilot 订阅来锻炼技能并学习 settings/JSON 配置，以便在受公司企业限制的 Copilot 环境中工作变得更容易，这是否是一个有效的策略？

回答：

是的，这在开发者中是一个**非常明智且被广泛采用的策略**。以下是关于为什么该策略有效以及你应该重点关注哪些方面的全面分析。

---

## 为什么这个策略合情合理

### 核心问题：Enterprise Copilot 受限严重

在企业环境中，管理员控制着三个层面的 policy：**feature policies**（哪些功能可用）、**privacy policies**（允许哪些数据操作）以及 **models policies**（除了基础模型外，你可以访问哪些 AI models）。每个功能都可以针对组织中的所有成员单独禁用或屏蔽。

如果你的组织是企业的一部分，并且在企业层面选择了明确的 settings，你 **无法在组织层面覆盖这些设置**。

这意味着像 agent mode、model selection、MCP servers 甚至是 Bing 访问等功能可能会被静默屏蔽——如果你从未自由地使用过 Copilot，你甚至不会知道缺少了什么。

---

### 个人订阅：你可以自由探索的内容

GitHub 提供三种个人计划：**Copilot Free**（每月 2,000 次 inline suggestions）、**Copilot Pro**（无限次 completions + premium model 访问）以及 **Copilot Pro+**（最大的灵活性、premium models 以及扩大的 request 限制）。

Copilot Pro 每月 10 美元，包含 300 次 premium requests。Pro+ 每月 39 美元，包含 1,500 次 premium requests，并可访问包括 Claude Opus 4 和 OpenAI o3 在すす内的所有 AI models。

在个人计划中，**你控制一切**——没有 policy 屏蔽 agent mode，没有管理员禁用 model selection，也没有 audit logs 监视你的 prompts。

---

### 哪些内容可以很好地迁移到企业环境

你在个人使用中建立的技能和知识可以**直接转化**到企业用途。具体包括：

#### 1. `settings.json` 精通

按体验区域（editor completions、chat、agents 和 workflow）对 Copilot settings 进行分组，并了解 **workspace settings**（策略/强制执行）与 **user settings**（个人偏好）之间的区别至关重要。保留一份带有注释的基准 JSON 可以让团队成员比对有意的更改。

最简单且被广泛采用的方法是将 VS Code workspace 配置文件直接通过 `.vscode/settings.json` 文件提交到你的 repository。当项目文件夹打开时，这些 workspace settings 会覆盖用户偏好。

#### 2. Custom Instructions 与 Prompt Engineering

为你的整个 codebase 创建标准化的 custom instructions，确保每个 Copilot 建议都遵循你团队确切的 coding standards，从而生成符合你的 style guide 的建议，而无需手动修正。

这些知识是**完全可移植的**——你在个人项目中养成习惯，在工作中使用它。

#### 3. Agent Skills（可移植标准）

Agent Skills 是一个**开放标准**，支持跨不同 AI agents 的可移植性。你在 VS Code 中创建的 skills 可以与 VS Code 中的 GitHub Copilot、GitHub Copilot CLI 以及 GitHub Copilot coding agent 配合使用。

在个人环境下掌握 skill 文件（`.vscode/`，`SKILL.md`），可以让你将这些相同的文件带入企业级 repos。

#### 4. MCP Server 配置

MCP servers 配置在 `.vscode/mcp.json`（workspace）或用户配置文件 `mcp.json` 中。组织可以通过 GitHub policies 集中管理 MCP server 访问权限，这需要 Copilot Business 或 Enterprise 计划。

在个人环境下了解 MCP 配置意味着你清楚地知道在企业环境中哪些是可用的，哪些是被屏蔽的。

---

## 核心注意事项：当企业为你分配席位时，个人计划会被取消

如果你有一个激活的 Copilot Pro 或 Copilot Pro+ 计划，然后被**分配了一个作为 Copilot Business 或 Copilot Enterprise 计划一部分的席位**，你的个人 Copilot 计划将**自动取消**。你将收到按比例退还的款项，然后按照公司设定的 policies 使用 Copilot。

**实践意义：** 如果你想在加入企业计划的同时继续自由练习，你需要使用一个**独立的个人 GitHub 账户**来维持并行的个人订阅。安全的方法是让开发者使用一个**专用的工作 GitHub 账户**，将 Enterprise 席位与个人账户分开，这样他们的个人计划就不会被取消。

---

## 总结：个人练习的重点内容

| 技能 | 为什么可以迁移 |
| --- | --- |
| `settings.json` 配置（user + workspace 级别） | 相同的 JSON 结构在企业环境中同样有效 |
| Custom instructions (`.github/copilot-instructions.md`) | 完全可移植到任何 repo |
| Agent mode + agentic workflows | 当企业开启这些功能时，你知道有哪些可用 |
| MCP server 设置 (`mcp.json`) | 了解被屏蔽与被允许的配置区别 |
| Prompt engineering 模式 | 完全基于技能，不依赖于计划类型 |
| Model selection 行为 | 了解当企业固定模型时，输出为何会有差异 |
| `SKILL.md` agent skill 编写 | 开放标准，可在个人和企业环境间通用 |

---

## 结论

该策略是**有效且值得推荐的**。核心洞察在于，大多数对企业级 Copilot 的挫败感源于不知道什么功能 *应该* 起作用——因此开发者意识不到哪些是由于 policy 屏蔽、配置错误还是单纯的不支持。在个人计划上建立熟练度意味着当你在工作中遇到限制时，你可以自信地说“这个功能存在但被 policy 禁用了”，并据此向管理员申请或寻找正确的 workaround。

参考资料：

- [GitHub Copilot Plans](https://docs.github.com/en/copilot/get-started/plans)
- [Copilot Policies Documentation](https://docs.github.com/en/copilot/concepts/policies)
- [Managing Individual Copilot Policies](https://docs.github.com/copilot/how-tos/manage-your-account/managing-copilot-policies-as-an-individual-subscriber)
- [Copilot in VS Code Settings Reference](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
- [Tuning Copilot Settings in VS Code](https://dev.to/pwd9000/tune-github-copilot-settings-in-vs-code-32kp)
- [Managing Copilot & VS Code Settings Across Teams](https://dev.to/pwd9000/managing-github-copilot-vs-code-settings-across-teams-1phj)
- [Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Copilot Licenses](https://docs.github.com/en/billing/concepts/product-billing/github-copilot-licenses)
