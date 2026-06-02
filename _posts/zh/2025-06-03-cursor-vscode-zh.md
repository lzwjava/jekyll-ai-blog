---
audio: false
generated: true
lang: zh
layout: post
title: 光标与VS Code
translated: true
type: note
---

是的，Cursor 对 Visual Studio Code（VS Code）进行分支并围绕其构建业务是合法的，前提是他们遵守 VS Code 源代码发布的 MIT 许可证条款。MIT 许可证具有高度许可性，允许任何人使用、复制、修改、合并、发布、分发、再许可和销售软件副本，只要在所有副本或软件的实质部分中包含原始版权声明和许可声明。

以下是关于 Cursor 分支合法性的关键点：

1. **MIT 许可证合规性**：在 GitHub 仓库 `vscode` 中提供的 VS Code 源代码基于 MIT 许可证授权。这允许 Cursor 对代码库进行分支、修改并将其用于商业目的，包括创建闭源产品，只要他们在分发时包含原始的 MIT 许可证和版权声明。MIT 许可证不要求分支项目保持开源，因此 Cursor 可以合法地使其产品成为专有软件。

2. **Visual Studio Code 与 Code-OSS 的区别**：开源 `vscode` 仓库（通常称为 Code-OSS）与微软品牌的 Visual Studio Code 产品之间存在区别。微软品牌的 VS Code 包含专有附加功能（例如遥测、市场集成），并在不同的许可证下分发。然而，对基于 MIT 许可证的开源 `vscode` 仓库进行分支，正是 Cursor 和类似项目（如 Windsurf）所做的。这是明确允许的，他们可以在其基础上构建自己的定制功能。

3. **Visual Studio Marketplace 限制**：像 Cursor 这样的分支面临的一个重要限制是，由于微软的服务条款，它们无法访问官方的 Visual Studio Marketplace。这意味着 Cursor 无法提供与 VS Code 相同的扩展生态系统，除非他们建立替代的扩展注册表（例如 OpenVSX）或开发自己的扩展。此外，一些专有扩展（如 GitHub Copilot 或微软的 C/C++ 扩展）仅限于微软官方的 VS Code 构建版本，这可能会限制分支的功能。

4. **伦理与社区关切**：尽管根据 MIT 许可证进行分支是合法的，但一些人提出了伦理关切，质疑像 Cursor 这样的公司是否公平地利用主要由 VS Code 团队开发的代码，添加功能后作为专有产品出售而不回馈原始 VS Code 社区。然而，这是一个道德辩论，而非法律问题，MIT 许可证明确允许此类使用。

5. **微软的回应**：微软已采取措施保护其生态系统，例如限制分支对市场的访问和专有扩展的使用，如从非官方构建中移除 C/C++ 扩展支持所示。然而，这些限制并不影响对 `vscode` 仓库本身进行分支的合法性，只要分支遵守 MIT 许可证。

总之，Cursor 对 VS Code 的分支在 MIT 许可证下是合法的，因为他们可以自由修改代码库并将其商业化，只要包含所需的版权和许可证声明。他们面临的主要挑战是实际性的——例如无法访问 VS Code Marketplace 和某些专有扩展——而非法律障碍。如果您对 Cursor 的具体实现或合规性有疑虑，建议咨询您所在司法管辖区的法律专业人士，因为我不是律师。
