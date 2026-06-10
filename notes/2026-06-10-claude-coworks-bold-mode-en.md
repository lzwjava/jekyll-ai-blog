---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Cowork's Bold Mode
translated: false
type: note
---

**Question:** What is "Act without asking" in the Claude Mac (desktop) app?

**Answer:**

"Act without asking" is a permission mode in Claude Cowork (the agentic mode in the Claude desktop app, including macOS) and in Claude in Chrome. It's the autonomous end of a two-mode toggle on the chat input:

- **Ask before acting** (default, safer): Claude creates a plan from your prompt — specifying which sites/resources it will touch and the approach — which you approve before it executes. It then acts within those parameters but still checks with you before irreversible actions like purchases, account creation, or downloads.
- **Act without asking**: Claude executes multi-step tasks without pausing for approval between steps. It's faster for well-defined tasks, but it significantly increases the risk of prompt injection attacks — a malicious instruction embedded in a webpage, email, or file Claude reads could steer it mid-task with no human checkpoint to catch it.

Even in "Act without asking," some guardrails are non-negotiable:

- File deletion still requires an explicit "Allow" permission prompt, and computer use asks before accessing each application.
- Certain actions are always prohibited regardless of mode — bypassing bot checks/CAPTCHAs, executing financial trades, permanently deleting files, and actions flagged as likely prompt-injection.
- Anthropic layers defenses behind it: RL training to refuse malicious instructions even when they appear authoritative, plus classifiers that scan all untrusted content entering Claude's context for injections.

**Practical guidance for your setup:** treat it like `--dangerously-skip-permissions` in Claude Code, but with classifier backstops. Fine for well-scoped, local tasks on your M2 Air (e.g., "reorganize this folder of notes," "batch-rename these files"). Avoid it when the task involves credentials, your bank work context, browsing untrusted pages, or anything touching `~/.ssh`, API keys in env files, or your `192.168.1.36` workstation over SSH — injected content + no approval loop is exactly the attack surface. Conceptually it maps to the `bypassPermissions` end of Claude Code's permission spectrum (`ask` → `auto` → `allow`), whereas Claude Code's newer "auto mode" is the middle path that passes each action through a risk classifier — auto-approving safe operations and blocking or escalating risky ones like file deletion.

**References:**

- [Claude in Chrome Permissions Guide — Claude Help Center](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- [Use Claude Cowork safely — Claude Help Center](https://support.claude.com/en/articles/13364135-use-claude-cowork-safely)
