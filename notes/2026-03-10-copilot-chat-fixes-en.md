---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot Chat Fixes Guide
translated: false
type: note
---

**Question:** Why does GitHub Copilot in VS Code sometimes not allow sending messages, and only works after opening a new Copilot window?

**Answer:**

This is a well-known and widely reported bug/issue with the GitHub Copilot Chat extension in VS Code. Here is a comprehensive explanation of the root causes and how to fix them.

---

## Root Causes

### 1. Extension Failed to Activate (Most Common)

When you click Send Chat Feedback, a message saying "Activating Extensions..." shows up in the Status Bar, but nothing happens — this indicates the Copilot Chat extension is in a "Not yet activated" state. This means the extension process did not fully initialize when VS Code started up. Opening a new window forces a fresh extension host process, which is why it works in a new window.

### 2. Corrupted Extension State / Stale Session

Disabling the GitHub.copilot-chat extension, reloading the window, and re-enabling it again has been found to fix the issue for many users. This points to a stale or corrupted in-memory extension state — a session that got into a broken condition without crashing fully.

### 3. Authentication / Account Token Expiry

Going to Accounts (bottom left) → "Manage extension account preferences" → "Github Copilot Chat" → reselecting your account has resolved the issue for some users. This happens because the auth token silently expires or gets confused between sessions.

### 4. Pasting Text Bug in the Chat Input

When pasting text while the cursor is at the beginning of a context reference, something breaks and the prompt cannot be sent. This is a specific bug in the Copilot Chat extension that corrupts the chat input state without any obvious error shown to the user.

### 5. Extension Version Mismatch with VS Code

You must be on the latest version of Visual Studio Code, and must have the latest version of both the GitHub Copilot and GitHub Copilot Chat extensions. An outdated VS Code version can cause extension activation failures silently.

### 6. Free Plan Monthly Limit Stale Cache

If you are on the free plan, the backend might read old stale data and register that you've already used your free allotment for the month even though it just began. The UI freezes without clearly telling you why messages aren't sending.

---

## Fixes (Try in Order)

**Quick fixes (no reinstall needed):**

1. **Reload the VS Code window** — Press `Ctrl+Shift+P` → type `Developer: Reload Window` → Enter. This is the fastest fix.
2. **Disable → Reload → Re-enable the Copilot Chat extension** — Go to Extensions panel, disable `GitHub Copilot Chat`, reload window, then re-enable it.
3. **Re-select your GitHub account** — Go to Accounts (bottom-left icon) → "Manage extension account preferences" → "GitHub Copilot Chat" → reselect your account.
4. **Sign out and sign back in** — Logging out of all GitHub accounts and logging back in has resolved the issue for some users.
5. **Check the Output log** — Check the Output pane under the "Window" category in VS Code for error messages that explain why the send button isn't working.

**Deeper fixes (if above don't work):**

6. **Update VS Code** — Run `Help → Check for Updates`.
7. Go to Extensions, and if you see a blue "Reload Required" button for GitHub Copilot, press it.
8. **Delete the `.vscode` config folder** — Deleting the `.vscode` folder (e.g., `C:\Users\<YOUR USER>\.vscode` on Windows) and restarting has fixed the problem for some users.
9. **Full reinstall** — Uninstall VS Code completely and reinstall it fresh.

---

## Why Does a New Window Fix It?

Opening a new VS Code window creates a **fresh extension host process**. The old window had a broken/stuck extension runtime (authentication state, activation state, or input state corruption), and the new window starts everything cleanly from scratch — so Copilot activates properly and the chat input works again.

**References:**

- [GitHub Issue: Can't send messages to copilot chat #941](https://github.com/microsoft/vscode-copilot-release/issues/941)
- [GitHub Issue: Unable to submit chats #565](https://github.com/microsoft/vscode-copilot-release/issues/565)
- [GitHub Issue: Missing send button in copilot chat #262645](https://github.com/microsoft/vscode/issues/262645)
- [GitHub Discussion: Copilot Chat Not Working Even After Reinstalling VS Code](https://github.com/orgs/community/discussions/167353)
- [VS Code Copilot FAQ – Official Troubleshooting](https://code.visualstudio.com/docs/copilot/faq)
- [Tim Taurit Blog: Send and Dispatch button broken diagnosis](https://taurit.pl/vs-code-github-copilot-send-and-dispatch-button-not-working/)
