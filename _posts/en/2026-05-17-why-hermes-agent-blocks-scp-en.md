---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Hermes Agent Blocks scp
translated: false
type: note
---

**Question:** Why was the `scp` command blocked by the Hermes agent?

**Answer:**

The `scp` command was blocked because **Hermes (and Claude Code underneath it) treats `scp` as a potentially dangerous network command by default**. Here's a breakdown of why:

---

## 1. `scp` is on the Default Deny List

Common security configurations for Claude Code explicitly include `Bash(scp *)` in the deny list, alongside other commands like `ssh *`, `curl *`, `wget *`, `kubectl apply *`, and `terraform apply *` — all commands that can exfiltrate data or connect to remote hosts.

This means if your Hermes or Claude Code settings have `scp` in the deny rules, **any `scp` command is automatically rejected**, regardless of intent.

---

## 2. Claude Code's "Fail Closed" Security Design

Claude Code uses strict read-only permissions by default. When additional actions are needed — such as running shell commands — it requests explicit permission. The system is designed to "fail closed": unmatched or disallowed commands default to requiring manual approval or being blocked outright.

`scp` transfers files to a **remote host over SSH**, which is exactly the kind of network exfiltration vector the security system is designed to prevent.

---

## 3. Network-to-Remote-Host Commands Are High Risk

Claude Code blocks risky commands that fetch or send content over the network by default. Commands that make network requests require user approval.

`scp` to a remote host like `lzw@192.168.1.36` fits squarely in this category — it's sending a local file to a remote machine over the network.

---

## 4. Hermes Agent Cannot Run It on Your Behalf

The Hermes agent operates in a sandboxed context. Even if you want it to run `scp`, the agent:
- Cannot authenticate to your SSH key/remote host from inside its environment
- Does not have access to your local filesystem paths (like `/Users/lzwjava/Documents/...`)
- Is intentionally restricted from running commands that could exfiltrate data to external hosts

That's why Hermes correctly tells you: **"You'll need to run it yourself."** This is expected, safe behavior — not a bug.

---

## How to Run It Yourself

Simply copy and run the provided command in your own terminal:

```bash
scp "/Users/lzwjava/Documents/TencentMeeting/2026-05-17 10.30.30 Started by Zhiwei Li 992874154/meeting_01.mp4" lzw@192.168.1.36:~/projects/private-projects/whisper-playground/
```

This runs with **your** credentials and SSH keys, which is the correct and secure way to do it.

**References:**

- [AI Coding Agent Security: Practical Guardrails for Claude Code – DEV Community](https://dev.to/maxkrivich/ai-coding-agent-security-practical-guardrails-for-claude-code-copilot-and-codex-och)
- [Security – Claude Code Docs](https://code.claude.com/docs/en/security)
- [Stop Fighting Claude Code's Permission Prompts – Stackademic](https://medium.com/@tonimaxx/stop-fighting-claude-codes-permission-prompts-here-s-how-the-system-actually-works-ae594e59fb13)
- [Hermes Agent – Claude Code Skill](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code)