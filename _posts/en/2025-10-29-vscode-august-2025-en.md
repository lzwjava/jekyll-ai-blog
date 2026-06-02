---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Visual Studio Code August 2025 Update
translated: false
type: note
---

### Visual Studio Code 1.104 (August 2025)

This release focuses heavily on AI enhancements for GitHub Copilot, improved security for AI tools, and productivity boosts across the editor and terminal. Here's a breakdown of the key updates:

#### AI Features

- **Auto Model Selection (Preview)**: Chat now automatically picks the best model (e.g., Claude Sonnet 4, GPT-5 variants) based on performance and rate limits when "Auto" is selected; includes a 10% request discount for paid users.
- **Confirm Edits to Sensitive Files**: Agent mode requires user approval before editing system files, dotfiles, or anything outside the workspace; customizable via settings.
- **Support for AGENTS.md Files (Experimental)**: Automatically incorporates workspace `AGENTS.md` as context for chat requests.
- **Enhanced Coding Agents Collaboration (Experimental)**: Better session management, GitHub integration, and delegation from TODO comments or chat.
- **Terminal Auto Approve**: Opt-in for safer command execution with warnings for risky actions like `curl` or `wget`; new rules for approvals.
- **Math Rendering**: KaTeX equations now render inline by default in chat responses.
- **Improved #codebase Tool**: Uses a new embeddings model for faster, more efficient semantic code search.
- **Disable AI Features**: New setting to hide and disable Copilot chat, completions, and suggestions globally or per workspace.
- **Python-Specific AI Tools (Experimental/Preview)**: AI-powered hover summaries for undocumented symbols and a "Run Code Snippet" tool for in-memory execution.

#### Security

- **AI Tool Safeguards**: Expanded confirmations for sensitive edits, terminal commands, and global auto-approvals, with warnings and configurable rules to mitigate risks.
- **Documentation**: New guidance on security considerations for AI-powered development.

#### Productivity

- **Chat View Defaults**: Chat now opens by default in the Secondary Side Bar; customizable visibility.
- **Terminal Improvements**: Better IntelliSense (e.g., git completions, icons), sticky scroll, and actions in terminal editors/windows.
- **Python Environments**: Enhanced Pipenv support, environment variable injection from `.env` files, and full IntelliSense in all Python documents.
- **Editor Tweaks**: Configurable inline suggestion delay, tab index for keyboard nav, and window border colors on Windows.
- **GitHub Pull Requests**: Collapsible sidebar, TODO actions for Copilot, and submodule ignore options.
- **Task and Terminal Support**: Improved input handling, error surfacing, and shell integration timeouts.

#### Other Notable Changes

- **Accessibility**: Focus command for chat confirmations to aid screen readers.
- **Languages**: Removed built-in Bower.json IntelliSense (deprecated tool; migrate to npm/yarn).
- **Extension Authoring**: Proposed APIs for authentication challenges and secondary sidebar contributions.
- **Deprecations**: Settings like `chat.mcp.enabled` migrated; Bower support dropped.

For full details, check the official release notes.

[August 2025 (version 1.104)](https://code.visualstudio.com/updates/v1_104)
