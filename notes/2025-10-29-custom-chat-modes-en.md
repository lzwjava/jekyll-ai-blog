---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Custom Chat Modes for GitHub Copilot
translated: false
type: note
---

### What is chatmode.md?

In the GitHub Copilot extension for Visual Studio Code (VS Code), `chatmode.md` files are used to define **custom chat modes**. These allow you to configure Copilot Chat to adopt specific personas or behaviors for tasks like planning, security reviews, or code implementation. Each mode can specify instructions, available tools (e.g., search, fetch, or GitHub repo access), and even the AI model to use. This feature is in preview as of VS Code 1.101 and helps tailor responses for consistency across your workflow.

Custom modes are stored as Markdown files with the `.chatmode.md` extension, either in your workspace (for team sharing) or user profile (for personal reuse).

### Why Use Custom Chat Modes?
- **Tailored Responses**: Enforce guidelines, like generating plans without editing code.
- **Tool Control**: Limit tools to read-only for planning or enable editing for implementation.
- **Efficiency**: Reuse setups for common roles (e.g., architect, reviewer).

### How to Create a chatmode.md File

1. Open the **Chat view** in VS Code:
   - Click the Copilot Chat icon in the title bar, or use `Ctrl+Alt+I` (Windows/Linux) / `Cmd+Option+I` (macOS).

2. In the Chat view, click **Configure Chat > Modes**, then select **Create new custom chat mode file**. Alternatively, open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Chat: New Mode File**.

3. Choose a location:
   - **Workspace**: Saves to `.github/chatmodes/` by default (shareable with your team). Customize folders via the `chat.modeFilesLocations` setting.
   - **User profile**: Saves to your profile folder for syncing across devices.

4. Name the file (e.g., `planning.chatmode.md`) and edit it in VS Code.

To manage existing modes, use **Configure Chat > Modes** or the **Chat: Configure Chat Modes** command.

### File Structure and Syntax

A `.chatmode.md` file uses Markdown with optional YAML frontmatter for metadata. Here's the basic structure:

- **YAML Frontmatter** (enclosed in `---` lines, optional):
  - `description`: Short text shown in the chat input placeholder and dropdown hover.
  - `tools`: Array of tool names (e.g., `['fetch', 'search']`). Use built-in tools like `githubRepo` or extension tools; configure via **Configure Tools**.
  - `model`: AI model (e.g., `"Claude Sonnet 4"`). Defaults to your selected model.

- **Body**: Markdown instructions for the AI, including prompts, guidelines, or links to external files.

Tool priority: Prompt file > Referenced mode > Default mode tools.

### Example chatmode.md File

This creates a "Planning" mode for generating implementation plans without code changes:

```
---
description: Generate an implementation plan for new features or refactoring existing code.
tools: ['fetch', 'githubRepo', 'search', 'usages']
model: Claude Sonnet 4
---
# Planning Mode Instructions

You are in planning mode. Your task is to generate an implementation plan for a new feature or for refactoring existing code. Don't make any code edits—just generate a plan.

The plan consists of a Markdown document with these sections:

* **Overview**: Brief description of the feature or refactoring.
* **Requirements**: List of requirements.
* **Implementation Steps**: Detailed steps to implement.
* **Testing**: List of tests to verify.
```

Save the file, and it will appear in the chat mode dropdown.

### How to Use a Custom Chat Mode

1. Open the **Chat view** (as above).

2. In the dropdown at the top of the Chat view (next to the mode selector), choose your custom mode (e.g., "Planning").

3. The mode's `description` appears as a placeholder in the input box. Type your prompt (e.g., "Plan a user authentication feature").

4. Copilot responds following the mode's instructions and tools. Switch modes anytime via the dropdown—built-in modes (Ask, Edit, Agent) remain available.

For more examples, check community contributions in the [Awesome Copilot repo](https://github.com/github/awesome-copilot/tree/main).

### References
- [Custom chat modes in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-chat-modes)
- [Get started with chat in VS Code](https://code.visualstudio.com/docs/copilot/chat/copilot-chat)
