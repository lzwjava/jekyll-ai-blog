---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smart Approval Mode Status and Settings
translated: false
type: note
---

Your config confirms `approvals.mode: smart` is set at line 406. Here's the status:

**Config file (~/.hermes/config.yaml):**
- `approvals.mode: smart` -- SET (line 406)
- `approvals.timeout: 60` -- SET (line 407)
- `approvals.cron_mode: deny` -- (line 408)
- `auxiliary.approval.provider: auto` -- (line 198, the LLM used for smart assessments)

**Applied in current session?**

Yes. The config is read at session start, so your current session has `smart` mode active. When a command matches a dangerous pattern, instead of immediately prompting you, Hermes will call the auxiliary approval LLM to assess risk. If the LLM deems the command safe, it passes through automatically. Only genuinely risky ones will prompt you.

**Key details for your setup:**
- `auxiliary.approval.provider: auto` means it inherits your main provider (openrouter) and picks a small/cheap model for the risk assessment call.
- `subagent_auto_approve: false` (line 348) -- subagents will NOT auto-approve dangerous commands; they'll be denied. If you run batch/cron jobs and want them to proceed without blocking on approval, flip that to `true`.
- `terminal.backend: local` (line 67) -- you're running commands directly on your host, so dangerous-command checks are still relevant (they'd be skipped in a Docker container backend).

If you find `smart` mode still prompts too often, the next step down is `mode: off`. But with `smart` + `local` backend, you get a reasonable middle ground: the LLM filters out false positives while catching genuinely dangerous operations.
