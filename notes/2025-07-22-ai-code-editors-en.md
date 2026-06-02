---
audio: false
generated: true
lang: en
layout: post
title: AI-Powered Code Editing Tools
translated: false
type: note
---

### Visual Studio Code (VS Code) with GitHub Copilot

VS Code, enhanced by GitHub Copilot (an AI extension), supports selecting code (like a function) and using AI to fix, edit, or refactor it. Key features include:

- **Inline Chat**: Select the code, press `Ctrl+I` (Windows/Linux) or `Cmd+I` (Mac), and enter a prompt like "fix this bug" or "refactor to use async/await." Copilot suggests edits directly in the editor.
- **Fix Errors**: For compiler errors (red squiggles), hover and select "Fix using Copilot" to get AI-generated fixes.
- **Chat View**: Open the Copilot Chat (`Ctrl+Alt+I`), select code, and ask to explain, edit, or generate tests. It can handle multi-file edits in agent mode.
- **Actions Menu**: Right-click selected code for AI actions like explaining, renaming, or reviewing.

Copilot is free with limits or paid for unlimited use.

### Cursor AI Code Editor

Cursor is an AI-first code editor forked from VS Code, designed specifically for AI-assisted editing. It excels at selecting and modifying code with AI:

- **Edit with Ctrl+K**: Select a function or code block, press `Ctrl+K` (or `Cmd+K` on Mac), and describe changes (e.g., "optimize this function for performance"). Cursor generates diffs you can preview and apply.
- **Composer Mode**: For complex edits across files, use the Composer interface to prompt multi-file changes, review diffs, and iterate.
- **Agent Mode**: Press `Ctrl+I`, instruct broader tasks (e.g., "fix bugs in this module"), and it autonomously plans, edits, and runs commands while keeping you in the loop.
- **Next Edit Suggestions**: AI predicts and suggests follow-up edits based on your changes.

Cursor is free for basics, with a Pro plan for advanced models. It imports VS Code extensions seamlessly.

### IntelliJ IDEA with JetBrains AI Assistant

IntelliJ IDEA (and other JetBrains IDEs) has a built-in AI Assistant plugin that allows selecting code and using AI for fixes or edits:

- **AI Actions Menu**: Select code, press `Alt+Enter` or right-click, choose "AI Actions" > options like "Suggest Refactoring," "Find Problems," or "Fix with AI." It analyzes context and suggests changes in a diff viewer.
- **Inline Prompt**: Type a prompt directly in the editor (e.g., "refactor this function"), press `Tab`, and AI generates/edits code inline.
- **Error Fixes**: For highlighted errors, select "Fix with AI" to get context-aware suggestions.
- **Code Generation/Refactoring**: Invoke via menu for explaining code, adding type annotations, or regenerating sections.

AI Assistant requires a JetBrains AI license (free trial available) and is powered by models like Mellum for completions.

All these tools integrate AI deeply, but Cursor is the most AI-centric, VS Code/Copilot is flexible and widely used, and IntelliJ's AI is tailored for enterprise/Java-heavy workflows. Choose based on your preferred ecosystem.

References:
[GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview)
[Get started with GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/getting-started)
[Features | Cursor - The AI Code Editor](https://cursor.com/en/features)
[Cursor AI: A Guide With 10 Practical Examples](https://www.datacamp.com/tutorial/cursor-ai-code-editor)
[Use AI in editor | IntelliJ IDEA Documentation](https://www.jetbrains.com/help/idea/use-ai-in-editor.html)
[AI Assistant in JetBrains IDEs | IntelliJ IDEA Documentation](https://www.jetbrains.com/help/idea/ai-assistant-in-jetbrains-ides.html)
[Use AI prompts to explain and refactor your code | IntelliJ IDEA Documentation](https://www.jetbrains.com/help/idea/use-prompts-to-explain-and-refactor-your-code.html)
