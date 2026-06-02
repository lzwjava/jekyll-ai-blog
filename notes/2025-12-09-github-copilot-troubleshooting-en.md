---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: GitHub Copilot Extension Troubleshooting Guide
translated: false
type: note
---

Question: Why does the GitHub Copilot extension in VS Code on Windows sometimes become unresponsive, requiring me to open a new window, and why can't I switch between Ask and Agent modes?

Answer:

The GitHub Copilot extension in Visual Studio Code (VS Code) can become unresponsive or frozen on Windows due to several common issues, particularly when using features like the Chat view (with modes such as Ask for questions, Edit for code changes, or Agent for autonomous tasks). This often manifests as the interface hanging, requiring a full reload or new window to resolve, and prevents switching between modes because the extension host process becomes stuck. Based on user reports and official troubleshooting, here are the most likely causes and fixes:

### Common Causes

- **Extension or VS Code Caching/Loading Issues**: Copilot's chat features rely on background processes for AI requests. If these get stuck (e.g., during long Agent mode tasks), the UI freezes. This is exacerbated when switching windows or tabs while an Agent task runs, as it interrupts the process.
- **Outdated or Conflicting Versions**: Incompatible VS Code or Copilot versions can cause mode-switching to fail. For instance, recent updates (like VS Code 1.102+) have had bugs where the mode selector becomes unresponsive.
- **Authentication or Subscription Limits**: If you're on the free Copilot plan, you may hit monthly chat limits, causing hangs. Token glitches or expired sessions also block features like Agent mode.
- **Resource Constraints on Windows**: Low memory, restricted mode (e.g., in untrusted workspaces), or background processes (like large embedding files in Copilot's cache) can overload the extension host, leading to "unresponsive" errors.
- **Agent Mode-Specific Bugs**: Agent mode is more resource-intensive and prone to infinite "Working..." loops, especially after interrupted tasks or with certain models (e.g., GPT variants). This doesn't affect simpler Ask mode.

### Troubleshooting Steps

Try these in order—most users resolve it without reinstalling:

1. **Quick Reloads**:
   - Reload the window: Press `Ctrl+Shift+P`, type "Developer: Reload Window", and select it. This refreshes Copilot without closing your work.
   - Restart extensions: Open Extensions view (`Ctrl+Shift+X`), click the "..." menu, and select "Restart Extensions". This often fixes unresponsiveness without a full restart.

2. **Check Logs for Clues**:
   - Open Command Palette (`Ctrl+Shift+P`), run "Output: Show Output", and select "GitHub Copilot" or "GitHub Copilot Chat". Look for errors like connection failures or large file warnings (e.g., embeddings.json >5MB). Set log level to "Trace" via "Developer: Set Log Level" for more details.

3. **Verify Settings and Auth**:
   - Ensure Agent mode is enabled: Go to Settings (`Ctrl+,`), search for "chat.agent.enabled", and toggle it on.
   - Sign out/in: Click the Accounts icon (bottom-left), sign out of GitHub, then sign back in.
   - Check subscription: Visit [GitHub Copilot settings](https://github.com/settings/copilot) to confirm active access and no limits.

4. **Clear Cache and Data**:
   - Run `Ctrl+Shift+P` > "GitHub Copilot: Clear Copilot Data" (or similar commands in Output panel).
   - Delete large cache files: Navigate to `%APPDATA%\Code\User\globalStorage` (or workspace-specific) and remove Copilot-related folders like `github.copilot-chat`. Restart VS Code.

5. **Update Everything**:
   - Update VS Code and Copilot extension to the latest versions via Extensions view.
   - If on Windows, run VS Code as Administrator once to rule out permission issues.

6. **Workarounds for Mode Switching**:
   - Open a new Chat view: Press `Ctrl+Alt+I` to open Chat in a side panel, then select the mode from the dropdown. If stuck, close the current chat tab and start fresh.
   - Avoid multitasking: Don't switch windows during Agent tasks; let them complete.

If these don't help, collect diagnostics via `Ctrl+Shift+P` > "GitHub Copilot: Collect Diagnostics" and report on the [VS Code GitHub issues](https://github.com/microsoft/vscode/issues). For persistent freezes, temporarily disable other extensions to isolate conflicts.

References:

- [GitHub Copilot FAQ](https://code.visualstudio.com/docs/copilot/faq)
- [Stack Overflow: GitHub Copilot not working suddenly](https://stackoverflow.com/questions/71806576/why-is-my-github-copilot-not-working-all-of-a-sudden)
- [VS Code Issue: Unable to switch Copilot modes](https://github.com/microsoft/vscode/issues/260293)
- [GitHub Docs: Troubleshooting Copilot](https://docs.github.com/copilot/troubleshooting-github-copilot/troubleshooting-common-issues-with-github-copilot)
- [GitHub Discussion: VS Code freezing with Copilot Agent](https://github.com/orgs/community/discussions/159701)
- [GitHub Discussion: Copilot Chat issues](https://github.com/orgs/community/discussions/156686)
