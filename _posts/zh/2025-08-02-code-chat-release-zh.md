---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VS Code 中的 Copilot 聊天命令
translated: true
type: note
---

在 Visual Studio Code（VS Code）中使用 `code chat "hi"` 命令打开 GitHub Copilot 聊天窗口的功能，与 GitHub Copilot Chat 及其相关功能（如聊天视图和相关命令）的广泛集成紧密相关。根据现有信息，分析如下：

### `code chat` 命令的发布
虽然 VS Code 的发布说明中没有明确提及 `code chat` 命令，但它与 GitHub Copilot Chat 功能密切相关，该功能在多个 VS Code 版本中逐步增强。该命令很可能是调用 Copilot 聊天视图或内联聊起的别名或快捷方式，随着 Copilot Chat 功能的引入而变得突出。

- **GitHub Copilot Chat 集成**：Copilot Chat 功能，包括聊天视图，从 2023 年 8 月左右（VS Code 1.82 版本）开始开发，并在后续版本（包括 2025 年 3 月的 1.99 版本）中不断演进。聊天视图及相关命令（如 `Chat: Open Chat` 或内联聊天命令）在此期间被引入并完善。[](https://code.visualstudio.com/updates/v1_93)[](https://code.visualstudio.com/updates/v1_86)
- **命令面板和聊天命令**：到 2024 年 11 月（1.96 版本），VS Code 引入了从聊天视图切换到 Copilot Edits 以及改进聊天视图中的上下文处理等功能，表明聊天相关命令已得到充分支持。通过命令面板触发 Copilot Chat 的功能已经就位，`code chat` 命令很可能作为这些增强功能的一部分出现。[](https://code.visualstudio.com/updates/v1_96)
- **针对 1.99.2 版本**：2025 年 3 月发布（1.99 版本）及其更新（1.99.2 和 1.99.3）未明确提及 `code chat "hi"` 命令。然而，它们讨论了 Copilot Chat 体验的进展，如自定义聊天模式、代理模式和改进的上下文处理，这表明聊天相关命令在此阶段已得到良好支持。如果 `code chat` 命令未明确记录，它很可能作为命令面板与 Copilot Chat 集成的一部分而可用。[](https://code.visualstudio.com/updates/v1_99)

### `code chat "hi"` 功能何时发布？
虽然提供的说明中未明确指出 `code chat "hi"` 命令的发布时间，但可以合理推断，考虑到 Copilot Chat 功能的成熟状态，该命令在 2025 年 3 月发布（1.99 版本）或更早时已可用。该命令很可能利用了打开聊天视图的现有基础设施，该基础设施在 1.96 版本（2024 年 11 月）时已通过 `Chat: Open Chat` 或 `Open Quick Chat` 等命令建立。[](https://code.visualstudio.com/updates/v1_96)[](https://code.visualstudio.com/updates/v1_93)

- **最早可能发布时间**：Copilot Chat 功能，包括通过命令打开聊天视图的能力，在 2024 年 8 月（1.93 版本）时已显著发展，具备快速聊天和上下文改进等功能。`code chat` 命令可能在此时间点左右或之后作为命令面板与 Copilot 集成的一部分被引入。[](https://code.visualstudio.com/updates/v1_93)
- **针对 1.99.2 的确认**：到 1.99.2 版本（2025 年 3 月），Copilot Chat 系统已成熟，支持自定义模式、代理模式以及如 `#codebase` 等上下文变量。考虑到聊天功能的高级状态，`code chat "hi"` 命令（用于打开聊天视图并输入提示如 "hi"）很可能作为命令面板中的标准命令得到支持。[](https://code.visualstudio.com/updates/v1_99)

### 结论
用于打开 Copilot Chat 窗口的 `code chat "hi"` 命令很可能在 2025 年 3 月发布（1.99 版本）或更早时可用，可能早至 2024 年 8 月（1.93 版本），当时 Copilot Chat 功能已显著增强。具体到 1.99.2 版本，该命令几乎肯定可用，因为聊天视图及相关命令在此阶段已充分集成。如需精确确认，可以在 VS Code 1.99.2 的命令面板中输入 `code chat` 查看它是否作为有效命令出现。

**参考资料**：
- 2025 年 3 月（1.99 版本）- code.visualstudio.com[](https://code.visualstudio.com/updates/v1_99)
- 2024 年 11 月（1.96 版本）- code.visualstudio.com[](https://code.visualstudio.com/updates/v1_96)
- 2024 年 8 月（1.93 版本）- code.visualstudio.com[](https://code.visualstudio.com/updates/v1_93)
