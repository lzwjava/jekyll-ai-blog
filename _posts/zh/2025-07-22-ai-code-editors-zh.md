---
audio: false
generated: true
lang: zh
layout: post
title: AI赋能的代码编辑工具
translated: true
type: note
---

### Visual Studio Code (VS Code) 与 GitHub Copilot

VS Code 结合 GitHub Copilot（AI扩展插件）支持选中代码（如函数）并通过AI进行修复、编辑或重构。核心功能包括：

- **行内对话**：选中代码后按 `Ctrl+I`（Windows/Linux）或 `Cmd+I`（Mac），输入指令如“修复此错误”或“重构为异步模式”，Copilot将在编辑器中直接建议修改方案
- **错误修复**：针对编译器错误（红色波浪线），悬停并选择“通过Copilot修复”即可获取AI生成的解决方案
- **对话视图**：打开Copilot聊天界面（`Ctrl+Alt+I`），选中代码后可要求解释、编辑或生成测试用例。在代理模式下支持多文件编辑
- **操作菜单**：右键选中代码可调用AI功能，包括代码解释、重命名或审查

Copilot提供有限免费版，付费版可无限制使用。

### Cursor AI 代码编辑器

Cursor是基于VS Code分支开发的AI优先代码编辑器，专为AI辅助编辑设计。其核心优势在于通过AI选择并修改代码：

- **Ctrl+K编辑模式**：选中函数或代码块后按 `Ctrl+K`（Mac按 `Cmd+K`），描述修改需求（如“优化此函数性能”），Cursor将生成可预览应用的差异代码
- **作曲者模式**：针对跨文件复杂编辑，可通过Composer界面指令多文件修改，实时查看差异并迭代
- **代理模式**：按 `Ctrl+I` 输入宏观指令（如“修复该模块缺陷”），AI将自主规划、编辑并运行命令，同时保持操作透明
- **连续编辑建议**：AI会根据代码变更预测并推荐后续修改方案

基础功能免费，高级模型需订阅Pro版。可无缝兼容VS Code扩展插件。

### IntelliJ IDEA 与 JetBrains AI助手

IntelliJ IDEA（及其他JetBrains IDE）内置AI助手插件，支持选中代码并通过AI进行修复编辑：

- **AI操作菜单**：选中代码后按 `Alt+Enter` 或右键选择“AI操作”>“建议重构”、“发现问题”或“AI修复”。系统将分析上下文并在差异查看器中建议修改
- **行内指令**：直接在编辑器中输入指令（如“重构此函数”），按 `Tab` 键即可生成/编辑代码
- **错误修复**：针对高亮错误，选择“AI修复”获取上下文感知建议
- **代码生成/重构**：通过菜单调用代码解释、添加类型注解或重构代码段

AI助手需JetBrains AI授权（含免费试用），由Mellum等模型提供智能补全支持。

这些工具均深度集成AI功能：Cursor最聚焦AI交互，VS Code/Copilot灵活性高且用户广泛，IntelliJ的AI则专为企业级/Java重度工作流优化。建议根据实际开发生态进行选择。

参考文献：
[VS Code中的GitHub Copilot](https://code.visualstudio.com/docs/copilot/overview)
[VS Code中开始使用GitHub Copilot](https://code.visualstudio.com/docs/copilot/getting-started)
[功能特性 | Cursor - AI代码编辑器](https://cursor.com/en/features)
[Cursor AI：10个实战案例指南](https://www.datacamp.com/tutorial/cursor-ai-code-editor)
[在编辑器中使用AI | IntelliJ IDEA文档](https://www.jetbrains.com/help/idea/use-ai-in-editor.html)
[JetBrains IDE中的AI助手 | IntelliJ IDEA文档](https://www.jetbrains.com/help/idea/ai-assistant-in-jetbrains-ides.html)
[使用AI指令解释与重构代码 | IntelliJ IDEA文档](https://www.jetbrains.com/help/idea/use-prompts-to-explain-and-refactor-your-code.html)
