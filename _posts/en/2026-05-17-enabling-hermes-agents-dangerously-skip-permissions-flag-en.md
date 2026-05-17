---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling Hermes Agent's Dangerously Skip Permissions Flag
translated: false
type: note
---

**Question:** How do I enable the `--dangerously-skip-permissions` flag when using the Hermes agent with Claude Code?

**Answer:**

There are **three approaches** depending on how Hermes launches Claude Code — interactive mode (tmux), print mode, or via a persistent settings file.

---

## Option 1: Interactive Mode via tmux (Most Common in Hermes)

Hermes uses tmux to orchestrate Claude Code in interactive mode. You can launch with the permissions bypass flag like this:

```bash
# Step 1: Launch Claude Code with the flag inside tmux
tmux send-keys -t claude-work 'claude --dangerously-skip-permissions "your task"' Enter

# Step 2: Handle the first trust dialog (press Enter for default "Yes")
sleep 4 && tmux send-keys -t claude-work Enter

# Step 3: Handle the permissions dialog (Down arrow then Enter to accept)
sleep 3 && tmux send-keys -t claude-work Down && sleep 0.3 && tmux send-keys -t claude-work Enter

# Step 4: Wait and capture output
sleep 15 && tmux capture-pane -t claude-work -p -S -60
```

**Important:** After the first trust acceptance for a directory, the trust dialog won't appear again. Only the permissions dialog recurs each time you use `--dangerously-skip-permissions`.

---

## Option 2: Print Mode (Simplest — No Flag Needed)

Print mode runs a one-shot task, returns the result, and exits. It skips ALL interactive dialogs — no workspace trust prompt, no permission confirmations. This makes it ideal for automation.

```bash
terminal(command="claude -p 'your task here' --allowedTools 'Read,Edit,Bash' --max-turns 10", workdir="/path/to/project", timeout=120)
```

This is the **cleanest and safest path** if you just want uninterrupted execution without dealing with the permission dialog at all.

---

## Option 3: Persistent Settings (Recommended for Daily Use)

Set `defaultMode` in your project's `.claude/settings.json` so every session in that directory starts with bypass enabled automatically:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

The `--dangerously-skip-permissions` flag is equivalent to `--permission-mode bypassPermissions`. Administrators can block this mode by setting `permissions.disableBypassPermissionsMode` to `"disable"` in managed settings.

---

## Option 4: Hermes IDE Wizard (GUI Checkbox)

If you want a fully async operation, enable "Auto-approve all actions" in the Hermes wizard. This maps to `--dangerously-skip-permissions` and lets Claude read, write, and execute without stopping to ask.

---

## ⚠️ Safety Reminder

`bypassPermissions` offers no protection against prompt injection or unintended actions. On Linux and macOS, Claude Code refuses to start in this mode when running as root or under sudo.

Best practice before using it: **always `git commit` your work first**, so you can `git reset` if Claude does something unexpected.

**References:**

- [Hermes Agent – Claude Code Skill Docs](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code)
- [Claude Code – Choose a Permission Mode](https://code.claude.com/docs/en/permission-modes)
- [How to Control Claude Code from Telegram Using Hermes IDE](https://medium.com/@anhaia.gabriel/how-to-control-claude-code-from-telegram-using-hermes-ide-3d81c6705f8c)
- [Claude Code Autonomous Mode Guide](https://pasqualepillitteri.it/en/news/141/claude-code-dangerously-skip-permissions-guide-autonomous-mode)